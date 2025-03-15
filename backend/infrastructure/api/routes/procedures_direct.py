"""
Routes directes pour les procédures chirurgicales.

Ce module définit les endpoints API pour la gestion des procédures chirurgicales
en contournant les problèmes de sérialisation entre SQLAlchemy 2.0 et Pydantic.
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Procedure
from infrastructure.api.serializers import serialize_procedure, serialize_procedures

# Configuration du logger
logger = logging.getLogger(__name__)

# Création du routeur
router = APIRouter()


@router.get("/")
def read_procedures(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> JSONResponse:
    """
    Récupère toutes les procédures chirurgicales.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    skip : int
        Nombre d'éléments à sauter
    limit : int
        Nombre maximum d'éléments à retourner
    
    Retourne
    --------
    JSONResponse
        Liste des procédures chirurgicales
    """
    procedures = db.query(Procedure).offset(skip).limit(limit).all()
    return JSONResponse(content=serialize_procedures(procedures))


@router.get("/{id}")
def read_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> JSONResponse:
    """
    Récupère une procédure chirurgicale par son ID.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    id : int
        ID de la procédure à récupérer
    
    Retourne
    --------
    JSONResponse
        La procédure demandée
    
    Raises
    ------
    HTTPException
        Si la procédure n'existe pas
    """
    procedure = db.query(Procedure).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procédure non trouvée")
    return JSONResponse(content=serialize_procedure(procedure))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_procedure(
    *,
    db: Session = Depends(get_db),
    procedure_data: Dict[str, Any],
) -> JSONResponse:
    """
    Crée une nouvelle procédure chirurgicale.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    procedure_data : Dict[str, Any]
        Données de la procédure à créer
    
    Retourne
    --------
    JSONResponse
        La procédure créée
    """
    procedure = Procedure(
        name=procedure_data.get("name"),
        description=procedure_data.get("description"),
        risk_factors=procedure_data.get("risk_factors"),
    )
    db.add(procedure)
    db.commit()
    db.refresh(procedure)
    return JSONResponse(content=serialize_procedure(procedure))


@router.put("/{id}")
def update_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
    procedure_data: Dict[str, Any],
) -> JSONResponse:
    """
    Met à jour une procédure chirurgicale.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    id : int
        ID de la procédure à mettre à jour
    procedure_data : Dict[str, Any]
        Données de mise à jour de la procédure
    
    Retourne
    --------
    JSONResponse
        La procédure mise à jour
    
    Raises
    ------
    HTTPException
        Si la procédure n'existe pas
    """
    procedure = db.query(Procedure).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procédure non trouvée")
    
    # Mettre à jour les attributs
    if "name" in procedure_data:
        procedure.name = procedure_data["name"]
    if "description" in procedure_data:
        procedure.description = procedure_data["description"]
    if "risk_factors" in procedure_data:
        procedure.risk_factors = procedure_data["risk_factors"]
    
    db.add(procedure)
    db.commit()
    db.refresh(procedure)
    return JSONResponse(content=serialize_procedure(procedure))


@router.delete("/{id}")
def delete_procedure(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> JSONResponse:
    """
    Supprime une procédure chirurgicale.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    id : int
        ID de la procédure à supprimer
    
    Retourne
    --------
    JSONResponse
        La procédure supprimée
    
    Raises
    ------
    HTTPException
        Si la procédure n'existe pas
    """
    procedure = db.query(Procedure).filter(Procedure.id == id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procédure non trouvée")
    
    # Conserver une copie des données pour la réponse
    procedure_data = serialize_procedure(procedure)
    
    db.delete(procedure)
    db.commit()
    return JSONResponse(content=procedure_data)


@router.get("/search/by-name")
def search_procedures_by_name(
    *,
    db: Session = Depends(get_db),
    name: str = Query(..., min_length=3, description="Terme de recherche (min 3 caractères)"),
) -> JSONResponse:
    """
    Recherche des procédures chirurgicales par nom.
    
    Paramètres
    ----------
    db : Session
        Session de base de données SQLAlchemy
    name : str
        Terme de recherche (minimum 3 caractères)
    
    Retourne
    --------
    JSONResponse
        Liste des procédures correspondant au terme de recherche
    """
    procedures = db.query(Procedure).filter(
        Procedure.name.ilike(f"%{name}%")
    ).all()
    return JSONResponse(content=serialize_procedures(procedures))
