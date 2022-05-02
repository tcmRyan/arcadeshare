import os

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint
from flask_login import current_user

from server import db
from server.auth.models import OAuth

google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT"),
    client_secret=os.environ.get("GOOGLE_SECRET"),
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    redirect_url="/success"
)
