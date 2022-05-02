import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

from server.utils import create_binds
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
security = Security()
login_manager = LoginManager()
api = Api()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_BINDS'] = create_binds()
    db.init_app(app)

    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from server import main, auth
        from server.auth.models import Role, User
        ds = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, ds)
        app.register_blueprint(main.main_bp, url_prefix="/app")
        app.register_blueprint(auth.auth_bp, url_prefix="/auth")

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
