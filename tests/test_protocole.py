"""Tests pour S-012 : Écran protocole — détail intervention."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


# --- ID utilisé dans les tests : PTH (protocole + allergie + notes) ---
INTERVENTION_ID = "ortho-prog-mi-prothese-hanche-genou"

# --- ID sans antibioprophylaxie ---
INTERVENTION_SANS_ABP = "ortho-prog-mi-arthroscopie-sans-materiel"


@pytest.fixture(name="html")
def _html(client):
    """HTML de la page protocole pour la PTH."""
    return client.get(f"/protocole/{INTERVENTION_ID}").text


@pytest.fixture(name="html_sans_abp")
def _html_sans_abp(client):
    """HTML de la page protocole pour une intervention sans ABP."""
    return client.get(f"/protocole/{INTERVENTION_SANS_ABP}").text


# ---------- Route et HTTP ----------


def test_protocole_route_retourne_200(client):
    """La route /protocole/{id} doit retourner 200 pour un ID valide."""
    response = client.get(f"/protocole/{INTERVENTION_ID}")
    assert response.status_code == 200


def test_protocole_id_inconnu_retourne_404(client):
    """Un ID d'intervention inconnu doit retourner 404."""
    response = client.get("/protocole/intervention-inexistante")
    assert response.status_code == 404


# ---------- Contenu principal ----------


def test_protocole_contient_nom_intervention(html):
    """Le H1 doit contenir le nom de l'intervention."""
    assert "Prothèse de hanche ou de genou" in html


def test_protocole_contient_molecule_principale(html):
    """La molécule principale (Céfazoline) doit apparaître bien visible."""
    assert "Céfazoline" in html


def test_protocole_contient_dose(html):
    """La posologie doit être affichée."""
    assert "2g IVL" in html


def test_protocole_contient_reinjection(html):
    """Les consignes de réinjection doivent apparaître."""
    lower_html = html.lower()
    assert ("réinjection" in lower_html or "reinjection" in lower_html) and "4h" in lower_html


def test_protocole_contient_duree(html):
    """La durée doit être affichée."""
    assert "durée" in html.lower() or "duree" in html.lower()


# ---------- Bloc allergie ----------


def test_protocole_contient_bloc_allergie(html):
    """Le bloc allergie doit être présent quand des alternatives existent."""
    assert "allergie" in html.lower()


def test_protocole_allergie_contient_molecules(html):
    """Les molécules alternatives (allergie) doivent être listées."""
    assert "Clindamycine" in html
    assert "Vancomycine" in html


def test_protocole_allergie_contient_intentions(html):
    """Les intentions (1ère, 2ème…) doivent apparaître pour les alternatives."""
    assert "intention" in html.lower()


# ---------- Source ----------


def test_protocole_contient_source(html):
    """La source (page PDF, tableau) doit être affichée."""
    assert "73" in html  # source_page
    assert "Tableau" in html  # source_tableau


def test_protocole_contient_force_recommandation(html):
    """La force de la recommandation doit être mentionnée."""
    assert "Avis d" in html and "experts" in html


# ---------- Notes ----------


def test_protocole_contient_notes(html):
    """Les notes cliniques doivent être affichées quand elles existent."""
    assert "voie antérieure" in html


# ---------- Breadcrumb ----------


def test_protocole_contient_breadcrumb(html):
    """Le breadcrumb doit contenir la spécialité et l'intervention."""
    assert "Chirurgie orthopédique programmée" in html
    assert 'class="breadcrumb"' in html


def test_breadcrumb_contient_lien_specialite(html):
    """Le breadcrumb doit avoir un lien vers la page spécialité."""
    assert "chirurgie-orthopedique-programmee" in html


# ---------- Cas « pas d'antibioprophylaxie » ----------


def test_pas_abp_retourne_200(client):
    """Une intervention sans ABP doit retourner 200 (pas une erreur)."""
    response = client.get(f"/protocole/{INTERVENTION_SANS_ABP}")
    assert response.status_code == 200


def test_pas_abp_affiche_message_clair(html_sans_abp):
    """Quand pas d'ABP, afficher un message clair (pas un protocole vide)."""
    text = html_sans_abp.lower()
    assert "pas d'antibioprophylaxie" in text


# ---------- CSS ----------


def test_css_protocole_accessible(client):
    """Le fichier protocole.css doit être servi."""
    response = client.get("/static/css/protocole.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_css_contient_protocol_card(client):
    """Le CSS doit définir le composant ProtocolCard."""
    css = client.get("/static/css/protocole.css").text
    assert ".protocol-card" in css


def test_css_contient_bloc_allergie(client):
    """Le CSS doit définir le style du bloc allergie."""
    css = client.get("/static/css/protocole.css").text
    assert "allergie" in css.lower() or "warning" in css.lower()
