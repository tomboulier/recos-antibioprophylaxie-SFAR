"""Tests TDD — endpoints GET /api/v1/specialites."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


def test_get_specialites_retourne_200(client):
    """GET /api/v1/specialites retourne un statut 200."""
    response = client.get("/api/v1/specialites")
    assert response.status_code == 200


def test_get_specialites_liste_non_vide(client):
    """GET /api/v1/specialites retourne une liste non vide."""
    response = client.get("/api/v1/specialites")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_specialites_structure_item(client):
    """Chaque spécialité contient id et nom."""
    response = client.get("/api/v1/specialites")
    specialites = response.json()
    first = specialites[0]
    assert "id" in first
    assert "nom" in first


def test_get_specialite_par_id_retourne_200(client):
    """GET /api/v1/specialites/{id} retourne 200 pour un id valide."""
    specialites = client.get("/api/v1/specialites").json()
    first_id = specialites[0]["id"]

    response = client.get(f"/api/v1/specialites/{first_id}")
    assert response.status_code == 200


def test_get_specialite_par_id_contient_interventions(client):
    """GET /api/v1/specialites/{id} retourne les interventions associées."""
    specialites = client.get("/api/v1/specialites").json()
    first_id = specialites[0]["id"]

    response = client.get(f"/api/v1/specialites/{first_id}")
    data = response.json()
    assert "interventions" in data
    assert isinstance(data["interventions"], list)
    assert len(data["interventions"]) > 0


def test_get_specialite_par_id_structure_complete(client):
    """GET /api/v1/specialites/{id} retourne tous les champs attendus."""
    specialites = client.get("/api/v1/specialites").json()
    first_id = specialites[0]["id"]

    response = client.get(f"/api/v1/specialites/{first_id}")
    data = response.json()
    assert "id" in data
    assert "nom" in data
    assert "interventions" in data


def test_get_specialite_inexistante_retourne_404(client):
    """GET /api/v1/specialites/inexistant retourne 404."""
    response = client.get("/api/v1/specialites/specialite-qui-nexiste-pas")
    assert response.status_code == 404


def test_get_specialite_inexistante_message_erreur(client):
    """GET /api/v1/specialites/inexistant contient un message d'erreur."""
    response = client.get("/api/v1/specialites/specialite-qui-nexiste-pas")
    data = response.json()
    assert "detail" in data
