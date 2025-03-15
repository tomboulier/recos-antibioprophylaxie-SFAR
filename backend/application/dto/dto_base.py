"""
DTO (Data Transfer Object) de base pour tous les DTOs.

Ce module fournit une classe de base pour tous les DTOs utilisés
dans l'application.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DTOBase(BaseModel):
    """
    Classe de base pour tous les DTOs de l'application.
    
    Attributs
    ---------
    id : Optional[int]
        Identifiant unique de l'entité, None si nouvelle entité
    date_creation : Optional[datetime]
        Date et heure de création de l'entité
    date_modification : Optional[datetime]
        Date et heure de dernière modification de l'entité
    """
    
    id: Optional[int] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    
    class Config:
        """Configuration pour les DTOs Pydantic."""
        from_attributes = True  # Permet de créer un DTO à partir d'un attribut d'une classe (ORM)
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
