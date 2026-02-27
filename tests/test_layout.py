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
    """GET / doit retourner 200 avec du HTML (pas du JSON)."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ---------- HTML sémantique : header, main, footer ----------


def test_accueil_contient_structure_semantique(client):
    """Le HTML doit contenir header, main et footer pour le SEO et l'accessibilité."""
    html = client.get("/").text
    assert "<header" in html
    assert "<main" in html
    assert "<footer" in html


def test_accueil_a_un_seul_h1(client):
    """Un seul H1 par page, requis pour l'accessibilité et le SEO."""
    html = client.get("/").text
    assert html.count("<h1") == 1


# ---------- Header : navigation ----------


def test_header_contient_navigation(client):
    """Le header doit inclure une balise nav pour la navigation principale."""
    html = client.get("/").text
    assert "<nav" in html


def test_header_contient_nom_app(client):
    """Le nom de l'application doit apparaître dans la page (branding)."""
    html = client.get("/").text
    assert "Antibioprophylaxie" in html


# ---------- Footer : disclaimer ----------


def test_footer_contient_disclaimer(client):
    """Le disclaimer médico-légal doit être présent sur chaque page."""
    html = client.get("/").text
    assert "Ne remplace pas le jugement clinique" in html or (
        "ne se substitue pas au jugement clinique" in html.lower()
    )


def test_footer_contient_source_sfar(client):
    """La source RFE SFAR 2024 doit être citée pour la traçabilité."""
    html = client.get("/").text
    assert "RFE SFAR 2024" in html


# ---------- CSS design tokens ----------


def test_css_tokens_accessible(client):
    """Le fichier tokens.css doit être servi correctement en statique."""
    response = client.get("/static/css/tokens.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_css_tokens_contient_couleurs_sfar(client):
    """Les 3 couleurs de la charte SFAR doivent être définies dans les tokens."""
    css = client.get("/static/css/tokens.css").text
    assert "#273466" in css  # primaire
    assert "#0cc9bf" in css  # accent
    assert "#f15c40" in css  # warning/allergie


def test_css_tokens_contient_variables_custom(client):
    """Les variables CSS (couleurs, typo, espacement) doivent exister pour le design system."""
    css = client.get("/static/css/tokens.css").text
    assert "--color-primary" in css
    assert "--color-accent" in css
    assert "--font-family" in css
    assert "--space-" in css


def test_css_tokens_contient_breakpoints(client):
    """Les breakpoints mobile-first (768px tablet, 1024px desktop) doivent être définis."""
    css = client.get("/static/css/tokens.css").text
    assert "768px" in css
    assert "1024px" in css


# ---------- CSS layout ----------


def test_css_layout_accessible(client):
    """Le fichier layout.css doit être servi correctement en statique."""
    response = client.get("/static/css/layout.css")
    assert response.status_code == 200


# ---------- HTMX inclus ----------


def test_htmx_inclus(client):
    """HTMX doit être chargé via un script local (pas de CDN) pour les interactions."""
    html = client.get("/").text
    assert "/static/js/htmx.min.js" in html


# ---------- Meta viewport (mobile-first) ----------


def test_meta_viewport_present(client):
    """Le meta viewport est requis pour le rendu mobile-first (évite le zoom iOS)."""
    html = client.get("/").text
    assert 'name="viewport"' in html


def test_html_lang_fr(client):
    """La langue doit être déclarée en français pour l'accessibilité (lecteurs d'écran)."""
    html = client.get("/").text
    assert 'lang="fr"' in html


# ---------- Page 404 personnalisée ----------


def test_404_renvoie_html(client):
    """Une route inexistante doit retourner du HTML (pas le JSON par défaut de FastAPI)."""
    response = client.get("/page-inexistante")
    assert response.status_code == 404
    assert "text/html" in response.headers["content-type"]


def test_404_contient_layout(client):
    """La page 404 doit utiliser le même layout (header, footer) pour rester cohérente."""
    html = client.get("/page-inexistante").text
    assert "<header" in html
    assert "<footer" in html
    assert "Antibioprophylaxie" in html


def test_404_contient_message(client):
    """La page 404 doit afficher un message clair pour l'utilisateur."""
    html = client.get("/page-inexistante").text
    assert "introuvable" in html.lower() or "404" in html
