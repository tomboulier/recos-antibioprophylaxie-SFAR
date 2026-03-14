"""Endpoint de recherche fuzzy — /api/v1/search."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

from app.data.search import search_interventions

router = APIRouter(prefix="/api/v1", tags=["search"])


class SearchResultResponse(BaseModel):
    """Schéma de réponse pour un résultat de recherche.

    Attributes
    ----------
    id : str
        Identifiant unique de l'intervention.
    nom : str
        Nom de l'intervention chirurgicale.
    specialite : str
        Spécialité chirurgicale.
    score : float
        Score de similarité (0–100).
    """

    id: str
    nom: str
    specialite: str
    score: float


@router.get("/search", response_model=list[SearchResultResponse])
def search(
    request: Request,
    q: Annotated[str, Query(description="Texte de recherche")] = "",
    limit: Annotated[int, Query(ge=1, le=50, description="Nombre max de résultats")] = 10,
) -> list[SearchResultResponse]:
    """Recherche fuzzy d'interventions chirurgicales.

    Parameters
    ----------
    request : Request
        Requête FastAPI (accès aux données via app.state).
    q : str, optional
        Texte de recherche (nom d'intervention, spécialité).
        Retourne une liste vide si absent ou vide.
    limit : int, optional
        Nombre maximum de résultats (défaut : 10, max : 50).

    Returns
    -------
    list[SearchResultResponse]
        Liste de résultats triés par score décroissant.
    """
    rfe_data = request.app.state.rfe_data
    results = search_interventions(q, rfe_data, limit=limit)
    return [
        SearchResultResponse(
            id=r.intervention.id,
            nom=r.intervention.nom,
            specialite=r.intervention.specialite,
            score=r.score,
        )
        for r in results
    ]
