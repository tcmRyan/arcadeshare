"""
The Models in the database are bound to the 'arcade' database and
not replicated across all the tenant dbs.
"""
import hashlib
import os

from flask import current_app
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_security import RoleMixin, UserMixin
import psycopg2
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection
import sqlalchemy
from werkzeug.security import gen_salt

from server import db
from server.signals import tenant_provisioned
from server.utils.storage import S3StorageProvider

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    """
    User Roles for Authentication
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String(255))

    @staticmethod
    def create_roles():
        super_admin = Role(name="site_admin", description="Controls all sites / domains")
        admin = Role(name="admin", description="Administers a location")
        user = Role(name="user", description="arcade creator")

        current_roles = [
            super_admin,
            admin,
            user
        ]
        for role in current_roles:
            query = Role.query.filter_by(name=role.name)
            try:
                query.one()
            except NoResultFound:
                db.session.add(role)
                db.session.commit()

    def __repr__(self):
        return f"<Role: {self.name} >"


class User(db.Model, UserMixin):
    __table_args = (UniqueConstraint('email', 'username', name="_username_uc"),)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, default=None)
    password_hash = db.Column(db.String)
    username = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    # default="pbkdf2:sha256"
    salt = db.Column(db.String)
    is_superuser = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}:{self.email} >" if self.email else f"<User {self.id}:{self.username} >"

    def __unicode__(self):
        return self.password_hash

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        if not self.password_hash == password:
            self.salt, self.password_hash = self.generate_emqx_password(password)

    def verify_password(self, password):
        tsalt = self.salt.encode("utf-8")
        tpwd = password.encode("utf-8")
        check = hashlib.pbkdf2_hmac("sha256", tpwd, tsalt, 26000).hex()
        return check == self.password[2:]

    @staticmethod
    def get_by_username_or_email(username_or_email):
        result = User.query.filter_by(username=username_or_email).one_or_none()
        if not result:
            result = User.query.filter_by(email=username_or_email).one_or_none()
        return result

    @staticmethod
    def generate_emqx_password(password):
        salt = gen_salt(16)
        en_salt = salt.encode("utf-8")
        password = password.encode("utf-8")
        password = hashlib.pbkdf2_hmac("sha256", password, en_salt, 26000)
        return salt, password


class OAuth(OAuthConsumerMixin, db.Model):
    """
    OAuth Tokens associated with the user.  Allows for the support of multiple OAuth vendors
    """
    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(
        User,
        # This `backref` thing sets up an `oauth` property on the Users get_or_create_model_from_json,
        # which is a dictionary of OAuth models associated with that user,
        # where the dictionary key is the OAuth provider name.
        backref=db.backref(
            "oauth",
            collection_class=attribute_mapped_collection("provider"),
            cascade="all, delete-orphan",
        ),
    )


class Tenant(db.Model):
    """
    Mapping for all requests to a give
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship("User", backref="tenant", lazy=True)

    def provision(self):
        conn = psycopg2.connect(
            database="postgres",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            host=os.environ["DB_HOST"],
            port="5432"
        )
        conn.autocommit = True

        cursor = conn.cursor()
        db_name = self.name.lower()
        sql = f"CREATE database {db_name}"
        current_app.logger.info("Executing: %s", sql)
        cursor.execute(sql)

        conn.close()
        binds = current_app.config.get("SQLALCHEMY_BINDS", {})
        new_bind = {db_name: current_app.config.get("DB_URL").format(db_name)}
        if binds:
            binds.update(new_bind)
        else:
            binds = new_bind
        current_app.config.update({"SQLALCHEMY_BINDS": binds})
        db.create_all(bind=db_name)
        storage = S3StorageProvider()
        storage.provision(self.id)
        tenant_provisioned.send(self)


class MqttAcl(db.Model):
    __table_name__ = "mqtt_acl"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    permission = db.Column(db.String)
    action = db.Column(db.String)
    topic = db.Column(db.String)


@sqlalchemy.event.listens_for(db.session, "after_flush")
def provision(session, flush_context):
    for instance in session.new:
        if not isinstance(instance, Tenant):
            continue
        current_app.logger.info("Creating DB for %s", instance.name)
        instance.provision()
