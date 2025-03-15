"""
Entité représentant une recommandation d'antibioprophylaxie.

Ce module définit la classe RecommandationAntibioprophylaxie qui modélise
les recommandations d'antibioprophylaxie de la SFAR pour chaque
intervention chirurgicale.
"""
from dataclasses import dataclass
from typing import Optional

from domaine.entites.antibiotique import Antibiotique
from domaine.entites.entite_base import EntiteBase
from domaine.entites.intervention_chirurgicale import InterventionChirurgicale


@dataclass
class RecommandationAntibioprophylaxie(EntiteBase):
    """
    Recommandation d'antibioprophylaxie selon la SFAR.
    
    Cette classe représente une recommandation spécifique d'antibioprophylaxie
    pour une intervention chirurgicale donnée.
    
    Attributs
    ---------
    intervention : InterventionChirurgicale
        L'intervention chirurgicale concernée par cette recommandation
    antibiotique : Antibiotique
        L'antibiotique recommandé
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
    
    intervention: InterventionChirurgicale
    antibiotique: Antibiotique
    posologie: str
    moment_administration: str
    duree: str
    est_alternative: bool = False
    populations_specifiques: Optional[str] = None
    niveau_preuve: Optional[str] = None
    remarques: Optional[str] = None
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.intervention:
            raise ValueError("L'intervention chirurgicale est obligatoire")
        if not self.antibiotique:
            raise ValueError("L'antibiotique est obligatoire")
        if not self.posologie:
            raise ValueError("La posologie est obligatoire")
        if not self.moment_administration:
            raise ValueError("Le moment d'administration est obligatoire")
        if not self.duree:
            raise ValueError("La durée est obligatoire")
