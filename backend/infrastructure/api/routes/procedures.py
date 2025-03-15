"""
Routes pour les procédures chirurgicales.

Ce module définit les routes pour l'API des procédures chirurgicales,
en adaptant les endpoints définis dans app.api.endpoints.procedures.
"""

import logging
from fastapi import APIRouter, status

from app.api.endpoints.procedures import (
    read_procedures,
    read_procedure,
    create_procedure,
    update_procedure, 
    delete_procedure,
    search_procedures_by_name
)

# Logger
logger = logging.getLogger(__name__)

# Router
router = APIRouter()

# Routes
router.add_api_route(
    path="/",
    endpoint=read_procedures,
    methods=["GET"],
    summary="Récupérer toutes les procédures",
    description="Récupère toutes les procédures chirurgicales avec pagination optionnelle"
)

router.add_api_route(
    path="/{id}",
    endpoint=read_procedure,
    methods=["GET"],
    summary="Récupérer une procédure",
    description="Récupère une procédure chirurgicale spécifique par son ID"
)

router.add_api_route(
    path="/",
    endpoint=create_procedure,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    summary="Créer une procédure",
    description="Crée une nouvelle procédure chirurgicale"
)

router.add_api_route(
    path="/{id}",
    endpoint=update_procedure,
    methods=["PUT"],
    summary="Mettre à jour une procédure",
    description="Met à jour une procédure chirurgicale existante"
)

router.add_api_route(
    path="/{id}",
    endpoint=delete_procedure,
    methods=["DELETE"],
    summary="Supprimer une procédure",
    description="Supprime une procédure chirurgicale existante"
)

router.add_api_route(
    path="/search/by-name",
    endpoint=search_procedures_by_name,
    methods=["GET"],
    summary="Rechercher des procédures par nom",
    description="Recherche des procédures chirurgicales par nom (minimum 3 caractères)"
)
