"""Tests pour l'endpoint HTMX /search (suggestions dropdown)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


class TestSearchEndpoint:
    """Tests sur le rendu HTML du dropdown de suggestions."""

    def test_retourne_html_vide_si_requete_vide(self, client):
        """Pas de résultats si la requête est vide."""
        resp = client.get("/search", params={"q": ""})
        assert resp.status_code == 200
        assert "search-results__item" not in resp.text

    def test_retourne_resultats_pour_requete_valide(self, client):
        """Une requête valide retourne au moins un lien de protocole."""
        resp = client.get("/search", params={"q": "hanche"})
        assert resp.status_code == 200
        assert "/protocole/" in resp.text

    def test_limite_a_3_suggestions(self, client):
        """Le dropdown ne doit pas dépasser 3 liens de protocole."""
        resp = client.get("/search", params={"q": "chirurgie"})
        assert resp.status_code == 200
        protocole_links = resp.text.count("/protocole/")
        assert protocole_links <= 3

    def test_lien_voir_tous_present_si_has_more(self, client):
        """Le lien 'Voir tous les résultats' apparaît si plus de 3 résultats existent."""
        # "proth" matche Prothèse de hanche/genou, vasculaire, etc. → garantiement > 3
        resp = client.get("/search", params={"q": "proth"})
        assert resp.status_code == 200
        assert resp.text.count("/protocole/") == 3  # exactement 3 affichés
        assert "/recherche?q=" in resp.text  # lien "Voir tous" présent

    def test_pas_de_lien_voir_tous_si_peu_de_resultats(self, client):
        """Pas de lien 'Voir tous' si moins de 3 résultats."""
        # Requête très spécifique → 1 seul résultat attendu
        resp = client.get("/search", params={"q": "cœlioscopie"})
        assert resp.status_code == 200
        if resp.text.count("/protocole/") < 3:
            assert "Voir tous" not in resp.text
