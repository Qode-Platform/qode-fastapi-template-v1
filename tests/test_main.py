from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_create_and_read_item():
    created = client.post("/items", json={"name": "widget", "price": 9.5})
    assert created.status_code == 201
    item_id = created.json()["id"]
    assert client.get(f"/items/{item_id}").json()["name"] == "widget"


def test_missing_item_is_404():
    assert client.get("/items/999999").status_code == 404
