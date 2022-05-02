from flask import Blueprint

from .azure import azure_bp
from .google import google_bp
from .models import *

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates"
)

from server.auth import routes
