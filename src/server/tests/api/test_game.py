import json

from src.server.api import Game
from src.server.signals import game_created, game_updated


def test_create_game_api(a_client):
    recorded = []

    def record(sender):
        recorded.append(sender)

    game_created.connect(record)

    data = {
        "name": "my_game",
        "description": "fight, score, win",
        "storage_slug": "path/to/file",
        "version": "some.version"
    }

    resp = a_client.post(
        "/api/games/",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    r_data = resp.get_json()
    assert r_data["name"] == "my_game"
    assert Game.query.get(r_data["id"]).description == data["description"]
    assert recorded[0].name == data["name"]


def test_update_game_api(a_client):
    recorded = []

    def record(sender):
        recorded.append(sender)

    game_updated.connect(record)

    game1 = Game()
    game1.name = "updated"
    game1.description = "test sage"
    game1.storage_slug = "some/path"
    game1.version = "1.2"
    game1.save()

    resp = a_client.put(f"/api/games/{game1.id}", data=json.dumps({"name": "new name", "version": "1.3"}),
                        headers={"Content-Type": "application/json"})
    r_data = resp.get_json()
    assert r_data["name"] == "new name"
    assert Game.query.get(r_data["id"]).version == "1.3"
    assert recorded[0].name == "new name"
