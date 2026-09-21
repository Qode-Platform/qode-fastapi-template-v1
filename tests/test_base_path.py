"""BASE_PATH is read at import time, so each mode needs a fresh module."""

import importlib

from fastapi.testclient import TestClient


def _app(monkeypatch, value: str | None):
    if value is None:
        monkeypatch.delenv("BASE_PATH", raising=False)
    else:
        monkeypatch.setenv("BASE_PATH", value)
    import app.main as main

    return importlib.reload(main).app


def test_serves_at_root_when_unset(monkeypatch):
    client = TestClient(_app(monkeypatch, None))
    assert client.get("/healthz").status_code == 200


def test_serves_under_prefix(monkeypatch):
    client = TestClient(_app(monkeypatch, "/direct/agent-7:3000"))
    assert client.get("/direct/agent-7:3000/healthz").status_code == 200
    assert client.get("/healthz").status_code == 404


def test_prefix_is_normalised(monkeypatch):
    client = TestClient(_app(monkeypatch, "direct/agent-7:3000/"))
    assert client.get("/direct/agent-7:3000/healthz").status_code == 200
