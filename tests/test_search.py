"""Tests pour la recherche fuzzy des interventions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from app.data.loader import load_rfe_data
from app.data.search import SearchResult, search_interventions
from app.main import app

if TYPE_CHECKING:
    from app.data.models import RFEData


# ---------------------------------------------------------------------------
# Fixture : données réelles du projet
# ---------------------------------------------------------------------------


@pytest.fixture(name="rfe_data")
def _rfe_data() -> RFEData:
    """Charge le vrai fichier data/rfe.json."""
    project_root = Path(__file__).parent.parent
    return load_rfe_data(project_root / "data" / "rfe.json")


@pytest.fixture(name="rfe_data_minimal")
def _rfe_data_minimal(tmp_path) -> RFEData:
    """Données minimales pour les tests unitaires."""
    data = {
        "version": "RFE SFAR 2024",
        "date_extraction": "2026-02-16",
        "specialites": [
            {
                "id": "orthopedie",
                "nom": "Orthopédie",
                "interventions": [
                    {
                        "id": "orthopedie-01",
                        "nom": "Prothèse de hanche",
                        "specialite": "Orthopédie",
                        "protocole": {
                            "molecule": "Céfazoline",
                            "dose_initiale": "2g IVL",
                        },
                        "force_recommandation": "GRADE 1",
                        "source_page": 10,
                        "source_tableau": "Tableau 1",
                    },
                    {
                        "id": "orthopedie-02",
                        "nom": "Prothèse de genou",
                        "specialite": "Orthopédie",
                        "protocole": {
                            "molecule": "Céfazoline",
                            "dose_initiale": "2g IVL",
                        },
                        "force_recommandation": "GRADE 1",
                        "source_page": 11,
                        "source_tableau": "Tableau 1",
                    },
                    {
                        "id": "orthopedie-03",
                        "nom": "Ostéosynthèse",
                        "specialite": "Orthopédie",
                        "protocole": {
                            "molecule": "Céfazoline",
                            "dose_initiale": "2g IVL",
                        },
                        "force_recommandation": "GRADE 2",
                        "source_page": 12,
                        "source_tableau": "Tableau 2",
                    },
                ],
            },
            {
                "id": "digestif",
                "nom": "Chirurgie digestive",
                "interventions": [
                    {
                        "id": "digestif-01",
                        "nom": "Appendicectomie",
                        "specialite": "Chirurgie digestive",
                        "protocole": {
                            "molecule": "Amoxicilline/Clavulanate",
                            "dose_initiale": "2g IVL",
                        },
                        "force_recommandation": "GRADE 1",
                        "source_page": 20,
                        "source_tableau": "Tableau 3",
                    },
                ],
            },
        ],
    }
    json_path = tmp_path / "rfe.json"
    json_path.write_text(json.dumps(data), encoding="utf-8")
    return load_rfe_data(json_path)


# ---------------------------------------------------------------------------
# Tests unitaires — search_interventions
# ---------------------------------------------------------------------------


class TestSearchInterventions:
    """Tests pour la fonction search_interventions."""

    def test_recherche_exacte_retourne_bon_resultat_en_premier(self, rfe_data_minimal):
        """Une recherche exacte retourne le bon résultat en premier."""
        results = search_interventions("Prothèse de hanche", rfe_data_minimal)

        assert len(results) > 0
        assert results[0].intervention.id == "orthopedie-01"

    def test_recherche_fuzzy_tolere_faute_de_frappe(self, rfe_data_minimal):
        """Une faute de frappe tolérée par le matching fuzzy."""
        results = search_interventions("prothese de hanche", rfe_data_minimal)

        assert len(results) > 0
        assert results[0].intervention.id == "orthopedie-01"

    def test_recherche_sans_accent_trouve_avec_accent(self, rfe_data_minimal):
        """Taper sans accent trouve les interventions avec accent."""
        results = search_interventions("prothese", rfe_data_minimal)

        noms = [r.intervention.nom for r in results]
        assert any("Prothèse" in nom for nom in noms)

    def test_recherche_avec_accent_trouve_avec_accent(self, rfe_data_minimal):
        """Taper avec accent fonctionne aussi."""
        results = search_interventions("Prothèse", rfe_data_minimal)

        assert len(results) > 0
        assert results[0].intervention.id == "orthopedie-01"

    def test_recherche_vide_retourne_liste_vide(self, rfe_data_minimal):
        """Une requête vide retourne une liste vide."""
        results = search_interventions("", rfe_data_minimal)

        assert results == []

    def test_limite_max_resultats(self, rfe_data):
        """La recherche retourne au maximum `limit` résultats."""
        results = search_interventions("a", rfe_data, limit=5)

        assert len(results) <= 5

    def test_limite_defaut_est_10(self, rfe_data):
        """La limite par défaut est de 10 résultats."""
        results = search_interventions("e", rfe_data)

        assert len(results) <= 10

    def test_recherche_sans_resultats_retourne_liste_vide(self, rfe_data_minimal):
        """Une recherche sans correspondance retourne une liste vide."""
        results = search_interventions("xyznotfound123", rfe_data_minimal)

        assert results == []

    def test_resultats_tries_par_score_decroissant(self, rfe_data_minimal):
        """Les résultats sont triés par score décroissant."""
        results = search_interventions("prothèse", rfe_data_minimal)

        assert len(results) >= 2
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_resultat_est_searchresult(self, rfe_data_minimal):
        """Les résultats sont des instances de SearchResult."""
        results = search_interventions("hanche", rfe_data_minimal)

        assert len(results) > 0
        for r in results:
            assert isinstance(r, SearchResult)
            assert hasattr(r, "intervention")
            assert hasattr(r, "score")

    def test_recherche_par_specialite(self, rfe_data_minimal):
        """La recherche fonctionne sur le nom de la spécialité."""
        results = search_interventions("digestive", rfe_data_minimal)

        assert len(results) > 0
        # L'appendicectomie (spécialité digestive) doit apparaître
        ids = [r.intervention.id for r in results]
        assert "digestif-01" in ids

    def test_score_entre_0_et_100(self, rfe_data_minimal):
        """Le score est compris entre 0 et 100."""
        results = search_interventions("hanche", rfe_data_minimal)

        for r in results:
            assert 0 <= r.score <= 100

    def test_requete_espaces_seulement_retourne_liste_vide(self, rfe_data_minimal):
        """Une requête composée uniquement d'espaces retourne une liste vide."""
        results = search_interventions("   ", rfe_data_minimal)

        assert results == []


