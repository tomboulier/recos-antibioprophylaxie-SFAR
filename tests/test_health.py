"""Tests pour le health check endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


def test_health_returns_ok(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "data_version" in data


def test_health_contient_statistiques(client):
    response = client.get("/api/v1/health")
    data = response.json()
    assert data["specialites"] >= 2
    assert data["interventions"] >= 40
