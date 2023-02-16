from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from server.api import RoleSchema
from server.auth import Role
from flask_cors import cross_origin

ns = Namespace("roles", "User Roles", decorators=[jwt_required(), cross_origin()])


@ns.route("/")
class RoleResource(Resource):

    def get(self):
        schema = RoleSchema(many=True)
        return schema.dump(Role.query.filter(Role.name != "superadmin").all())