# ---------------------------------------------------------------------------
# Tests d'intégration — endpoint /api/v1/search
# ---------------------------------------------------------------------------


@pytest.fixture(name="client")
def _client():
    """Client de test FastAPI avec données chargées."""
    with TestClient(app) as c:
        yield c


class TestSearchEndpoint:
    """Tests d'intégration pour GET /api/v1/search."""

    def test_recherche_valide_retourne_200(self, client):
        """Une requête valide retourne HTTP 200."""
        response = client.get("/api/v1/search", params={"q": "hanche"})
        assert response.status_code == 200

    def test_retourne_liste_json(self, client):
        """L'endpoint retourne une liste JSON."""
        response = client.get("/api/v1/search", params={"q": "hanche"})
        data = response.json()
        assert isinstance(data, list)

    def test_resultats_contiennent_champs_attendus(self, client):
        """Chaque résultat contient les champs attendus."""
        response = client.get("/api/v1/search", params={"q": "hanche"})
        data = response.json()

        assert len(data) > 0
        first = data[0]
        assert "id" in first
        assert "nom" in first
        assert "specialite" in first
        assert "score" in first

    def test_requete_vide_retourne_liste_vide(self, client):
        """Une requête vide retourne une liste JSON vide."""
        response = client.get("/api/v1/search", params={"q": ""})
        assert response.status_code == 200
        assert response.json() == []

    def test_parametre_q_manquant_retourne_liste_vide(self, client):
        """Sans paramètre q, retourne une liste vide."""
        response = client.get("/api/v1/search")
        assert response.status_code == 200
        assert response.json() == []

    def test_limite_10_resultats_par_defaut(self, client):
        """Par défaut, au maximum 10 résultats."""
        response = client.get("/api/v1/search", params={"q": "a"})
        data = response.json()
        assert len(data) <= 10

    def test_parametre_limit_respecte(self, client):
        """Le paramètre limit est respecté."""
        response = client.get("/api/v1/search", params={"q": "a", "limit": 3})
        data = response.json()
        assert len(data) <= 3


# ---------------------------------------------------------------------------
# Tests _strip_accents
# ---------------------------------------------------------------------------


class TestStripAccents:
    """Tests pour la normalisation unicode."""

    def test_supprime_accent_aigu(self):
        from app.data.search import _strip_accents

        assert _strip_accents("cérasion") == "cerasion"

    def test_supprime_accent_grave(self):
        from app.data.search import _strip_accents

        assert _strip_accents("prothèse") == "prothese"

    def test_majuscules_normalisees(self):
        from app.data.search import _strip_accents

        assert _strip_accents("HÉPATIQUE") == "hepatique"

    def test_sans_accent_inchange(self):
        from app.data.search import _strip_accents

        assert _strip_accents("hanche") == "hanche"


# ---------------------------------------------------------------------------
# Tests _highlight sans accent
# ---------------------------------------------------------------------------


class TestHighlightSansAccent:
    """Tests pour le surlignage insensible aux accents."""

    def test_query_sans_accent_surligne_texte_avec_accent(self):
        from app.web.routes import _highlight

        result = str(_highlight("Prothèse de hanche", "prothese"))
        assert "<mark>Proth" in result
        assert "Proth" in result  # accents préservés dans le texte affiché

    def test_query_avec_accent_surligne_aussi(self):
        from app.web.routes import _highlight

        result = str(_highlight("Prothèse de hanche", "Prothèse"))
        assert "<mark>" in result

    def test_query_vide_retourne_texte_brut(self):
        from app.web.routes import _highlight

        result = str(_highlight("Prothèse de hanche", ""))
        assert "<mark>" not in result
        assert "Prothèse de hanche" in result
