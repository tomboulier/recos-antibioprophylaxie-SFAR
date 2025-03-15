"""
DTO pour les spécialités chirurgicales.

Ce module définit les classes DTO pour les spécialités chirurgicales.
"""
from typing import List, Optional

from pydantic import Field, validator

from application.dto.dto_base import DTOBase


class SpecialiteChirurgicaleBase(DTOBase):
    """
    DTO de base pour les spécialités chirurgicales.
    
    Attributs
    ---------
    nom : str
        Nom de la spécialité chirurgicale
    description : Optional[str]
        Description détaillée de la spécialité chirurgicale
    """
    
    nom: str
    description: Optional[str] = None
    
    @validator('nom')
    def nom_non_vide(cls, v):
        """Valide que le nom n'est pas vide."""
        if not v or not v.strip():
            raise ValueError("Le nom de la spécialité chirurgicale ne peut pas être vide")
        return v.strip()


class SpecialiteChirurgicaleCreation(SpecialiteChirurgicaleBase):
    """DTO pour la création d'une spécialité chirurgicale."""
    
    pass


class SpecialiteChirurgicaleMiseAJour(SpecialiteChirurgicaleBase):
    """DTO pour la mise à jour d'une spécialité chirurgicale."""
    
    pass


class SpecialiteChirurgicaleReponse(SpecialiteChirurgicaleBase):
    """
    DTO pour la réponse contenant une spécialité chirurgicale.
    
    Attributs
    ---------
    id : int
        Identifiant unique de la spécialité chirurgicale
    """
    
    id: int


class SpecialiteChirurgicaleCollection(DTOBase):
    """
    DTO pour une collection de spécialités chirurgicales.
    
    Attributs
    ---------
    items : List[SpecialiteChirurgicaleReponse]
        Liste des spécialités chirurgicales
    total : int
        Nombre total de spécialités chirurgicales
    """
    
    items: List[SpecialiteChirurgicaleReponse]
    total: int
