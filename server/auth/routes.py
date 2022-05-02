from flask import render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_login import current_user

from server.auth import auth_bp
from server.auth.schema import Profile, ProfileSchema


@auth_bp.route("/success")
def success():
    if current_user.is_anonymous:
        return render_template("failure.html", data={})
    return render_template("success.html", data=ProfileSchema.dump(Profile()))


@auth_bp.route("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
