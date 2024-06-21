import json
import os

import click
from flask import Flask, current_app
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_user
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_principal import (
    identity_loaded,
    UserNeed,
    RoleNeed,
    Permission,
    identity_changed,
    Identity,
)
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_cors import CORS
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_mqtt import Mqtt
from paho.mqtt.client import MQTT_LOG_ERR
from psycopg2 import OperationalError
import psycopg2
from server.admin.views import ArcadeAdminIndexView, UserView
from server.utils import create_binds, MultiTenantSQLA

import logging

from server.utils.storage import S3StorageProvider
from dotenv import load_dotenv

load_dotenv()

logging.getLogger("flask_cors").level = logging.INFO

db = MultiTenantSQLA()
jwt = JWTManager()
ma = Marshmallow()
security = Security()
login_manager = LoginManager()
migrate = Migrate()
cors = CORS()
mqtt = Mqtt()

admin_permission = Permission(RoleNeed("admin"))

admin = Admin(
    name="arcadeshare",
    index_view=ArcadeAdminIndexView(endpoint="admin", url="/admin"),
    base_template="master_admin.html",
    template_mode="bootstrap3",
)

base_roles = [
    {"name": "user", "description": "User that accesses the tenant"},
    {"name": "admin", "description": "Admin of a tenant"},
    {"name": "superadmin", "description": "Admin of the entire site"},
]


def create_app():
    from server.api import api

    app = Flask(__name__)
    app.config.from_object(os.environ["APP_SETTINGS"])

    db.init_app(app)

    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)
    admin.init_app(app)
    mqtt.init_app(app)

    with app.app_context():
        from server import main, auth, api
        from server.auth.models import Role, User, Tenant
        from server import events
        from server.api import Device
        from server.auth import MqttAcl

        ds = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, ds)
        app.register_blueprint(main.main_bp, url_prefix="/app")
        app.register_blueprint(auth.auth_bp, url_prefix="/auth")
        admin.add_view(UserView(User, db.session))
        admin.add_view(ModelView(Role, db.session))
        admin.add_view(ModelView(Tenant, db.session))

        try:
            app.config["SQLALCHEMY_BINDS"] = create_binds()
        except OperationalError as e:
            app.logger.error(e)
            app.logger.info("Run 'flask provision-db' to create the main database")

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.before_request
        def before_request():
            if current_user.is_authenticated and current_user.tenant:
                db.choose_tenant(current_user)

        @app.before_first_request
        def provision_mqtt():

            current_app.logger.info("Setting mqtt frontend")

        secur = app.extensions["security"]

        @secur.context_processor
        def security_context_processor():
            return dict(
                admin_base_template=admin.base_template,
                admin_view=admin.index_view,
                h=admin_helpers,
            )

        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            user = User.query.get(identity)
            login_user(user)
            db.choose_tenant(user)
            identity_changed.send(
                current_app._get_current_object(), identity=Identity(user.id)
            )
            return user

        @jwt.user_identity_loader
        def user_identity_loader(user):
            return user.id

        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            # Set the identity user object
            identity.user = current_user

            # Add the UserNeed to the identity
            if hasattr(current_user, "id"):
                identity.provides.add(UserNeed(current_user.id))

            # Assuming the User model has a list of roles, update the
            # identity with the roles that the user provides
            if hasattr(current_user, "roles"):
                for role in current_user.roles:
                    identity.provides.add(RoleNeed(role.name))

        # @mqtt.on_log()
        # def handle_logging(frontend, userdata, level, buf):
        #
        #     print('{}: {}'.format(level, buf))

        @app.cli.command("provision-db")
        def provision_db():
            conn = psycopg2.connect(
                database="postgres",
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASS"],
                host=os.environ["DB_HOST"],
                port="5432",
            )

            conn.autocommit = True
            cursor = conn.cursor()
            name = os.environ["MAIN_DB"].lower()
            sql = f"CREATE database {name}"
            cursor.execute(sql)
            conn.close()

        @app.cli.command("provision-bucket")
        @click.argument("tenant_name")
        def provision_bucket(tenant_name):
            tenant = Tenant.query.filter_by(name=tenant_name).first()
            if tenant:
                storage = S3StorageProvider()
                storage.provision(tenant.id)
                current_app.logger.info("Bucket PROVISIONED: %s", tenant.id)
            else:
                current_app.logger.error(f"No Tenant found for %s", tenant_name)

        @app.cli.command("list-buckets")
        def list_buckets():
            storage = S3StorageProvider()
            current_app.logger.info(storage.list_buckets())

        @app.cli.command("create-admin")
        @click.argument("email")
        @click.argument("passwd")
        @click.argument("username")
        def create_admin(email, passwd, username):
            roles = Role.query.all()

            if not roles:
                created_roles = [
                    Role(name=role["name"], description=role["description"])
                    for role in base_roles
                    if not Role.query.filter_by(name=role["name"]).one_or_none()
                ]

                security.datastore.db.session.add_all(created_roles)
                security.datastore.db.session.commit()

            user = ds.create_user(
                username=username,
                email=email,
                password=passwd,
                roles=["superadmin"],
            )
            security.datastore.db.session.commit()

        @app.cli.command("restore-mqtt-acl")
        def restore_mqtt_acl():
            tenants = Tenant.query.all()
            for tenant in tenants:
                users = User.query.filter_by(tenant=tenant).all()
                for user in users:
                    device_topic = MqttAcl(
                        username=user.username,
                        permission="allow",
                        action="subscribe",
                        topic=f"{tenant.id}/devices/update",
                    )
                    feed_topic = MqttAcl(
                        username=user.username,
                        permission="allow",
                        action="subscribe",
                        topic=f"{tenant.id}/feeds/update",
                    )
                    game_topic = MqttAcl(
                        username=user.username,
                        permission="allow",
                        action="subscribe",
                        topic=f"{tenant.id}/games/update",
                    )
                    db.session.add_all([device_topic, feed_topic, game_topic])
                    db.session.commit()

    return app
