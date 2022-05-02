"""
The Models in the database are bound to the 'arcade' database and
not replicated across all the tenant dbs.
"""
import os

from flask import current_app
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_security import RoleMixin, UserMixin
import psycopg2
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.collections import attribute_mapped_collection
from server import db


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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()


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

    def save(self):
        provision = False
        if self.query.filter_by(name=self.name).first() is not None:
            provision = True
        db.session.add(self)
        db.session.commit()
        if provision:
            self.provision()

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
        sql = f"CREATE database {self.name}"

        cursor.execute(sql)

        conn.close()
        binds = current_app.config.get("SQLALCHEMY_BINDS", {})
        new_bind = {self.name: current_app.config.get("DB_URL").format(self.name)}
        if binds:
            binds.update(new_bind)
        else:
            binds = new_bind
        current_app.config["SQLALCHEMY_BINDS"] = binds
