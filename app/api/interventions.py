"""Endpoints REST — interventions chirurgicales /api/v1/interventions."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from app.data.models import Intervention

router = APIRouter(prefix="/api/v1/interventions", tags=["interventions"])


@router.get("", response_model=list[Intervention])
def list_interventions(
    request: Request,
    skip: Annotated[int, Query(ge=0, description="Nombre d'éléments à sauter")] = 0,
    limit: Annotated[int, Query(ge=1, le=200, description="Nombre max d'éléments")] = 50,
) -> list[Intervention]:
    """Liste toutes les interventions chirurgicales avec pagination.

    Parameters
    ----------
    request : Request
        Requête FastAPI (accès aux données via app.state).
    skip : int, optional
        Nombre d'éléments à sauter (défaut : 0).
    limit : int, optional
        Nombre maximum d'éléments retournés (défaut : 50, max : 200).

    Returns
    -------
    list[Intervention]
        Liste paginée des interventions.
    """
    rfe_data = request.app.state.rfe_data
    all_interventions: list[Intervention] = []
    for specialite in rfe_data.specialites:
        all_interventions.extend(specialite.interventions)
    return all_interventions[skip : skip + limit]


@router.get("/{intervention_id}", response_model=Intervention)
def get_intervention(intervention_id: str, request: Request) -> Intervention:
    """Retourne le détail d'une intervention chirurgicale.

    Parameters
    ----------
    intervention_id : str
        Identifiant de l'intervention (slug).
    request : Request
        Requête FastAPI (accès aux données via app.state).

    Returns
    -------
    Intervention
        Détail complet de l'intervention.

    Raises
    ------
    HTTPException
        404 si l'intervention n'existe pas.
    """
    rfe_data = request.app.state.rfe_data
    for specialite in rfe_data.specialites:
        for intervention in specialite.interventions:
            if intervention.id == intervention_id:
                return intervention
    raise HTTPException(status_code=404, detail=f"Intervention '{intervention_id}' non trouvée.")
