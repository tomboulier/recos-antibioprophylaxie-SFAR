"""Endpoints REST — spécialités chirurgicales /api/v1/specialites."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.data.models import Specialite

router = APIRouter(prefix="/api/v1/specialites", tags=["specialites"])


@router.get("", response_model=list[Specialite])
def list_specialites(request: Request) -> list[Specialite]:
    """Liste toutes les spécialités chirurgicales.

    Parameters
    ----------
    request : Request
        Requête FastAPI (accès aux données via app.state).

    Returns
    -------
    list[Specialite]
        Liste de toutes les spécialités avec leurs interventions.
    """
    rfe_data = request.app.state.rfe_data
    return rfe_data.specialites


@router.get("/{specialite_id}", response_model=Specialite)
def get_specialite(specialite_id: str, request: Request) -> Specialite:
    """Retourne une spécialité avec ses interventions.

    Parameters
    ----------
    specialite_id : str
        Identifiant de la spécialité (slug).
    request : Request
        Requête FastAPI (accès aux données via app.state).

    Returns
    -------
    Specialite
        La spécialité et ses interventions associées.

    Raises
    ------
    HTTPException
        404 si la spécialité n'existe pas.
    """
    rfe_data = request.app.state.rfe_data
    for specialite in rfe_data.specialites:
        if specialite.id == specialite_id:
            return specialite
    raise HTTPException(status_code=404, detail=f"Spécialité '{specialite_id}' non trouvée.")
