"""
Entité représentant une spécialité chirurgicale.

Ce module définit la classe SpecialiteChirurgicale qui modélise
les différentes spécialités chirurgicales selon les recommandations SFAR.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from domaine.entites.entite_base import EntiteBase


@dataclass
class SpecialiteChirurgicale(EntiteBase):
    """
    Spécialité chirurgicale selon les recommandations SFAR.
    
    Cette classe représente une spécialité chirurgicale comme définie
    dans les recommandations d'antibioprophylaxie de la SFAR.
    
    Attributs
    ---------
    nom : str
        Nom de la spécialité chirurgicale (ex: "Chirurgie cardiaque")
    description : Optional[str]
        Description détaillée de la spécialité chirurgicale
    """
    
    nom: str
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.nom:
            raise ValueError("Le nom de la spécialité chirurgicale ne peut pas être vide")
