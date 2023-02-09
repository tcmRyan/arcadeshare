from flask_marshmallow import Schema
from marshmallow.fields import String


class LoginFormSchema(Schema):

    username = String()
    password = String()

