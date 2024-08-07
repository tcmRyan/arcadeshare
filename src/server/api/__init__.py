from flask_apispec import Ref, marshal_with, MethodResource
from flask_restx import Api

# Model Import
from .game.models import *
from .device.models import *
from .feed.models import *

# Schema Import
from .schemas import *

# API Import
from .user.api import ns as user_ns
from .role.api import ns as role_ns
from .device.api import ns as device_ns
from .game.api import ns as game_ns
from .feed.api import ns as feed_ns


@marshal_with(Ref('schema'))
class BaseResource(MethodResource):
    schema = None


api = Api(
    title="Arcade",
    version="0.0.1",
    description="Share Makecode Arcade Games",
    prefix="/api",
    doc="/docs"
)

api.add_namespace(user_ns)
api.add_namespace(role_ns)
api.add_namespace(device_ns)
api.add_namespace(game_ns)
api.add_namespace(feed_ns)
