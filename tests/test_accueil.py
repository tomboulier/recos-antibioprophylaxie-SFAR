"""Tests pour S-011 : Écran d'accueil — héros, recherche, grille spécialités."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(name="html")
def _html(client):
    """HTML de la page d'accueil, réutilisé par plusieurs tests."""
    return client.get("/").text


# ---------- Section héros ----------


def test_hero_contient_titre(html):
    """Le H1 doit mentionner l'antibioprophylaxie pour identifier l'app."""
    assert "<h1" in html
    assert "antibioprophylaxie" in html.lower()


def test_hero_contient_barre_recherche(html):
    """La barre de recherche doit être présente, même si pas encore fonctionnelle."""
    assert 'type="search"' in html or 'class="search' in html.lower()


def test_barre_recherche_a_placeholder(html):
    """Le placeholder guide l'utilisateur sur quoi chercher."""
    assert "placeholder=" in html.lower()


def test_barre_recherche_a_autofocus(html):
    """L'autofocus place le curseur directement dans la barre de recherche."""
    assert "autofocus" in html.lower()


# ---------- Grille des spécialités ----------


def test_grille_specialites_presente(html):
    """La section spécialités doit exister sur la page d'accueil."""
    assert "spécialité" in html.lower() or "specialite" in html.lower()


def test_grille_affiche_toutes_les_specialites(html):
    """Chaque spécialité du JSON doit apparaître sur la page."""
    assert "Chirurgie orthopédique programmée" in html
    assert "Chirurgie orthopédique traumatologique" in html


def test_grille_affiche_nombre_interventions(html):
    """Le nombre d'interventions par spécialité aide l'utilisateur à évaluer le contenu."""
    # 30 interventions en ortho programmée, 17 en trauma
    assert "30" in html
    assert "17" in html


def test_specialites_sont_des_liens(html):
    """Les cartes spécialités doivent être cliquables (liens vers la page spécialité)."""
    assert "chirurgie-orthopedique-programmee" in html
    assert "chirurgie-orthopedique-traumatologique" in html


# ---------- CSS accueil ----------


def test_css_accueil_accessible(client):
    """Le fichier accueil.css doit être servi pour le style de la page d'accueil."""
    response = client.get("/static/css/accueil.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_css_accueil_contient_hero(client):
    """Le CSS doit définir la section héros."""
    css = client.get("/static/css/accueil.css").text
    assert ".hero" in css


def test_css_accueil_contient_grille(client):
    """Le CSS doit définir la grille responsive des spécialités."""
    css = client.get("/static/css/accueil.css").text
    assert ".specialty" in css.lower() or ".specialite" in css.lower()
