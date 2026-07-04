"""Tests for FastAPI server."""

import pytest
from fastapi.testclient import TestClient

from starwatch.server.app import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestHealth:
    def test_health(self, client: TestClient):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestStatus:
    def test_status(self, client: TestClient):
        r = client.get("/status")
        assert r.status_code == 200
        data = r.json()
        assert "connected" in data
        assert "parked" in data


class TestSlew:
    def test_slew_m31(self, client: TestClient):
        client.post("/unpark")
        r = client.post("/slew", json={"target": "M31"})
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert data["ra_hours"] == pytest.approx(0.712)

    def test_slew_while_parked(self, client: TestClient):
        client.post("/park")
        r = client.post("/slew", json={"target": "M31"})
        assert r.status_code == 400
        assert "parked" in r.json()["detail"].lower()

    def test_unknown_target(self, client: TestClient):
        client.post("/unpark")
        r = client.post("/slew", json={"target": "FAKE_OBJECT_XYZ"})
        assert r.status_code == 400


class TestPark:
    def test_park_unpark(self, client: TestClient):
        client.post("/unpark")
        r = client.post("/park")
        assert r.status_code == 200
        status = client.get("/status").json()
        assert status["parked"] is True