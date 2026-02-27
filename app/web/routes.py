"""Routes web — pages HTML rendues côté serveur."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import _PROJECT_ROOT

router = APIRouter()
templates = Jinja2Templates(directory=str(_PROJECT_ROOT / "app" / "templates"))


@router.get("/")
async def accueil(request: Request):
    """Page d'accueil — recherche + navigation par spécialité.

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.

    Returns
    -------
    TemplateResponse
        Page HTML avec héros, barre de recherche et grille des spécialités.
    """
    rfe = request.app.state.rfe_data
    specialites = [
        {
            "id": s.id,
            "nom": s.nom,
            "nb_interventions": len(s.interventions),
        }
        for s in rfe.specialites
    ]
    return templates.TemplateResponse(
        request,
        "accueil.html",
        {"specialites": specialites},
    )
