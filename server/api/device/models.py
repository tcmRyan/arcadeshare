import uuid

from server import db
from server.signals import device_created, device_updated


class Device(db.Model):
    """
    Configuration of the device that has connected to the sever.
    """

    __bind_key__ = "__tenant__"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mac = db.Column(db.String)
    client_id = db.Column(db.String)
    key = db.Column(db.String(80))
    active = db.Column(db.Boolean, default=True)
    owner_id = db.Column(db.Integer)
    feed_id = db.Column(db.Integer, db.ForeignKey("feed.id"))

    def __init__(self, device_name, owner_id, client_id=None, device_key=None):
        self.name = device_name
        self.owner_id = owner_id
        self.client_id = client_id or uuid.uuid4()
        self.key = device_key or uuid.uuid4().hex

    @classmethod
    def find_by_name(cls, device_name):
        return cls.query.filter_by(name=device_name).first()

    @classmethod
    def find_by_clientid(cls, client_id):
        return cls.query.filter_by(client_id=client_id).first()

    @classmethod
    def find_by_key(cls, api_key):
        return cls.query.filter_by(key=api_key).first()

    def save(self):
        exists = self.query.get(self.id)
        db.session.add(self)
        db.session.commit()
        if exists:
            device_updated.send(self)
        else:
            device_created.send(self)
