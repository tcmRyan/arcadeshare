import os
import shutil

from psycopg2.errors import DuplicateDatabase
import pytest
from flask import testing
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import close_all_sessions
from werkzeug.datastructures import Headers

from server import create_app, db, base_roles
from server.auth import User, Role, Tenant
from server.utils import main_db_sql


@pytest.fixture
def app():
    try:
        sql = f"CREATE database {os.environ['MAIN_DB']}"
        main_db_sql(sql)
    except DuplicateDatabase:
        sql = f"DROP database {os.environ['MAIN_DB']}"
        main_db_sql(sql)
        sql = f"CREATE database {os.environ['MAIN_DB']}"
        main_db_sql(sql)

    app = create_app()

    with app.app_context():
        print("create all")
        db.create_all()
        yield app
        db.session.close()
        close_all_sessions()
        db.engine.dispose()
        sql = f"DROP database {os.environ['MAIN_DB']}"
        main_db_sql(sql)


@pytest.fixture(autouse=True)
def system_user(app):
    with app.app_context():
        roles = Role.query.all()
        if not roles:
            created_roles = [
                Role(name=role["name"], description=role["description"])
                for role in base_roles
                if not Role.query.filter_by(name=role["name"]).one_or_none()
            ]
            db.session.add_all(created_roles)
            db.session.commit()

        user = User()
        user.roles = [role for role in created_roles if role.name == "superadmin"]
        user.username = "system"
        user.password = "test1234"
        db.session.add(user)
        db.session.commit()


@pytest.fixture()
def tenant(app):
    sql = "DROP database test_tenant"
    main_db_sql(sql)
    tenant = Tenant()
    tenant.name = "test_tenant"
    db.session.add(tenant)
    db.session.commit()
    yield tenant


@pytest.fixture()
def test_user(app, tenant):
    with app.app_context():
        user = User()
        user.email = "tester@arcade.com"
        user.name = "Arcade Tester"
        user.username = "arcade.tester"
        user.tenant_id = 1

        db.session.add(user)
        db.session.commit()
        yield user


class AuthClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        test_user = User.query.filter_by(username="arcade.tester").first()
        access_token = create_access_token(
            identity=test_user, expires_delta=False, fresh=True
        )
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        headers = kwargs.pop("headers", Headers())
        headers.update(auth_headers)
        kwargs["headers"] = headers
        return super().open(*args, **kwargs)


@pytest.fixture
def a_client(app, test_user):
    app.test_client_class = AuthClient
    with app.test_client() as client:
        yield client


@pytest.fixture
def cleanup_tmp_files(app):
    yield
    shutil.rmtree(app.config["TEMP_FILES"])
