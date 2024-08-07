from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from flask import request

from src.server.api import TenantSchema
from src.server.auth.models import Tenant
from .. import BaseResource

ns = Namespace("tenants", description="Tenant for a given organization", decorators=[cross_origin()])


@ns.route("/<int:tid>")
class TenantResource(BaseResource, Resource):
    schema = TenantSchema
    decorators = [jwt_required()]

    def get(self, tid):
        schema = TenantSchema()
        schema.dump(Tenant.query.get(tid))

    def put(self, tid):
        schema = TenantSchema()
        tenant = Tenant.query.get(tid)

        return schema.dump(tenant)


@ns.route("/")
class TenantsResource(BaseResource, Resource):
    schema = TenantSchema(many=True)

    def get(self):
        schema = TenantSchema(many=True)
        return schema.dump(Tenant.query.all())

    def post(self):
        schema = TenantSchema()
        data = request.get_json()
        tenant = schema.load(data)
        for user in tenant.users:
            user.save()
        tenant.save()
        return schema.dump(tenant)
