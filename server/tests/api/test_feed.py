import json

from server.api import Feed
from server.signals import feed_created, feed_updated


def test_create_feed_api(a_client):
    recorded = []

    def record(sender):
        recorded.append(sender)

    feed_created.connect(record)

    game1 = {
        "id": "1",
        "name": "Game 1",
        "description": "Best game eva",
        "storage_slug": "some path",
        "version": "1234"
    }

    game2 = {
        "id": "2",
        "name": "Game 2",
        "description": "2nd Best game eva",
        "storage_slug": "some other path",
        "version": "12345"
    }

    feed_data = {
        "name": "Game Feed 1",
        "games": [game1, game2],
        "owner_id": 2,
    }

    resp = a_client.post("/api/feeds/", data=json.dumps(feed_data), headers={"Content-Type": "application/json"})
    data = resp.get_json()
    assert data["name"] == "Game Feed 1"
    assert Feed.query.get(data["id"]).name == feed_data["name"]
    assert recorded[0].name == "Game Feed 1"
