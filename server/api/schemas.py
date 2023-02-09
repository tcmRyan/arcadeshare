from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import auto_field
from marshmallow import EXCLUDE
from typemallow2 import ts_interface

from server import db, ma
from server.api import Game
from server.api.device.models import Device
from server.api.feed.models import Feed
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
    tenant = ma.Nested("TenantSchema", many=True)
    password_hash = auto_field(data_key="password", attribute="password")

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ("password_hash", "salt")


@ts_interface()
class TenantSchema(ma.SQLAlchemyAutoSchema):
    users = ma.Nested(UserSchema(only=("id", "username"), many=True))

    class Meta:
        model = Tenant
        load_instance = True
        sqla_session = db.session


@ts_interface()
class GameSchema(ma.SQLAlchemyAutoSchema):
    thumbnail_uri = fields.Method("get_thumbnail")
    game_uri = fields.Method("get_game")

    def get_thumbnail(self, obj: Game):
        return obj.download_redirect(obj.thumbnail) if obj.thumbnail else ""

    def get_game(self, obj: Game):
        return obj.download_redirect(obj.bucket)

    class Meta:
        model = Game
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE


@ts_interface()
class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        load_instance = True
        sqla_session = db.session


@ts_interface()
class FeedSchema(ma.SQLAlchemyAutoSchema):
    games = ma.Nested(GameSchema, many=True)

    class Meta:
        model = Feed
        load_instance = True
        sqla_session = db.session
