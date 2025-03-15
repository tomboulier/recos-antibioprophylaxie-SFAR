"""
Entité représentant une intervention chirurgicale.

Ce module définit la classe InterventionChirurgicale qui modélise
les différentes interventions chirurgicales mentionnées dans les 
recommandations SFAR d'antibioprophylaxie.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from domaine.entites.entite_base import EntiteBase
from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale


@dataclass
class InterventionChirurgicale(EntiteBase):
    """
    Intervention chirurgicale selon les recommandations SFAR.
    
    Cette classe représente une procédure chirurgicale spécifique pour laquelle
    des recommandations d'antibioprophylaxie existent.
    
    Attributs
    ---------
    nom : str
        Nom de l'intervention chirurgicale (ex: "Chirurgie de la hanche")
    description : Optional[str]
        Description détaillée de l'intervention
    facteurs_risque : Optional[str]
        Facteurs de risque associés à l'intervention
    specialites : List[SpecialiteChirurgicale]
        Spécialités chirurgicales auxquelles cette intervention appartient
    """
    
    nom: str
    description: Optional[str] = None
    facteurs_risque: Optional[str] = None
    specialites: List[SpecialiteChirurgicale] = field(default_factory=list)
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.nom:
            raise ValueError("Le nom de l'intervention chirurgicale ne peut pas être vide")
