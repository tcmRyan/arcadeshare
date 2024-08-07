
import os

from flask import current_app
from src.auth import Tenant
from src.server.utils import main_db_sql, create_binds


def test_tenant_creation(app, test_user):
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    tenant = Tenant(name="tenant1")
    tenant.users.append(test_user)
    tenant.save()
    assert current_app.config["SQLALCHEMY_BINDS"] == {
        "test_main": f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/test_main",
        "tenant1": f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/tenant1"
    }
    sql = "DROP database tenant1"
    main_db_sql(sql)


def test_startup(app, test_user):
    pass


def test_create_binds():
    create_binds()
