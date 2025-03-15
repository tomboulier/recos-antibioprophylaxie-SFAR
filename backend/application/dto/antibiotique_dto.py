"""
DTO pour les antibiotiques.

Ce module définit les classes DTO pour les antibiotiques.
"""
from typing import List, Optional

from pydantic import validator

from application.dto.dto_base import DTOBase


class AntibiotiqueBase(DTOBase):
    """
    DTO de base pour les antibiotiques.
    
    Attributs
    ---------
    nom : str
        Nom commercial de l'antibiotique
    nom_generique : Optional[str]
        Nom générique ou DCI (Dénomination Commune Internationale)
    description : Optional[str]
        Description de l'antibiotique
    posologie_standard : Optional[str]
        Informations générales sur la posologie standard
    contre_indications : Optional[str]
        Contre-indications notables
    """
    
    nom: str
    nom_generique: Optional[str] = None
    description: Optional[str] = None
    posologie_standard: Optional[str] = None
    contre_indications: Optional[str] = None
    
    @validator('nom')
    def nom_non_vide(cls, v):
        """Valide que le nom n'est pas vide."""
        if not v or not v.strip():
            raise ValueError("Le nom de l'antibiotique ne peut pas être vide")
        return v.strip()


class AntibiotiqueCreation(AntibiotiqueBase):
    """DTO pour la création d'un antibiotique."""
    
    pass


class AntibiotiqueModification(AntibiotiqueBase):
    """DTO pour la modification d'un antibiotique."""
    
    pass


class AntibiotiqueReponse(AntibiotiqueBase):
    """
    DTO pour la réponse contenant un antibiotique.
    
    Attributs
    ---------
    id : int
        Identifiant unique de l'antibiotique
    """
    
    id: int


class AntibiotiqueCollection(DTOBase):
    """
    DTO pour une collection d'antibiotiques.
    
    Attributs
    ---------
    items : List[AntibiotiqueReponse]
        Liste des antibiotiques
    total : int
        Nombre total d'antibiotiques
    """
    
    items: List[AntibiotiqueReponse]
    total: int
