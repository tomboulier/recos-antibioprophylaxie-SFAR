"""
Routes pour les spécialités chirurgicales.

Ce module définit les endpoints API liés aux spécialités chirurgicales.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from application.dto.specialite_chirurgicale_dto import (
    SpecialiteChirurgicaleCollection,
    SpecialiteChirurgicaleCreation,
    SpecialiteChirurgicaleMiseAJour,
    SpecialiteChirurgicaleReponse,
)
from infrastructure.api.dependencies import get_service_specialite_chirurgicale

# Configuration du logger
logger = logging.getLogger(__name__)

# Création du router
router = APIRouter(
    prefix="/specialites",
    tags=["Spécialités Chirurgicales"],
    responses={404: {"description": "Spécialité non trouvée"}},
)


@router.get("/", response_model=SpecialiteChirurgicaleCollection)
async def lister_specialites(
    debut: int = Query(0, ge=0, description="Index de début pour la pagination"),
    limite: int = Query(100, ge=1, le=1000, description="Nombre maximum de résultats à retourner"),
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> SpecialiteChirurgicaleCollection:
    """
    Récupère la liste des spécialités chirurgicales avec pagination.
    
    Paramètres
    ----------
    debut : int
        Index de début pour la pagination (0-indexed)
    limite : int
        Nombre maximum de résultats à retourner
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Retourne
    --------
    SpecialiteChirurgicaleCollection
        Collection de spécialités chirurgicales
    """
    try:
        return service_specialite.obtenir_tous(debut=debut, limite=limite)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des spécialités chirurgicales: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la récupération des spécialités")


@router.get("/{specialite_id}", response_model=SpecialiteChirurgicaleReponse)
async def obtenir_specialite(
    specialite_id: int = Path(..., ge=1, description="Identifiant de la spécialité chirurgicale"),
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> SpecialiteChirurgicaleReponse:
    """
    Récupère une spécialité chirurgicale par son identifiant.
    
    Paramètres
    ----------
    specialite_id : int
        Identifiant de la spécialité chirurgicale
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Retourne
    --------
    SpecialiteChirurgicaleReponse
        Détails de la spécialité chirurgicale
        
    Lève
    ----
    HTTPException
        Si la spécialité n'est pas trouvée (404)
    """
    specialite = service_specialite.obtenir_par_id(specialite_id)
    if not specialite:
        logger.info(f"Spécialité chirurgicale non trouvée, id: {specialite_id}")
        raise HTTPException(status_code=404, detail="Spécialité chirurgicale non trouvée")
    
    return specialite


@router.get("/nom/{nom}", response_model=SpecialiteChirurgicaleReponse)
async def obtenir_specialite_par_nom(
    nom: str,
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> SpecialiteChirurgicaleReponse:
    """
    Récupère une spécialité chirurgicale par son nom.
    
    Paramètres
    ----------
    nom : str
        Nom de la spécialité chirurgicale
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Retourne
    --------
    SpecialiteChirurgicaleReponse
        Détails de la spécialité chirurgicale
        
    Lève
    ----
    HTTPException
        Si la spécialité n'est pas trouvée (404)
    """
    specialite = service_specialite.obtenir_par_nom(nom)
    if not specialite:
        logger.info(f"Spécialité chirurgicale non trouvée, nom: {nom}")
        raise HTTPException(status_code=404, detail="Spécialité chirurgicale non trouvée")
    
    return specialite


@router.post("/", response_model=SpecialiteChirurgicaleReponse, status_code=201)
async def creer_specialite(
    specialite: SpecialiteChirurgicaleCreation,
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> SpecialiteChirurgicaleReponse:
    """
    Crée une nouvelle spécialité chirurgicale.
    
    Paramètres
    ----------
    specialite : SpecialiteChirurgicaleCreation
        Données de la spécialité chirurgicale à créer
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Retourne
    --------
    SpecialiteChirurgicaleReponse
        Détails de la spécialité chirurgicale créée
        
    Lève
    ----
    HTTPException
        Si la création échoue (400, 500)
    """
    try:
        return service_specialite.creer(specialite)
    except ValueError as e:
        logger.warning(f"Données invalides lors de la création d'une spécialité: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors de la création d'une spécialité: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la création de la spécialité")


@router.put("/{specialite_id}", response_model=SpecialiteChirurgicaleReponse)
async def mettre_a_jour_specialite(
    specialite_id: int = Path(..., ge=1, description="Identifiant de la spécialité chirurgicale"),
    specialite: SpecialiteChirurgicaleMiseAJour = None,
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> SpecialiteChirurgicaleReponse:
    """
    Met à jour une spécialité chirurgicale existante.
    
    Paramètres
    ----------
    specialite_id : int
        Identifiant de la spécialité chirurgicale à mettre à jour
    specialite : SpecialiteChirurgicaleMiseAJour
        Nouvelles données de la spécialité chirurgicale
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Retourne
    --------
    SpecialiteChirurgicaleReponse
        Détails de la spécialité chirurgicale mise à jour
        
    Lève
    ----
    HTTPException
        Si la spécialité n'est pas trouvée (404) ou si la mise à jour échoue (400, 500)
    """
    try:
        specialite_mise_a_jour = service_specialite.mettre_a_jour(specialite_id, specialite)
        return specialite_mise_a_jour
    except ValueError as e:
        if "Aucune entité trouvée" in str(e):
            logger.info(f"Spécialité chirurgicale non trouvée lors de la mise à jour, id: {specialite_id}")
            raise HTTPException(status_code=404, detail="Spécialité chirurgicale non trouvée")
        logger.warning(f"Données invalides lors de la mise à jour d'une spécialité: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour d'une spécialité: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la mise à jour de la spécialité")


@router.delete("/{specialite_id}", status_code=204)
async def supprimer_specialite(
    specialite_id: int = Path(..., ge=1, description="Identifiant de la spécialité chirurgicale"),
    service_specialite=Depends(get_service_specialite_chirurgicale),
) -> None:
    """
    Supprime une spécialité chirurgicale.
    
    Paramètres
    ----------
    specialite_id : int
        Identifiant de la spécialité chirurgicale à supprimer
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales, injecté par dépendance
        
    Lève
    ----
    HTTPException
        Si la spécialité n'est pas trouvée (404) ou si la suppression échoue (500)
    """
    try:
        resultat = service_specialite.supprimer(specialite_id)
        if not resultat:
            logger.info(f"Spécialité chirurgicale non trouvée lors de la suppression, id: {specialite_id}")
            raise HTTPException(status_code=404, detail="Spécialité chirurgicale non trouvée")
        return JSONResponse(status_code=204, content=None)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Erreur lors de la suppression d'une spécialité: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la suppression de la spécialité")
