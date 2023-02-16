from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from server.api import FeedSchema, Feed
from server.utils.decorators import tenant_context

ns = Namespace("feeds", "A collection of games to be shown in the arcade menu", decorators=[cross_origin()])


@ns.route("/")
class FeedsResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self):
        schema = FeedSchema(many=True)
        feeds = Feed.query.all()
        return schema.dump(feeds)

    def post(self):
        schema = FeedSchema()
        data = request.get_json()
        feed = schema.load(data)
        feed.save()
        return schema.dump(feed)


@ns.route("/<int:fid>")
class FeedResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self, fid):
        schema = FeedSchema()
        feed = Feed.query.get(fid)
        return schema.dump(feed)

    def put(self, fid):
        schema = FeedSchema()
        data = request.get_json()
        updated = schema.load(data, instance=Feed.query.get(fid))
        updated.save()

        return schema.dump(updated)
