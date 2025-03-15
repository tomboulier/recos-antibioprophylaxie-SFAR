"""
Module de sérialisation pour l'API.

Ce module fournit des fonctions permettant de convertir les modèles SQLAlchemy
en dictionnaires compatibles avec les schémas Pydantic et la sérialisation JSON.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.models.models import Category, Procedure

# Configuration du logger
logger = logging.getLogger(__name__)


def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Convertit un objet datetime en chaîne de caractères ISO 8601.
    
    Paramètres
    ----------
    dt : Optional[datetime]
        Objet datetime à convertir
        
    Retourne
    --------
    Optional[str]
        Chaîne de caractères au format ISO 8601, ou None si dt est None
    """
    if dt is None:
        return None
    return dt.isoformat()


def serialize_category(category: Category) -> Dict[str, Any]:
    """
    Sérialise un objet Category en dictionnaire.
    
    Paramètres
    ----------
    category : Category
        Objet Category à sérialiser
        
    Retourne
    --------
    Dict[str, Any]
        Dictionnaire représentant l'objet Category
    """
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "created_at": serialize_datetime(category.created_at),
        "updated_at": serialize_datetime(category.updated_at),
    }


def serialize_procedure(procedure: Procedure) -> Dict[str, Any]:
    """
    Sérialise un objet Procedure en dictionnaire.
    
    Paramètres
    ----------
    procedure : Procedure
        Objet Procedure à sérialiser
        
    Retourne
    --------
    Dict[str, Any]
        Dictionnaire représentant l'objet Procedure
    """
    result = {
        "id": procedure.id,
        "name": procedure.name,
        "created_at": serialize_datetime(procedure.created_at),
        "updated_at": serialize_datetime(procedure.updated_at),
    }
    
    # Ajouter les catégories si elles sont chargées
    if hasattr(procedure, "categories") and procedure.categories is not None:
        result["categories"] = [serialize_category(cat) for cat in procedure.categories]
    else:
        result["categories"] = []
    
    return result


def serialize_procedures(procedures: List[Procedure]) -> List[Dict[str, Any]]:
    """
    Sérialise une liste d'objets Procedure en liste de dictionnaires.
    
    Paramètres
    ----------
    procedures : List[Procedure]
        Liste d'objets Procedure à sérialiser
        
    Retourne
    --------
    List[Dict[str, Any]]
        Liste de dictionnaires représentant les objets Procedure
    """
    return [serialize_procedure(p) for p in procedures]
