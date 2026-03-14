"""Tests pour S-013 : Écran spécialité — liste interventions + toggle déplier."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def _client():
    """Client de test avec lifespan (données chargées en mémoire)."""
    with TestClient(app) as c:
        yield c


SPECIALITE_ID = "chirurgie-orthopedique-programmee"


@pytest.fixture(name="html")
def _html(client):
    """HTML de la page spécialité pour la chirurgie orthopédique programmée."""
    return client.get(f"/specialites/{SPECIALITE_ID}").text


# ---------- Route et HTTP ----------


def test_specialite_route_retourne_200(client):
    """La route /specialites/{id} doit retourner 200 pour un ID valide."""
    response = client.get(f"/specialites/{SPECIALITE_ID}")
    assert response.status_code == 200


def test_specialite_id_inconnu_retourne_404(client):
    """Un ID de spécialité inconnu doit retourner 404."""
    response = client.get("/specialites/specialite-inexistante")
    assert response.status_code == 404


# ---------- Contenu principal ----------


def test_specialite_contient_nom(html):
    """Le titre H1 doit contenir le nom de la spécialité."""
    assert "Chirurgie orthopédique programmée" in html


def test_specialite_affiche_nombre_interventions(html):
    """Le nombre d'interventions doit être affiché."""
    assert "30 interventions" in html


def test_specialite_liste_interventions(html):
    """Toutes les interventions doivent apparaître dans la liste."""
    assert "Prothèse de hanche ou de genou" in html
    assert "Arthroscopie diagnostique" in html


def test_specialite_apercu_molecule(html):
    """L'aperçu doit montrer la molécule principale."""
    assert "Céfazoline" in html


def test_specialite_apercu_pas_abp(html):
    """Les interventions sans ABP doivent afficher un aperçu distinct."""
    assert "Pas d'ABP recommandée" in html


def test_interventions_ont_lien_protocole(html):
    """Chaque intervention doit avoir un lien vers /protocole/{id}."""
    assert "/protocole/ortho-prog-mi-prothese-hanche-genou" in html
    assert "/protocole/ortho-prog-mi-arthroscopie-sans-materiel" in html
    assert "Voir le protocole complet" in html


def test_interventions_header_est_bouton(html):
    """Le header de chaque intervention est un bouton (accordéon), pas un lien."""
    assert 'class="intervention-item__header"' in html
    assert "aria-expanded" in html


# ---------- Breadcrumb ----------


def test_specialite_contient_breadcrumb(html):
    """Le breadcrumb doit être présent."""
    assert 'class="breadcrumb"' in html
    assert "Accueil" in html


# ---------- Bouton tout déplier ----------


def test_specialite_contient_bouton_deplier(html):
    """Le bouton 'Tout déplier' doit être présent."""
    lower = html.lower()
    assert "tout déplier" in lower or "tout replier" in lower


# ---------- Protocole inline (déplié) ----------


def test_specialite_contient_details_protocole_inline(html):
    """Les protocoles inline doivent être présents (cachés par défaut)."""
    assert 'class="intervention-item__detail" hidden' in html
    assert "protocol-card" in html


# ---------- CSS ----------


def test_css_specialite_accessible(client):
    """Le fichier specialite.css doit être servi."""
    response = client.get("/static/css/specialite.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]


def test_css_contient_intervention_item(client):
    """Le CSS doit définir le composant intervention-item."""
    css = client.get("/static/css/specialite.css").text
    assert ".intervention-item" in css


# ---------- Sous-catégories (issue #28) ----------


def test_specialite_affiche_sous_categories_h2(html):
    """Les sous-catégories doivent apparaître comme titres h2."""
    assert 'class="sous-categorie-heading"' in html
    assert "Membre inférieur" in html
    assert "Épaule et coude" in html


def test_specialite_contient_css_sous_categorie(client):
    """Le CSS doit définir le composant sous-categorie-heading."""
    css = client.get("/static/css/specialite.css").text
    assert ".sous-categorie-heading" in css


# ---------- Sous-catégories repliables (feat/toggle-sous-categories) ----------


def test_sous_categorie_heading_a_data_toggle(html):
    """Les h2 de sous-catégorie doivent avoir l'attribut data-toggle='sous-categorie'."""
    assert 'data-toggle="sous-categorie"' in html


def test_sous_categorie_heading_a_aria_expanded(html):
    """Les h2 de sous-catégorie doivent avoir aria-expanded (repliés par défaut)."""
    assert 'aria-expanded="false"' in html


def test_sous_categorie_heading_a_chevron(html):
    """Les h2 de sous-catégorie doivent contenir un chevron."""
    assert "sous-categorie-heading__chevron" in html


def test_sous_categorie_body_wrapper_present(html):
    """Les interventions doivent être enveloppées dans un data-sous-categorie-body."""
    assert "data-sous-categorie-body" in html


def test_css_sous_categorie_heading_pointer(client):
    """Le CSS doit définir cursor: pointer sur sous-categorie-heading."""
    css = client.get("/static/css/specialite.css").text
    assert "cursor: pointer" in css


def test_css_sous_categorie_chevron(client):
    """Le CSS doit définir le style du chevron sous-categorie."""
    css = client.get("/static/css/specialite.css").text
    assert ".sous-categorie-heading__chevron" in css
