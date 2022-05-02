from flask_apispec import Ref, marshal_with, MethodResource
from flask_restx import Api


@marshal_with(Ref('schema'))
class BaseResource(MethodResource):

    schema = None

# Model Import


# Schema Import
from .schemas import *

# API Import
from .user.api import ns as user_ns

api = Api(
    title="Arcade",
    version="0.0.1",
    description="Share Makecode Arcade Games",
    prefix="/api",
    doc="/docs"
)

api.add_namespace(user_ns)

