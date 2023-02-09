import json

from flask import current_app, g
from .. import mqttc
from ..api import GameSchema


def game_created_pub(game):
    current_app.logger.info("publishing changes to %s", game.name)
    tenant = g.get("tenant")
    if tenant is not None:
        topic = f"{tenant}/game-created"
        payload = GameSchema().dump(game)
        mqttc.publish(topic, payload=json.dumps(payload), qos=0, retain=False)
    else:
        current_app.logger.error("No tenant found in global context")


def game_updated_pub(game):
    current_app.logger.info("publishing changes to %s", game.name)
