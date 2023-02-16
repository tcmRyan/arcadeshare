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
    MQTT_BROKER_URL = os.environ.get("MQTT_BROKER_URL", "localhost")
    MQTT_BROKER_PORT = os.environ.get("MQTT_BROKER_PORT", 1883)
    MQTT_USERNAME = os.environ.get("MQTT_USERNAME", "system")
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "temp1234")
    MQTT_KEEPALIVE = os.environ.get("MQTT_KEEPALIVE", 5)
    MQTT_TLS_ENABLED = os.environ.get("MQTT_TLS_ENABLED", False)


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
