"""Routes web — pages HTML rendues côté serveur."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query, Request
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


@router.get("/search")
async def search_partial(
    request: Request,
    q: Annotated[str, Query(description="Texte de recherche")] = "",
):
    """Partial HTML pour la recherche fuzzy (HTMX).

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.
    q : str, optional
        Texte de recherche.

    Returns
    -------
    TemplateResponse
        Fragment HTML avec les résultats de recherche.
    """
    from app.data.search import search_interventions

    rfe = request.app.state.rfe_data
    results = search_interventions(q, rfe) if q.strip() else []
    items = [
        {
            "id": r.intervention.id,
            "nom": r.intervention.nom,
            "specialite": r.intervention.specialite,
        }
        for r in results
    ]
    return templates.TemplateResponse(
        request,
        "partials/search_results.html",
        {"results": items},
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
