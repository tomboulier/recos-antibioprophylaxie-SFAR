"""Chargement des données RFE depuis le fichier JSON."""

from __future__ import annotations

import json
from pathlib import Path  # noqa: TC003 — utilisé au runtime

from app.data.models import RFEData


def load_rfe_data(path: Path) -> RFEData:
    """Charge et valide les données RFE depuis un fichier JSON.

    Parameters
    ----------
    path : Path
        Chemin vers le fichier ``rfe.json``.

    Returns
    -------
    RFEData
        Données validées par Pydantic.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    json.JSONDecodeError
        Si le fichier n'est pas du JSON valide.
    pydantic.ValidationError
        Si les données ne respectent pas le schéma.
    """
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    return RFEData.model_validate(data)
