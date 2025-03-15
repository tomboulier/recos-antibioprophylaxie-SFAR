"""
DTO pour les interventions chirurgicales.

Ce module définit les classes DTO pour les interventions chirurgicales.
"""
from typing import List, Optional

from pydantic import Field, validator

from application.dto.dto_base import DTOBase
from application.dto.specialite_chirurgicale_dto import SpecialiteChirurgicaleReponse


class InterventionChirurgicaleBase(DTOBase):
    """
    DTO de base pour les interventions chirurgicales.
    
    Attributs
    ---------
    nom : str
        Nom de l'intervention chirurgicale
    description : Optional[str]
        Description détaillée de l'intervention
    facteurs_risque : Optional[str]
        Facteurs de risque associés à l'intervention
    """
    
    nom: str
    description: Optional[str] = None
    facteurs_risque: Optional[str] = None
    
    @validator('nom')
    def nom_non_vide(cls, v):
        """Valide que le nom n'est pas vide."""
        if not v or not v.strip():
            raise ValueError("Le nom de l'intervention chirurgicale ne peut pas être vide")
        return v.strip()


class InterventionChirurgicaleCreation(InterventionChirurgicaleBase):
    """
    DTO pour la création d'une intervention chirurgicale.
    
    Attributs
    ---------
    specialites_ids : List[int]
        Liste des identifiants des spécialités chirurgicales associées
    """
    
    specialites_ids: List[int] = Field(default_factory=list)


class InterventionChirurgicaleMiseAJour(InterventionChirurgicaleBase):
    """
    DTO pour la mise à jour d'une intervention chirurgicale.
    
    Attributs
    ---------
    specialites_ids : List[int]
        Liste des identifiants des spécialités chirurgicales associées
    """
    
    specialites_ids: List[int] = Field(default_factory=list)


class InterventionChirurgicaleReponse(InterventionChirurgicaleBase):
    """
    DTO pour la réponse contenant une intervention chirurgicale.
    
    Attributs
    ---------
    id : int
        Identifiant unique de l'intervention chirurgicale
    specialites : List[SpecialiteChirurgicaleReponse]
        Liste des spécialités chirurgicales associées
    """
    
    id: int
    specialites: List[SpecialiteChirurgicaleReponse] = Field(default_factory=list)


class InterventionChirurgicaleCollection(DTOBase):
    """
    DTO pour une collection d'interventions chirurgicales.
    
    Attributs
    ---------
    items : List[InterventionChirurgicaleReponse]
        Liste des interventions chirurgicales
    total : int
        Nombre total d'interventions chirurgicales
    """
    
    items: List[InterventionChirurgicaleReponse]
    total: int
