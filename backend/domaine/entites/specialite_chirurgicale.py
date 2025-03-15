"""
Entité représentant une spécialité chirurgicale.

Ce module définit la classe SpecialiteChirurgicale qui modélise
les différentes spécialités chirurgicales selon les recommandations SFAR.
"""
from dataclasses import dataclass
from typing import Optional
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
    
    nom: str
    description: Optional[str] = None
    
    def __init__(
        self,
        nom: str,
        description: Optional[str] = None,
        id: Optional[int] = None,
        date_creation: Optional[datetime] = None,
        date_modification: Optional[datetime] = None,
    ):
        """
        Initialise une nouvelle instance de SpecialiteChirurgicale.
        
        Paramètres
        ----------
        nom : str
            Nom de la spécialité chirurgicale
        description : Optional[str], optional
            Description détaillée de la spécialité, par défaut None
        id : Optional[int], optional
            Identifiant unique, par défaut None
        date_creation : Optional[datetime], optional
            Date et heure de création, par défaut None (sera définit par EntiteBase)
        date_modification : Optional[datetime], optional
            Date et heure de dernière modification, par défaut None
        """
        super().__init__(id, date_creation, date_modification)
        self.nom = nom
        self.description = description
        self._valider()
        
    def _valider(self):
        """Valide les invariants de l'entité."""
        if not self.nom:
            raise ValueError("Le nom de la spécialité chirurgicale ne peut pas être vide")
