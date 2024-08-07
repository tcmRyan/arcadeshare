import os.path

from flask import request, current_app
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt
from flask_restx import Namespace, Resource
from flask_security import roles_required
from werkzeug.utils import secure_filename

from src.server import admin_permission
from src.server.auth.models import User
from src.server.auth.schema import ProfileSchema, Profile, UserSchema

ns = Namespace("users", "System users", decorators=[cross_origin()])


@ns.route("/<int:uid>")
class UserResource(Resource):
    decorators = [jwt_required()]

    def get(self, uid):
        schema = UserSchema()
        user = User.query.get(uid)
        return schema.dump(user)


@ns.route("/me")
class MeResource(Resource):
    decorators = [jwt_required()]

    def get(self):
        schema = ProfileSchema()
        return schema.dump(Profile())


@ns.route("/")
class UsersResource(Resource):
    decorators = [jwt_required()]

    @roles_required(["admin"])
    def get(self):
        schema = UserSchema(many=True)
        claims = get_jwt()
        tenant_users = User.query.filter_by(tenant_id=claims.get("tenant")).all()
        return schema.dump(tenant_users)

    @admin_permission.require()
    def post(self):
        schema = UserSchema()
        claims = get_jwt()
        user = schema.load(request.get_json())

        # Ensure users can't create users outside their tenant
        user.tenant_id = claims["tenant"]
        user.save()
        return schema.dump(user), 201


@ns.route("/bulk-update")
class UsersBulkResource(Resource):
    decorators = [jwt_required()]

    @roles_required(["admin"])
    def post(self):

        if "file" not in request.files:
            pass

        file = request.files['file']
        allowed = '.' in file.filename and file.filename.split(".", 1)[1].lower() in ["csv"]
        if file.filename and allowed:
            filename = secure_filename(file.filename)
            file.save(os.path.join((current_app.config["UPLOAD_FOLDER"], filename)))
