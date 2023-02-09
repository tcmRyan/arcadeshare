import os
import pathlib

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
TENANT_DB_BASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/"


class Config:
    DEBUG = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = True
    DB_URL = TENANT_DB_BASE_URL + "{}"
    MAIN_DB = os.environ.get("MAIN_DB")
    SQLALCHEMY_DATABASE_URI = DB_URL.format(MAIN_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "d3vs3cr3t"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_SALT") or "d3vs3cr3t"
    SECURITY_PASSWORD_HASH = "bcrypt"
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"csv"}
    ROOT_PATH = pathlib.Path(__file__).parent
    pathlib.Path("./flask-tmp").mkdir(parents=True, exist_ok=True)
    TEMP_FILES = str((ROOT_PATH / pathlib.Path("./flask-tmp")).resolve())
    BOTO_ENDPOINT = os.environ.get("BOTO_ENDPOINT")
    BOTO_PROFILE = os.environ.get("BOTO_PROFILE")
    DEFAULT_REGION = os.environ.get("DEFAULT_REGION")


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
