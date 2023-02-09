from flask import g

from server import db, mqttc
from server.api import Device, DeviceSchema, Feed, FeedSchema
from server.auth import MqttAcl
from server.signals import device_created, device_updated, feed_created, feed_updated


def create_device(device: Device):
    acl = MqttAcl()
    acl.username = device.username
    acl.clientid = device.client_id
    acl.topic = f"/{g.tenant}/devices/{device.client_id}"
    db.session.add(acl)
    db.session.commit()
    schema = DeviceSchema()
    mqttc.publish(acl.topic, schema.dump(device))


def update_device(device: Device):
    topic = f"/{g.tenant}/devices/{device.client_id}"
    schema = DeviceSchema()
    mqttc.publish(topic, schema.dump(device))


def create_feed(feed: Feed):
    topic = f"/{g.tenant}/devices/{feed.client_id}"
    schema = FeedSchema()
    mqttc.publish(topic, schema.dump(feed))


def update_feed(feed: Feed):
    topic = f"/{g.tenant}/devices/{feed.client_id}"
    schema = FeedSchema()
    mqttc.publish(topic, schema.dump(feed))


device_created.connect(create_device)
device_updated.connect(update_device)
feed_created.connect(create_feed)
feed_updated.connect(update_feed)
