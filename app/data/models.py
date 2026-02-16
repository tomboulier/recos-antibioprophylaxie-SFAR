"""Modèles Pydantic — données d'antibioprophylaxie (RFE SFAR 2024).

Basé sur la section 5 de l'architecture, ajusté pour coller aux tableaux du PDF :
- `protocole` est optionnel (None quand pas_d_abp=True)
- `alternative_allergie` est une liste (1ère et 2nde intention possibles)
- `force_recommandation` ajouté (donnée clinique importante présente dans les tableaux)
"""

from __future__ import annotations

from pydantic import BaseModel


class Protocole(BaseModel):
    """Protocole d'antibioprophylaxie pour une intervention."""

    molecule: str
    posologie: str
    reinjection: str | None = None
    duree: str


class AlternativeAllergie(BaseModel):
    """Alternative en cas d'allergie aux bêtalactamines."""

    molecule: str
    posologie: str
    reinjection: str | None = None


class Intervention(BaseModel):
    """Une intervention chirurgicale avec son protocole d'ABP."""

    id: str
    nom: str
    specialite: str
    protocole: Protocole | None = None
    alternative_allergie: list[AlternativeAllergie] | None = None
    pas_d_abp: bool = False
    force_recommandation: str
    source_page: int
    source_tableau: str
    notes: str | None = None


class Specialite(BaseModel):
    """Une spécialité chirurgicale."""

    id: str
    nom: str
    interventions: list[Intervention]


class RecommandationGenerale(BaseModel):
    """Recommandation narrative transverse (FR-002)."""

    id: str
    titre: str
    contenu: str
    source_page: int


class RFEData(BaseModel):
    """Racine du fichier data/rfe.json."""

    version: str
    date_extraction: str
    specialites: list[Specialite]
    recommandations_generales: list[RecommandationGenerale] = []
