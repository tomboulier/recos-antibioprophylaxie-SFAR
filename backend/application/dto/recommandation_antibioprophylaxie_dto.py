"""
DTO pour les recommandations d'antibioprophylaxie.

Ce module définit les classes DTO pour les recommandations d'antibioprophylaxie
selon les directives de la SFAR.
"""
from typing import List, Optional

from pydantic import Field, validator

from application.dto.antibiotique_dto import AntibiotiqueReponse
from application.dto.dto_base import DTOBase
from application.dto.intervention_chirurgicale_dto import InterventionChirurgicaleReponse


class RecommandationAntibioprophylaxieBase(DTOBase):
    """
    DTO de base pour les recommandations d'antibioprophylaxie.
    
    Attributs
    ---------
    posologie : str
        Posologie recommandée (ex: "2g IV")
    moment_administration : str
        Moment d'administration (ex: "30-60 minutes avant incision")
    duree : str
        Durée de la prophylaxie (ex: "Dose unique" ou "24h maximum")
    est_alternative : bool
        Indique s'il s'agit d'une recommandation alternative (en cas d'allergie, etc.)
    populations_specifiques : Optional[str]
        Considérations particulières pour certaines populations de patients
    niveau_preuve : Optional[str]
        Niveau de preuve de la recommandation (ex: "Grade 1+")
    remarques : Optional[str]
        Remarques ou avertissements supplémentaires
    """
    
    posologie: str
    moment_administration: str
    duree: str
    est_alternative: bool = False
    populations_specifiques: Optional[str] = None
    niveau_preuve: Optional[str] = None
    remarques: Optional[str] = None
    
    @validator('posologie', 'moment_administration', 'duree')
    def champ_non_vide(cls, v, values, field):
        """Valide que les champs obligatoires ne sont pas vides."""
        if not v or not v.strip():
            raise ValueError(f"Le champ {field.name} ne peut pas être vide")
        return v.strip()


class RecommandationAntibioprophylaxieCreation(RecommandationAntibioprophylaxieBase):
    """
    DTO pour la création d'une recommandation d'antibioprophylaxie.
    
    Attributs
    ---------
    intervention_id : int
        Identifiant de l'intervention chirurgicale
    antibiotique_id : int
        Identifiant de l'antibiotique recommandé
    """
    
    intervention_id: int
    antibiotique_id: int


class RecommandationAntibioprophylaxieMiseAJour(RecommandationAntibioprophylaxieBase):
    """
    DTO pour la mise à jour d'une recommandation d'antibioprophylaxie.
    
    Attributs
    ---------
    intervention_id : Optional[int]
        Identifiant de l'intervention chirurgicale
    antibiotique_id : Optional[int]
        Identifiant de l'antibiotique recommandé
    """
    
    intervention_id: Optional[int] = None
    antibiotique_id: Optional[int] = None


class RecommandationAntibioprophylaxieReponse(RecommandationAntibioprophylaxieBase):
    """
    DTO pour la réponse contenant une recommandation d'antibioprophylaxie complète.
    
    Attributs
    ---------
    id : int
        Identifiant unique de la recommandation
    intervention : InterventionChirurgicaleReponse
        L'intervention chirurgicale concernée
    antibiotique : AntibiotiqueReponse
        L'antibiotique recommandé
    """
    
    id: int
    intervention: InterventionChirurgicaleReponse
    antibiotique: AntibiotiqueReponse


class RecommandationAntibioprophylaxieCollection(DTOBase):
    """
    DTO pour une collection de recommandations d'antibioprophylaxie.
    
    Attributs
    ---------
    items : List[RecommandationAntibioprophylaxieReponse]
        Liste des recommandations d'antibioprophylaxie
    total : int
        Nombre total de recommandations
    """
    
    items: List[RecommandationAntibioprophylaxieReponse]
    total: int
