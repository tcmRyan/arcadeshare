from server import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.BLOB)
    storage_slug = db.Column(db.String)
    played = db.Column(db.Integer)
