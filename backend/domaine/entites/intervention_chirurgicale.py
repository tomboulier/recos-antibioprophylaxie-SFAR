"""
Entité représentant une intervention chirurgicale.

Ce module définit la classe InterventionChirurgicale qui modélise
les différentes interventions chirurgicales mentionnées dans les 
recommandations SFAR d'antibioprophylaxie.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

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
    
    # Champs obligatoires en premier
    nom: str
    # Champs optionnels ensuite
    description: Optional[str] = None
    facteurs_risque: Optional[str] = None
    specialites: List[SpecialiteChirurgicale] = field(default_factory=list)
    # Redéfinition des champs hérités avec leurs valeurs par défaut
    id: Optional[int] = None
    date_creation: datetime = field(default_factory=datetime.utcnow)
    date_modification: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.nom:
            raise ValueError("Le nom de l'intervention chirurgicale ne peut pas être vide")
