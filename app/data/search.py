"""Recherche fuzzy des interventions chirurgicales.

Utilise rapidfuzz pour le matching approximatif sur les noms d'interventions
et les spécialités.
"""

from __future__ import annotations

from dataclasses import dataclass

from rapidfuzz import fuzz, process

from app.data.models import Intervention, RFEData

# Seuil minimal de score pour retenir un résultat (sur 100)
_SCORE_MIN = 50


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
            # Indexer sur nom + spécialité pour enrichir le matching
            texte = f"{intervention.nom} {intervention.specialite}"
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
    query = query.strip()
    if not query:
        return []

    index = _build_search_index(data)
    if not index:
        return []

    textes = [texte for texte, _ in index]

    # rapidfuzz.process.extract retourne une liste de (match, score, index)
    matches = process.extract(
        query,
        textes,
        scorer=fuzz.WRatio,
        limit=limit,
        score_cutoff=_SCORE_MIN,
    )

    results = []
    for _match, score, idx in matches:
        _, intervention = index[idx]
        results.append(SearchResult(intervention=intervention, score=score))

    # Tri décroissant par score (process.extract retourne déjà trié,
    # mais on garantit l'ordre explicitement)
    results.sort(key=lambda r: r.score, reverse=True)

    return results
