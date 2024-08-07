from src.server import db
from src.server.signals import feed_created, feed_updated
from src.server.api.game.models import Game

feed_games = db.Table(
    "feed_games",
    db.Column("game_id", db.Integer(), db.ForeignKey(Game.id), primary_key=True),
    info={"bind_key": "__tenant__"},
)


class Feed(db.Model):
    """
    A collection of games that can be subscribed to.  This collection of games will appear in the game menu.
    """

    __bind_key__ = "__tenant__"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    games = db.relationship(
        "Game",
        secondary=feed_games,
        lazy="subquery",
        backref=db.backref("feeds", lazy="dynamic"),
    )
    description = db.Column(db.String)
    owner_id = db.Column(db.Integer)
    devices = db.relationship("Device", backref="feed", lazy=True)

    def save(self):
        exists = self.query.get(self.id)
        db.session.add(self)
        db.session.commit()
        if exists:
            feed_updated.send(self)
        else:
            feed_created.send(self)


feed_games.append_column(db.Column("feed_id", db.Integer(), db.ForeignKey(Feed.id), primary_key=True))
