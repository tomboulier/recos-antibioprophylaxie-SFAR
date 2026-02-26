"""Tests pour S-010 : Layout de base — templates Jinja2, header, footer, CSS tokens."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


# ---------- Page d'accueil existe et rend du HTML ----------


def test_accueil_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ---------- HTML sémantique : header, main, footer ----------


def test_accueil_contient_structure_semantique(client):
    html = client.get("/").text
    assert "<header" in html
    assert "<main" in html
    assert "<footer" in html


def test_accueil_a_un_seul_h1(client):
    html = client.get("/").text
    assert html.count("<h1") == 1


# ---------- Header : navigation ----------


def test_header_contient_navigation(client):
    html = client.get("/").text
    assert "<nav" in html


def test_header_contient_nom_app(client):
    html = client.get("/").text
    assert "Antibioprophylaxie" in html


# ---------- Footer : disclaimer ----------


def test_footer_contient_disclaimer(client):
    html = client.get("/").text
    assert "Ne remplace pas le jugement clinique" in html or (
        "ne se substitue pas au jugement clinique" in html.lower()
    )


def test_footer_contient_source_sfar(client):
    html = client.get("/").text
    assert "RFE SFAR 2024" in html


# ---------- CSS design tokens ----------


def test_css_tokens_accessible(client):
    response = client.get("/static/css/tokens.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_css_tokens_contient_couleurs_sfar(client):
    css = client.get("/static/css/tokens.css").text
    assert "#273466" in css  # primaire
    assert "#0cc9bf" in css  # accent
    assert "#f15c40" in css  # warning/allergie


def test_css_tokens_contient_variables_custom(client):
    css = client.get("/static/css/tokens.css").text
    assert "--color-primary" in css
    assert "--color-accent" in css
    assert "--font-family" in css
    assert "--space-" in css


def test_css_tokens_contient_breakpoints(client):
    css = client.get("/static/css/tokens.css").text
    assert "768px" in css
    assert "1024px" in css


# ---------- CSS layout ----------


def test_css_layout_accessible(client):
    response = client.get("/static/css/layout.css")
    assert response.status_code == 200


# ---------- HTMX inclus ----------


def test_htmx_inclus(client):
    html = client.get("/").text
    assert "htmx" in html.lower()


# ---------- Meta viewport (mobile-first) ----------


def test_meta_viewport_present(client):
    html = client.get("/").text
    assert 'name="viewport"' in html


def test_html_lang_fr(client):
    html = client.get("/").text
    assert 'lang="fr"' in html


# ---------- Page 404 personnalisée ----------


def test_404_renvoie_html(client):
    response = client.get("/page-inexistante")
    assert response.status_code == 404
    assert "text/html" in response.headers["content-type"]


def test_404_contient_layout(client):
    html = client.get("/page-inexistante").text
    assert "<header" in html
    assert "<footer" in html
    assert "Antibioprophylaxie" in html


def test_404_contient_message(client):
    html = client.get("/page-inexistante").text
    assert "introuvable" in html.lower() or "404" in html
