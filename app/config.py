"""Configuration de l'application via variables d'environnement."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings

# Racine du projet = 2 niveaux au-dessus de ce fichier (app/config.py → racine)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Paramètres de l'application, surchargeables via variables d'environnement."""

    app_name: str = "Antibioprophylaxie SFAR"
    app_version: str = "0.1.0"
    data_version: str = "RFE SFAR 2024"
    debug: bool = False
    data_path: Path = _PROJECT_ROOT / "data" / "rfe.json"
