"""
Modèle SQLAlchemy pour les recommandations d'antibioprophylaxie.

Ce module définit le modèle de données pour les recommandations d'antibioprophylaxie
selon les directives de la SFAR.
"""

from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from infrastructure.persistance.database import Base
from infrastructure.persistance.models.modele_base import ModeleBase


class StatutRecommandation(str, PyEnum):
    """
    Énumération des statuts possibles pour une recommandation.
    
    Valeurs
    -------
    ACTIVE : str
        La recommandation est active et à jour
    OBSOLETE : str
        La recommandation est marquée comme obsolète
    EN_REVISION : str
        La recommandation est en cours de révision
    """
    ACTIVE = "active"
    OBSOLETE = "obsolete"
    EN_REVISION = "en_revision"


class ModeleRecommandationAntibioprophylaxie(Base, ModeleBase):
    """
    Modèle SQLAlchemy pour les recommandations d'antibioprophylaxie.
    
    Ce modèle représente une recommandation d'antibioprophylaxie pour une
    intervention chirurgicale spécifique dans la base de données.
    
    Attributs
    ---------
    intervention_id : int
        Identifiant de l'intervention chirurgicale associée
    antibiotique_id : int
        Identifiant de l'antibiotique recommandé
    posologie : str
        Posologie recommandée pour l'antibioprophylaxie
    moment_administration : str, optionnel
        Moment recommandé pour l'administration (ex: "30 minutes avant l'incision")
    duree_max : str, optionnel
        Durée maximale recommandée
    reinjection : str, optionnel
        Recommandations pour la réinjection si nécessaire
    indications_specifiques : str, optionnel
        Indications spécifiques pour cette recommandation
    commentaires : str, optionnel
        Commentaires supplémentaires
    niveau_preuve : str, optionnel
        Niveau de preuve scientifique pour cette recommandation
    statut : StatutRecommandation
        Statut actuel de la recommandation
    est_premiere_intention : bool
        Indique si c'est l'antibiotique de première intention
    intervention : ModeleInterventionChirurgicale
        Relation avec l'intervention chirurgicale
    antibiotique : ModeleAntibiotique
        Relation avec l'antibiotique
    """
    
    __tablename__ = "recommandations_antibioprophylaxie"
    
    intervention_id = Column(Integer, ForeignKey("interventions_chirurgicales.id", ondelete="CASCADE"), nullable=False)
    antibiotique_id = Column(Integer, ForeignKey("antibiotiques.id", ondelete="CASCADE"), nullable=False)
    posologie = Column(String(200), nullable=False)
    moment_administration = Column(String(100), nullable=True)
    duree_max = Column(String(100), nullable=True)
    reinjection = Column(String(200), nullable=True)
    indications_specifiques = Column(Text, nullable=True)
    commentaires = Column(Text, nullable=True)
    niveau_preuve = Column(String(50), nullable=True)
    statut = Column(
        Enum(StatutRecommandation, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=StatutRecommandation.ACTIVE
    )
    est_premiere_intention = Column(Boolean, nullable=False, default=False)
    
    # Relations
    intervention = relationship("ModeleInterventionChirurgicale", back_populates="recommandations")
    antibiotique = relationship("ModeleAntibiotique", back_populates="recommandations")
    
    def __repr__(self) -> str:
        """
        Représentation textuelle du modèle.
        
        Retourne
        --------
        str
            Représentation du modèle sous forme de chaîne
        """
        return (
            f"<RecommandationAntibioprophylaxie(id={self.id}, "
            f"intervention_id={self.intervention_id}, "
            f"antibiotique_id={self.antibiotique_id})>"
        )
