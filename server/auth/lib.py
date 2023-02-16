import functools
from hmac import compare_digest
from http import HTTPStatus

from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from server.api import Device


def required_roles(roles):
    def wrapper(f):
        def wrapped_fn(*args, **kwargs):
            claims = get_jwt()
            for claim in claims:
                if claim in roles:
                    return f(*args, **kwargs)
            return HTTPStatus.FORBIDDEN
        return wrapped_fn
    return wrapper


def is_key_valid(api_key):
    device = Device.find_by_key(api_key)
    if device and compare_digest(device.key, api_key):
        return True


def jwt_or_token_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY")
        if (api_key and is_key_valid(api_key)) or verify_jwt_in_request():
            return func(*args, **kwargs)
        else:
            return {"message": "Invalid token or API key"}, 403
    return decorator

