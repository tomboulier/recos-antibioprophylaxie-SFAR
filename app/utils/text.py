"""Utilitaires texte partagés (normalisation, accents, ligatures)."""

from __future__ import annotations

import unicodedata

# Table de translittération des ligatures courantes
_LIGATURE_TABLE = str.maketrans(
    {
        "œ": "oe",
        "Œ": "OE",
        "æ": "ae",
        "Æ": "AE",
    }
)


def strip_accents(text: str) -> str:
    """Supprime les accents et translittère les ligatures (NFD + filtre Mn).

    Parameters
    ----------
    text : str
        Texte à normaliser.

    Returns
    -------
    str
        Texte sans accents ni ligatures, en minuscules.

    Examples
    --------
    >>> strip_accents("Césarienne")
    'cesarienne'
    >>> strip_accents("HÉPATIQUE")
    'hepatique'
    >>> strip_accents("œsophage")
    'oesophage'
    >>> strip_accents("cœlioscopie")
    'coelioscopie'
    """
    text = text.lower().translate(_LIGATURE_TABLE)
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
