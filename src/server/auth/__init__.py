from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import get_jwt

from .azure import azure_bp
from .google import google_bp
from .models import *

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates"
)


def required_roles(roles):
    def wrapper(fn):
        def wrapped_fn(*args, **kwargs):
            if os.environ.get("JWT_OFF", False):
                return fn(*args, **kwargs)
            claims = get_jwt()
            for claim in claims["roles"]:
                if claim in roles:
                    return fn(*args, **kwargs)
            return HTTPStatus.FORBIDDEN

        return wrapped_fn()

    return wrapper


from . import routes
