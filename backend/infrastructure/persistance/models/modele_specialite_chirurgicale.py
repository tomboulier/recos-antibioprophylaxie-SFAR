"""
Modèle SQLAlchemy pour les spécialités chirurgicales.

Ce module définit le modèle de données pour les spécialités chirurgicales.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from infrastructure.persistance.database import Base
from infrastructure.persistance.models.modele_base import ModeleBase


class ModeleSpecialiteChirurgicale(Base, ModeleBase):
    """
    Modèle SQLAlchemy pour les spécialités chirurgicales.
    
    Ce modèle représente une spécialité chirurgicale dans la base de données.
    
    Attributs
    ---------
    nom : str
        Nom de la spécialité chirurgicale
    description : str, optionnel
        Description détaillée de la spécialité
    interventions : List[ModeleInterventionChirurgicale]
        Relation avec les interventions chirurgicales associées à cette spécialité
    """
    
    __tablename__ = "specialites_chirurgicales"
    
    nom = Column(String(100), nullable=False, index=True, unique=True)
    description = Column(Text, nullable=True)
    
    # Relations
    interventions = relationship(
        "ModeleInterventionChirurgicale", 
        secondary="specialites_interventions",
        back_populates="specialites"
    )
    
    def __repr__(self) -> str:
        """
        Représentation textuelle du modèle.
        
        Retourne
        --------
        str
            Représentation du modèle sous forme de chaîne
        """
        return f"<SpecialiteChirurgicale(id={self.id}, nom='{self.nom}')>"
