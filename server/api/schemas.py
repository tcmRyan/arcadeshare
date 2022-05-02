from typemallow2 import ts_interface

from server import db, ma
from server.auth.models import Role, User, Tenant


@ts_interface()
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session


@ts_interface()
class UserSchema(ma.SQLAlchemyAutoSchema):
    roles = ma.Nested(RoleSchema, many=True)

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


@ts_interface()
class TenantSchema(ma.SQLAlchemyAutoSchema):

    users = ma.Nested(UserSchema(only=("id", "name"), many=True))

    class Meta:
        model = Tenant
        load_instance = True
        sqla_session = db.session
