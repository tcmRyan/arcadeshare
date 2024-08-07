from flask import g, current_app

from src import mqtt
from src.server.api import Device, DeviceSchema, Feed, FeedSchema, Game, GameSchema
from src.auth import Tenant


def update_device(device: Device):
    tenant = Tenant.query.filter_by(name=g.tenant).first()

    topic = f"{tenant.id}/devices/update"
    schema = DeviceSchema()
    mqtt.publish(topic, schema.dumps(device))


def update_feed(feed: Feed):
    tenant = Tenant.query.filter_by(name=g.tenant).first()
    topic = f"{tenant.id}/feeds/updated"
    schema = FeedSchema()
    current_app.logger.info(f"Publishing update for feed: {feed.id} to {topic}")
    mqtt.publish(topic, schema.dumps(feed))


def update_game(game: Game):
    topic = f"/{g.tenant}/games/update"
    schema = GameSchema()
    mqtt.publish(topic, schema.dumps(game))
