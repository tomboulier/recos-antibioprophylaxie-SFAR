"""Tests TDD — endpoints GET /api/v1/interventions."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


def test_get_interventions_retourne_200(client):
    """GET /api/v1/interventions retourne un statut 200."""
    response = client.get("/api/v1/interventions")
    assert response.status_code == 200


def test_get_interventions_liste_non_vide(client):
    """GET /api/v1/interventions retourne une liste non vide."""
    response = client.get("/api/v1/interventions")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_interventions_structure_item(client):
    """Chaque intervention contient les champs essentiels."""
    response = client.get("/api/v1/interventions")
    interventions = response.json()
    first = interventions[0]
    assert "id" in first
    assert "nom" in first
    assert "specialite" in first
    assert "force_recommandation" in first


def test_get_interventions_pagination_limit(client):
    """GET /api/v1/interventions?limit=5 retourne au plus 5 résultats."""
    response = client.get("/api/v1/interventions?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5


def test_get_interventions_pagination_skip(client):
    """GET /api/v1/interventions?skip=1 saute le premier élément."""
    all_items = client.get("/api/v1/interventions").json()
    skipped_items = client.get("/api/v1/interventions?skip=1").json()

    if len(all_items) > 1:
        assert skipped_items[0]["id"] == all_items[1]["id"]


def test_get_interventions_pagination_skip_et_limit(client):
    """GET /api/v1/interventions?skip=0&limit=50 fonctionne correctement."""
    response = client.get("/api/v1/interventions?skip=0&limit=50")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 50


def test_get_intervention_par_id_retourne_200(client):
    """GET /api/v1/interventions/{id} retourne 200 pour un id valide."""
    interventions = client.get("/api/v1/interventions").json()
    first_id = interventions[0]["id"]

    response = client.get(f"/api/v1/interventions/{first_id}")
    assert response.status_code == 200


def test_get_intervention_par_id_detail_complet(client):
    """GET /api/v1/interventions/{id} retourne tous les champs."""
    interventions = client.get("/api/v1/interventions").json()
    first_id = interventions[0]["id"]

    response = client.get(f"/api/v1/interventions/{first_id}")
    data = response.json()
    assert "id" in data
    assert "nom" in data
    assert "specialite" in data
    assert "force_recommandation" in data
    assert "source_page" in data
    assert "source_tableau" in data


def test_get_intervention_inexistante_retourne_404(client):
    """GET /api/v1/interventions/inexistant retourne 404."""
    response = client.get("/api/v1/interventions/intervention-qui-nexiste-pas")
    assert response.status_code == 404


def test_get_intervention_inexistante_message_erreur(client):
    """GET /api/v1/interventions/inexistant contient un message d'erreur."""
    response = client.get("/api/v1/interventions/intervention-qui-nexiste-pas")
    data = response.json()
    assert "detail" in data


def test_get_interventions_limit_defaut(client):
    """GET /api/v1/interventions sans paramètres retourne 50 interventions max par défaut."""
    response = client.get("/api/v1/interventions")
    data = response.json()
    assert len(data) <= 50
