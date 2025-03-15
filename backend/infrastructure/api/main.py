"""
Point d'entrée principal de l'API.

Ce module initialise l'application FastAPI et configure les routes, middleware et dépendances.
"""

import logging
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routes
from infrastructure.api.routes import specialites
from infrastructure.api.routes import procedures_direct

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="API Antibioprophylaxie SFAR",
    description="API pour les recommandations d'antibioprophylaxie selon la SFAR",
    version="0.1.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes dans l'application
app.include_router(specialites.router, prefix="/specialites", tags=["Spécialités"])
app.include_router(procedures_direct.router, prefix="/procedures", tags=["Procédures"])


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Route racine de l'API.
    
    Retourne
    --------
    Dict[str, str]
        Message de bienvenue et informations sur l'API
    """
    return {
        "message": "Bienvenue sur l'API Antibioprophylaxie SFAR",
        "documentation": "/docs",
        "version": app.version,
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Vérification de l'état de santé de l'API.
    
    Retourne
    --------
    Dict[str, str]
        Statut de l'API
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Démarrage de l'API Antibioprophylaxie SFAR")
    uvicorn.run("infrastructure.api.main:app", host="0.0.0.0", port=8000, reload=True)
