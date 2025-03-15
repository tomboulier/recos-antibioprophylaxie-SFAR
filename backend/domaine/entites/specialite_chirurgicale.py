"""
Entité représentant une spécialité chirurgicale.

Ce module définit la classe SpecialiteChirurgicale qui modélise
les différentes spécialités chirurgicales selon les recommandations SFAR.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

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
    
    # Champs obligatoires en premier
    nom: str
    # Champs optionnels ensuite
    description: Optional[str] = None
    # Redéfinition des champs hérités avec leurs valeurs par défaut
    id: Optional[int] = None
    date_creation: datetime = field(default_factory=datetime.utcnow)
    date_modification: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validation après initialisation."""
        if not self.nom:
            raise ValueError("Le nom de la spécialité chirurgicale ne peut pas être vide")
