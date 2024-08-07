import json

from src.server.api import Device, DeviceSchema
from src.server.signals import device_created, device_updated


def test_create_device(test_user):
    data = {"active": True, "name": "Pi", "owner_id": test_user.id}
    schema = DeviceSchema()
    device = schema.load(data)


def test_create_device_api(a_client):
    recorded = []

    def record(sender):
        recorded.append(sender)

    device_created.connect(record)

    data = {"name": "my_device", "active": True, "id": 1}
    a_client.get("/api/devices")
    resp = a_client.post(
        "/api/devices/",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    data = resp.get_json()
    assert data["name"] == "my_device"
    assert Device.query.get(data["id"]).name == data["name"]
    assert recorded[0].name == "my_device"


def test_update_device_api(a_client):
    recorded = []

    def record(sender):
        recorded.append(sender)

    device_updated.connect(record)

    data = {
        "name": "my_device",
        "mac": "1ED12DE3F",
        "client_id": "randomhash",
    }
    resp = a_client.post(
        "/api/devices/",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    r_data = resp.get_json()
    data2 = {"name": "updated_name"}
    resp = a_client.put(
        f"/api/devices/{r_data['id']}",
        data=json.dumps(data2),
        headers={"Content-Type": "application/json"},
    )
    r_data2 = resp.get_json()
    assert r_data2["client_id"] == "randomhash"
    assert r_data2["name"] == data2["name"]
    assert recorded[0].id == r_data["id"]
