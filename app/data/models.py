"""Modèles Pydantic — données d'antibioprophylaxie (RFE SFAR 2024).

Basé sur la section 5 de l'architecture, ajusté pour coller aux tableaux du PDF :
- ``protocole`` est optionnel (None quand pas d'antibioprophylaxie recommandée)
- ``alternative_allergie`` est une liste de ``Protocole`` (1ère et 2nde intention)
- ``force_recommandation`` est un Enum à 3 valeurs
"""

from __future__ import annotations

import datetime  # noqa: TC003 — nécessaire au runtime pour Pydantic
from enum import StrEnum

from pydantic import BaseModel


class Molecule(StrEnum):
    """Molécule ou association utilisée en antibioprophylaxie."""

    CEFAZOLINE = "Céfazoline"
    CLINDAMYCINE = "Clindamycine"
    VANCOMYCINE = "Vancomycine"
    TEICOPLANINE = "Teicoplanine"
    AMOXICILLINE_CLAVULANATE = "Amoxicilline/Clavulanate"
    GENTAMICINE = "Gentamicine"
    CLINDAMYCINE_GENTAMICINE = "Clindamycine + Gentamicine"
    CEFAZOLINE_GENTAMICINE = "Céfazoline + Gentamicine"


class ForceRecommandation(StrEnum):
    """Force de la recommandation selon la méthodologie GRADE."""

    AVIS_EXPERTS = "Avis d'experts"
    GRADE_1 = "GRADE 1"
    GRADE_2 = "GRADE 2"


class Protocole(BaseModel):
    """Protocole d'antibioprophylaxie (standard ou alternative allergie)."""

    molecule: Molecule
    posologie: str
    reinjection: str | None = None
    duree: str | None = None


class Intervention(BaseModel):
    """Une intervention chirurgicale avec son protocole d'antibioprophylaxie."""

    id: str
    nom: str
    specialite: str
    protocole: Protocole | None = None
    alternative_allergie: list[Protocole] | None = None
    force_recommandation: ForceRecommandation
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
    date_extraction: datetime.date
    specialites: list[Specialite]
    recommandations_generales: list[RecommandationGenerale] = []
