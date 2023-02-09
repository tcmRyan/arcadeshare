from http import HTTPStatus

from flask import render_template, jsonify, request, Response, redirect, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_login import current_user
from flask_principal import identity_changed, Identity
from flask_security import login_user
from flask_security.utils import config_value
from flask_security.views import _ctx
from werkzeug.local import LocalProxy

from server.auth import auth_bp, User
from server.auth.basic_auth import LoginFormSchema
from server.auth.schema import Profile, ProfileSchema

# Convenient references
_security = LocalProxy(lambda: current_app.extensions['security'])


@auth_bp.route("/user-login", methods=["POST"])
def user_login():
    data = request.get_json()
    schema = LoginFormSchema()
    user_data = schema.load(data)

    user = User.get_by_username_or_email(user_data["username"])

    if user is None or not user.verify_password(user_data["password"]):
        return Response("{'message': 'Bad username or password'", status=HTTPStatus.NOT_FOUND)
    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    profile_schema = ProfileSchema()
    return profile_schema.dump(Profile())


@auth_bp.route("/admin-login", methods=["POST"])
def admin_login():
    form_class = _security.login_form
    form = form_class(request.form)
    user = User.get_by_username_or_email(request.form.get("email"))
    if user is None or not user.verify_password(request.form.get("password")):
        return _security.render_template(config_value('LOGIN_USER_TEMPLATE'),
                                         login_user_form=form,
                                         **_ctx('login'))
    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    return redirect(request.form.get("next"))


@auth_bp.route("/success")
def success():
    schema = ProfileSchema()
    if current_user.is_anonymous:
        return render_template("failure.html", data={})
    return render_template("success.html", data=schema.dump(Profile()))


@auth_bp.route("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
