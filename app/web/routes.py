"""Routes web — pages HTML rendues côté serveur."""

from __future__ import annotations

import re
from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from markupsafe import Markup

from app.config import _PROJECT_ROOT

router = APIRouter()
templates = Jinja2Templates(directory=str(_PROJECT_ROOT / "app" / "templates"))


def _highlight(text: str, query: str) -> Markup:
    """Surligne les occurrences de query dans text avec <mark>.

    La comparaison est insensible à la casse et aux accents : taper
    "cesari" surligne "Césarienne", "oeso" surligne "Œsophagectomie".
    Le texte affiché conserve ses accents et ligatures d'origine.

    Parameters
    ----------
    text : str
        Texte brut à traiter (non échappé).
    query : str
        Terme à surligner (insensible à la casse et aux accents).

    Returns
    -------
    Markup
        HTML sûr avec les occurrences entourées de <mark>.
    """
    from app.utils.text import strip_accents

    query_norm = strip_accents(query.strip())
    if not query_norm:
        return Markup.escape(text)

    # Construction d'une table de correspondance : position dans text_norm → position dans text.
    # strip_accents peut changer la longueur (ex: œ → oe), donc les offsets divergent.
    norm_to_orig: list[int] = []
    for i, char in enumerate(text):
        norm_char = strip_accents(char)
        norm_to_orig.extend([i] * len(norm_char))

    text_norm = strip_accents(text)
    pattern = re.compile(re.escape(query_norm))
    result = []
    last_orig = 0
    for m in pattern.finditer(text_norm):
        # Convertit les positions normalisées en positions originales
        orig_start = norm_to_orig[m.start()] if m.start() < len(norm_to_orig) else len(text)
        last_norm_idx = m.end() - 1
        in_bounds = m.end() > 0 and last_norm_idx < len(norm_to_orig)
        orig_end = (norm_to_orig[last_norm_idx] + 1) if in_bounds else len(text)
        result.append(str(Markup.escape(text[last_orig:orig_start])))
        result.append(f"<mark>{Markup.escape(text[orig_start:orig_end])}</mark>")
        last_orig = orig_end
    result.append(str(Markup.escape(text[last_orig:])))
    return Markup("".join(result))


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
    results = search_interventions(q, rfe, limit=6) if q.strip() else []
    items = [
        {
            "id": r.intervention.id,
            "nom": _highlight(r.intervention.nom, q),
            "specialite": r.intervention.specialite,
        }
        for r in results[:5]
    ]
    has_more = len(results) > 5
    return templates.TemplateResponse(
        request,
        "partials/search_results.html",
        {"results": items, "has_more": has_more, "query": q},
    )


@router.get("/specialites")
async def liste_specialites(request: Request):
    """Page liste de toutes les spécialités (lien 'Parcourir').

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.

    Returns
    -------
    TemplateResponse
        Page HTML avec la grille des spécialités.
    """
    rfe = request.app.state.rfe_data
    specialites = [
        {"id": s.id, "nom": s.nom, "nb_interventions": len(s.interventions)}
        for s in rfe.specialites
    ]
    return templates.TemplateResponse(
        request,
        "specialites.html",
        {"specialites": specialites},
    )


@router.get("/recherche")
async def recherche(
    request: Request,
    q: Annotated[str, Query(description="Texte de recherche")] = "",
):
    """Page de résultats de recherche complète.

    Parameters
    ----------
    request : Request
        Requête HTTP entrante.
    q : str, optional
        Texte de recherche.

    Returns
    -------
    TemplateResponse
        Page HTML avec tous les résultats de recherche.
    """
    from app.data.search import search_interventions

    rfe = request.app.state.rfe_data
    results = search_interventions(q, rfe, limit=50) if q.strip() else []
    items = [
        {
            "id": r.intervention.id,
            "nom": _highlight(r.intervention.nom, q),
            "specialite": r.intervention.specialite,
        }
        for r in results
    ]
    return templates.TemplateResponse(
        request,
        "recherche.html",
        {"query": q, "results": items},
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
