"""Routes web — pages HTML rendues côté serveur."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
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


@router.get("/protocole/{intervention_id}")
async def protocole(request: Request, intervention_id: str):
    """Page protocole — détail d'une intervention avec protocole ABP.

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.
    intervention_id : str
        Identifiant slug de l'intervention (ex: ortho-prog-mi-prothese-hanche-genou).

    Returns
    -------
    TemplateResponse | HTMLResponse
        Page HTML du protocole, ou 404 si l'intervention n'existe pas.
    """
    rfe = request.app.state.rfe_data
    for specialite in rfe.specialites:
        for intervention in specialite.interventions:
            if intervention.id == intervention_id:
                return templates.TemplateResponse(
                    request,
                    "protocole.html",
                    {
                        "intervention": intervention,
                        "specialite": specialite,
                    },
                )
    return HTMLResponse(
        content=templates.get_template("404.html").render({"request": request}),
        status_code=404,
    )
