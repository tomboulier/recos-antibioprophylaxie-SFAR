"""
Modèle SQLAlchemy pour les antibiotiques.

Ce module définit le modèle de données pour les antibiotiques.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from infrastructure.persistance.database import Base
from infrastructure.persistance.models.modele_base import ModeleBase


class ModeleAntibiotique(Base, ModeleBase):
    """
    Modèle SQLAlchemy pour les antibiotiques.
    
    Ce modèle représente un antibiotique dans la base de données.
    
    Attributs
    ---------
    nom : str
        Nom commercial de l'antibiotique
    nom_generique : str, optionnel
        Nom générique ou DCI (Dénomination Commune Internationale)
    description : str, optionnel
        Description de l'antibiotique
    posologie_standard : str, optionnel
        Informations générales sur la posologie standard
    contre_indications : str, optionnel
        Contre-indications notables
    recommandations : List[ModeleRecommandationAntibioprophylaxie]
        Relation avec les recommandations d'antibioprophylaxie utilisant cet antibiotique
    """
    
    __tablename__ = "antibiotiques"
    
    nom = Column(String(150), nullable=False, index=True, unique=True)
    nom_generique = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    posologie_standard = Column(Text, nullable=True)
    contre_indications = Column(Text, nullable=True)
    
    # Relations
    recommandations = relationship(
        "ModeleRecommandationAntibioprophylaxie", 
        back_populates="antibiotique",
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
        return f"<Antibiotique(id={self.id}, nom='{self.nom}')>"
