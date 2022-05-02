import os

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_login import current_user
from flask_marshmallow.fields import fields
from typemallow2 import ts_interface

from server import ma, db
from server.auth.models import Role, User


@ts_interface()
class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
        load_instance = True
        include_fk = True


@ts_interface()
class UserSchema(ma.SQLAlchemyAutoSchema):

    roles = ma.Nested(RoleSchema, many=True)

    class Meta:
        model = User
        load_instance = True
        include_fk = True
        sqla_session = db.session


@ts_interface()
class ProfileSchema(ma.Schema):

    user = ma.Nested(UserSchema)
    access_token = fields.Str()
    refresh_token = fields.Str()
    expires_in = fields.Int()


class Profile:

    @property
    def roles(self):
        return [role.name for role in current_user.roles]

    @property
    def additional_claims(self):
        return {"roles": self.roles}

    @property
    def user(self):
        return current_user

    @property
    def access_token(self):
        return create_access_token(current_user, additional_claims=self.additional_claims)

    @property
    def refresh_token(self):
        return create_refresh_token(current_user, additional_claims=self.additional_claims)

    @property
    def expires_in(self):
        return os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600)




