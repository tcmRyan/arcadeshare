from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import current_user
from flask_restx import Namespace, Resource

from server.api import DeviceSchema, Device
from server.utils.decorators import tenant_context

ns = Namespace("devices", "Devices for this organization", decorators=[cross_origin()])


@ns.route("/")
class DevicesResource(Resource):
    method_decorators = [tenant_context, jwt_required()]

    def get(self):
        schema = DeviceSchema(many=True)
        return schema.load(Device.query.all())

    def post(self):
        data = request.get_json()
        schema = DeviceSchema()
        device = Device(device_name=data["name"], owner_id=current_user.id)
        device = schema.load(data, instance=device)
        device.save()
        return schema.dump(device), 201


@ns.route("/<int:did>")
class DeviceResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self, did):
        schema = DeviceSchema()
        return schema.load(Device.query.get(did))

    def put(self, did):
        schema = DeviceSchema()
        data = request.get_json()
        updated = schema.load(data, instance=Device.query.get(did))
        updated.save()
        return schema.dump(updated)
