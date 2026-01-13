import pytest
from fastapi.testclient import TestClient

from app import app


def test_read_root():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data and data["status"] == "ok"
