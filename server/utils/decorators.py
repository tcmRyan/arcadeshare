from server import db

from flask_login import current_user


def tenant_context(fn):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            with db.context(current_user.tenant.name):
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return inner
