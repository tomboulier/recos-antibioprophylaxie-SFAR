"""Recherche fuzzy des interventions chirurgicales.

Utilise rapidfuzz pour le matching approximatif sur les noms d'interventions
et les spécialités.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import TYPE_CHECKING

from rapidfuzz import fuzz, process

if TYPE_CHECKING:
    from app.data.models import Intervention, RFEData

# Seuil minimal de score pour retenir un résultat (sur 100)
_SCORE_MIN = 75


def _strip_accents(text: str) -> str:
    """Supprime les accents d'une chaîne (NFD + filtre catégorie Mn).

    Parameters
    ----------
    text : str
        Texte à normaliser.

    Returns
    -------
    str
        Texte sans accents, en minuscules.

    Examples
    --------
    >>> _strip_accents("Césarienne")
    'cesarienne'
    >>> _strip_accents("HÉPATIQUE")
    'hepatique'
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn"
    )


@dataclass
class SearchResult:
    """Résultat d'une recherche d'intervention.

    Attributes
    ----------
    intervention : Intervention
        L'intervention correspondante.
    score : float
        Score de similarité entre 0 et 100 (100 = correspondance exacte).
    """

    intervention: Intervention
    score: float


def _build_search_index(data: RFEData) -> list[tuple[str, Intervention]]:
    """Construit l'index de recherche à partir des données RFE.

    Parameters
    ----------
    data : RFEData
        Données RFE chargées en mémoire.

    Returns
    -------
    list[tuple[str, Intervention]]
        Liste de tuples (texte indexé, intervention).
    """
    index = []
    for specialite in data.specialites:
        for intervention in specialite.interventions:
            # Indexer sur nom + spécialité, normalisé sans accents pour le matching
            texte = _strip_accents(f"{intervention.nom} {intervention.specialite}")
            index.append((texte, intervention))
    return index


def search_interventions(
    query: str,
    data: RFEData,
    limit: int = 10,
) -> list[SearchResult]:
    """Recherche des interventions par correspondance fuzzy.

    Effectue une recherche approximative sur le nom de l'intervention
    et la spécialité chirurgicale. Les résultats sont triés par score
    décroissant.

    Parameters
    ----------
    query : str
        Texte de recherche (nom d'intervention, spécialité, etc.).
        Si vide ou composé uniquement d'espaces, retourne une liste vide.
    data : RFEData
        Données RFE chargées en mémoire.
    limit : int, optional
        Nombre maximum de résultats retournés (défaut : 10).

    Returns
    -------
    list[SearchResult]
        Liste de résultats triés par score décroissant (0–100).
        Retourne une liste vide si la requête est vide ou sans correspondance.

    Examples
    --------
    >>> results = search_interventions("hanche", data)
    >>> results[0].intervention.nom
    'Prothèse de hanche'
    >>> results[0].score
    90.0
    """
    query = _strip_accents(query.strip())
    if not query:
        return []

    index = _build_search_index(data)
    if not index:
        return []

    # Pour les requêtes courtes (< 4 chars) : sous-chaîne exacte
    if len(query) < 4:
        results = []
        for texte, intervention in index:
            if query in texte:
                results.append(SearchResult(intervention=intervention, score=100.0))
        return results[:limit]

    # Pour les requêtes plus longues : fuzzy matching
    textes = [texte for texte, _ in index]
    matches = process.extract(
        query,
        textes,
        scorer=fuzz.partial_ratio,
        limit=limit,
        score_cutoff=_SCORE_MIN,
    )

    results = []
    for _match, score, idx in matches:
        _, intervention = index[idx]
        results.append(SearchResult(intervention=intervention, score=score))

    results.sort(key=lambda r: r.score, reverse=True)

    return results
