from http import HTTPStatus
import os

from flask import request, redirect, current_app
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_login import current_user
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename

from server import db
from server.api import GameSchema, Game
from server.utils.decorators import tenant_context

ns = Namespace("games", description="All Games", decorators=[cross_origin()])

ALLOWED_EXTENSIONS = [".uf2"]
ALLOWED_THUMB_EXTENSIONS = [".png", ".svg", ".jpg", ".jpeg"]


@ns.route("/")
class GamesResource(Resource):
    schema = GameSchema
    decorators = [tenant_context, jwt_required()]

    def get(self):
        schema = GameSchema(many=True)
        return schema.dump(Game.query.all())

    def post(self):
        data = request.form.to_dict()
        schema = GameSchema()
        file = request.files["upload"]
        thumbnail = request.files["thumbnail"]
        new_game = schema.load(data)
        current_app.logger.info("Received request %s", new_game.name)
        ext = os.path.splitext(file.filename)[1]
        if os.path.splitext(thumbnail.filename)[1] in ALLOWED_THUMB_EXTENSIONS:
            filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join(current_app.config["TEMP_FILES"], filename))
            new_game.save_thumbnail(thumbnail, current_user)
        else:
            return HTTPStatus.BAD_REQUEST
        if ext in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["TEMP_FILES"], filename))
            new_game.upload_game(file, current_user)
        else:
            return HTTPStatus.BAD_REQUEST
        current_app.logger.info("Created game %s", new_game.name)
        new_game.save(new=True)

        return schema.dump(new_game)


@ns.route("/<int:gid>")
class GameResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self, gid):
        schema = GameSchema()
        game = Game.query.get(gid)
        return schema.dump(game)

    def put(self, gid):
        data = request.form.to_dict()
        schema = GameSchema()
        game = Game.query.get(gid)
        file = request.files.get("upload")
        thumbnail = request.files.get("thumbnail")
        updated_game = schema.load(data, instance=game)

        if thumbnail:
            if os.path.splitext(thumbnail.filename)[1] in ALLOWED_THUMB_EXTENSIONS:
                filename = secure_filename(thumbnail.filename)
                thumbnail.save(os.path.join(current_app.config["TEMP_FILES"], filename))
                updated_game.save_thumbnail(thumbnail, current_user)
            else:
                return HTTPStatus.BAD_REQUEST
        if file:
            if os.path.splitext(file.filename)[1] in ALLOWED_EXTENSIONS:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["TEMP_FILES"], filename))
                updated_game.upload_game(file, current_user)
            else:
                return HTTPStatus.BAD_REQUEST

        updated_game.save()
        return schema.dump(updated_game), 201


@ns.route("/<int:gid>/download")
class GameDownloadResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self, gid):
        game = Game.query.get(gid)
        return redirect(game.download_redirect())


@ns.route("/search")
class GameSearchResource(Resource):
    decorators = [tenant_context, jwt_required()]

    def get(self):
        params = request.args
        results = Game.query.filter(Game.name.like("%" + params.get("query") + "%")).all()
        schema = GameSchema(many=True)
        return schema.dump(results)
