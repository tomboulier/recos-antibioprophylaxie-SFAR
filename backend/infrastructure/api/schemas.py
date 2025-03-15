"""
Schémas de données pour l'API.

Ce module définit les schémas Pydantic utilisés pour la validation
et la sérialisation des données dans l'API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SpecialiteBase(BaseModel):
    """
    Schéma de base pour une spécialité chirurgicale.
    
    Attributs
    ---------
    nom : str
        Nom de la spécialité
    description : Optional[str]
        Description de la spécialité
    """
    
    nom: str = Field(..., description="Nom de la spécialité chirurgicale")
    description: Optional[str] = Field(None, description="Description de la spécialité")


class SpecialiteCreate(SpecialiteBase):
    """Schéma pour la création d'une spécialité chirurgicale."""
    
    pass


class SpecialiteUpdate(SpecialiteBase):
    """Schéma pour la mise à jour d'une spécialité chirurgicale."""
    
    nom: Optional[str] = Field(None, description="Nom de la spécialité chirurgicale")


class Specialite(SpecialiteBase):
    """
    Schéma complet pour une spécialité chirurgicale avec ID.
    
    Attributs
    ---------
    id : int
        Identifiant unique de la spécialité
    """
    
    id: int = Field(..., description="Identifiant unique de la spécialité")
    
    class Config:
        """Configuration du modèle Pydantic."""
        
        from_attributes = True


class ProcedureBase(BaseModel):
    """
    Schéma de base pour une procédure chirurgicale.
    
    Attributs
    ---------
    nom : str
        Nom de la procédure
    description : Optional[str]
        Description de la procédure
    facteurs_risque : Optional[str]
        Facteurs de risque associés à la procédure
    """
    
    nom: str = Field(..., description="Nom de la procédure chirurgicale")
    description: Optional[str] = Field(None, description="Description de la procédure")
    facteurs_risque: Optional[str] = Field(None, description="Facteurs de risque associés")


class ProcedureCreate(ProcedureBase):
    """
    Schéma pour la création d'une procédure chirurgicale.
    
    Attributs
    ---------
    specialites_ids : Optional[List[int]]
        Liste des IDs des spécialités associées
    """
    
    specialites_ids: Optional[List[int]] = Field(None, description="IDs des spécialités associées")


class ProcedureUpdate(ProcedureBase):
    """
    Schéma pour la mise à jour d'une procédure chirurgicale.
    
    Attributs
    ---------
    nom : Optional[str]
        Nom de la procédure
    specialites_ids : Optional[List[int]]
        Liste des IDs des spécialités associées
    """
    
    nom: Optional[str] = Field(None, description="Nom de la procédure chirurgicale")
    specialites_ids: Optional[List[int]] = Field(None, description="IDs des spécialités associées")


class Procedure(ProcedureBase):
    """
    Schéma complet pour une procédure chirurgicale avec ID.
    
    Attributs
    ---------
    id : int
        Identifiant unique de la procédure
    specialites : Optional[List[Specialite]]
        Liste des spécialités associées
    """
    
    id: int = Field(..., description="Identifiant unique de la procédure")
    specialites: Optional[List[Specialite]] = Field(None, description="Spécialités associées")
    
    class Config:
        """Configuration du modèle Pydantic."""
        
        from_attributes = True
