import os

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
MAIN_DB = os.environ.get("MAIN_DB")
TENANT_DB_BASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/"



class Config:
    DEBUG = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = True
    DB_URL = TENANT_DB_BASE_URL + "{}"
    SQLALCHEMY_DATABASE_URI = DB_URL.format(MAIN_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "d3vs3cr3t"


class DevConfig(Config):

    DEBUG = True
    CSRF_ENABLED = False
    FLASK_DEBUG = 1
    OAUTHLIB_INSECURE_TRANSPORT = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    DEBUG = True
    CSRF_ENABLED = False
    FLASK_DEBUG = 1
    OAUTHLIB_INSECURE_TRANSPORT = True
    WTF_CSRF_ENABLED = False
