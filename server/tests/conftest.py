import os

import pytest
from flask import testing
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import close_all_sessions
from werkzeug.datastructures import Headers

from server import create_app, db
from server.auth import User
from server.auth.schema import ProfileSchema
from server.utils import main_db_sql


@pytest.fixture
def app():

    app = create_app()

    with app.app_context():
        sql = f"CREATE database {os.environ['MAIN_DB']}"
        main_db_sql(sql)
        db.create_all()
        yield app
        db.session.close()
        close_all_sessions()
        db.engine.dispose()
        sql = f"DROP database {os.environ['MAIN_DB']}"
        main_db_sql(sql)


@pytest.fixture()
def test_user(app):
    with app.app_context():
        user = User()
        user.email = "tester@arcade.com"
        user.name = "Arcade Tester"
        user.username = "arcade.tester"

        db.session.add(user)
        db.session.commit()
        yield user


class AuthClient(testing.FlaskClient):

    def open(self, *args, **kwargs):
        test_user = User.query.filter_by(username="arcade.tester")
        access_token = create_access_token(
            identity=ProfileSchema().dump(test_user), expires_delta=False, fresh=True
        )
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        headers = kwargs.pop("headers", Headers())
        headers.update(auth_headers)
        kwargs["headers"] = headers
        return super().open(*args, kwargs)


@pytest.fixture
def a_client(app, test_user):
    app.test_client_class = AuthClient
    with app.test_client() as client:
        yield client

