"""
Modèle SQLAlchemy pour les interventions chirurgicales.

Ce module définit le modèle de données pour les interventions chirurgicales
et la table d'association avec les spécialités chirurgicales.
"""

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship

from infrastructure.persistance.database import Base
from infrastructure.persistance.models.modele_base import ModeleBase

# Table d'association pour la relation many-to-many entre spécialités et interventions
specialites_interventions = Table(
    "specialites_interventions",
    Base.metadata,
    Column("specialite_id", ForeignKey("specialites_chirurgicales.id", ondelete="CASCADE"), primary_key=True),
    Column("intervention_id", ForeignKey("interventions_chirurgicales.id", ondelete="CASCADE"), primary_key=True),
)


class ModeleInterventionChirurgicale(Base, ModeleBase):
    """
    Modèle SQLAlchemy pour les interventions chirurgicales.
    
    Ce modèle représente une intervention chirurgicale dans la base de données.
    
    Attributs
    ---------
    nom : str
        Nom de l'intervention chirurgicale
    description : str, optionnel
        Description détaillée de l'intervention
    facteurs_risque : str, optionnel
        Facteurs de risque associés à l'intervention
    specialites : List[ModeleSpecialiteChirurgicale]
        Relation avec les spécialités chirurgicales associées
    recommandations : List[ModeleRecommandationAntibioprophylaxie]
        Relation avec les recommandations d'antibioprophylaxie pour cette intervention
    """
    
    __tablename__ = "interventions_chirurgicales"
    
    nom = Column(String(200), nullable=False, index=True, unique=True)
    description = Column(Text, nullable=True)
    facteurs_risque = Column(Text, nullable=True)
    
    # Relations
    specialites = relationship(
        "ModeleSpecialiteChirurgicale", 
        secondary=specialites_interventions,
        back_populates="interventions"
    )
    recommandations = relationship(
        "ModeleRecommandationAntibioprophylaxie", 
        back_populates="intervention",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        """
        Représentation textuelle du modèle.
        
        Retourne
        --------
        str
            Représentation du modèle sous forme de chaîne
        """
        return f"<InterventionChirurgicale(id={self.id}, nom='{self.nom}')>"
