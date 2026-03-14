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
    TemplateResponse
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
    return templates.TemplateResponse(
        request,
        "404.html",
        status_code=404,
    )


@router.get("/specialites/{specialite_id}")
async def specialite(request: Request, specialite_id: str):
    """Page spécialité — liste des interventions groupées par sous-catégorie.

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.
    specialite_id : str
        Identifiant slug de la spécialité (ex: chirurgie-orthopedique-programmee).

    Returns
    -------
    TemplateResponse
        Page HTML de la spécialité avec groupes par sous-catégorie, ou 404.
    """
    rfe = request.app.state.rfe_data
    for s in rfe.specialites:
        if s.id == specialite_id:
            groupes: dict[str, list] = {}
            for interv in s.interventions:
                cle = interv.sous_categorie or "Général"
                groupes.setdefault(cle, []).append(interv)
            return templates.TemplateResponse(
                request,
                "specialite.html",
                {"specialite": s, "groupes": groupes},
            )
    return templates.TemplateResponse(
        request,
        "404.html",
        status_code=404,
    )
