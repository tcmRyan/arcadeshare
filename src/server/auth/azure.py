import os

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.azure import make_azure_blueprint
from flask_login import current_user

from src.server import db
from src.server.auth.models import OAuth

azure_bp = make_azure_blueprint(
    client_id=os.environ.get("AZURE_CLIENT_ID"),
    client_secret=os.environ.get("AZURE_SECRET"),
    storage=SQLAlchemyStorage(OAuth, db.session, current_user),
    redirect_url="/success"
)
