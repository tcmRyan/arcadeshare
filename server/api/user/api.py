from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from server.api.schemas import UserSchema
from server.auth.models import User

ns = Namespace("users", "System users")


@ns.route("/<int:uid>")
class UserResource(Resource):

    decorators = [jwt_required()]

    def get(self, uid):
        schema = UserSchema()
        user = User.query.get(uid)
        return schema.dump(user)


# @ns.route("/")
# class UsersResource(Resource):
#
#     decorators = [jwt_required()]
#
#     def get(self):
#         schema = UserSchema(many=True)
#         return
