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
    
    nom: str
    description: Optional[str] = None
    facteurs_risque: Optional[str] = None
    specialites: List[SpecialiteChirurgicale] = field(default_factory=list)
    
    def __init__(
        self,
        nom: str,
        description: Optional[str] = None,
        facteurs_risque: Optional[str] = None,
        specialites: Optional[List[SpecialiteChirurgicale]] = None,
        id: Optional[int] = None,
        date_creation: Optional[datetime] = None,
        date_modification: Optional[datetime] = None,
    ):
        """
        Initialise une nouvelle instance d'InterventionChirurgicale.
        
        Paramètres
        ----------
        nom : str
            Nom de l'intervention chirurgicale
        description : Optional[str], optional
            Description détaillée de l'intervention, par défaut None
        facteurs_risque : Optional[str], optional
            Facteurs de risque associés à l'intervention, par défaut None
        specialites : Optional[List[SpecialiteChirurgicale]], optional
            Spécialités chirurgicales associées, par défaut liste vide
        id : Optional[int], optional
            Identifiant unique, par défaut None
        date_creation : Optional[datetime], optional
            Date et heure de création, par défaut None
        date_modification : Optional[datetime], optional
            Date et heure de dernière modification, par défaut None
        """
        super().__init__(id, date_creation, date_modification)
        self.nom = nom
        self.description = description
        self.facteurs_risque = facteurs_risque
        self.specialites = specialites or []
        self._valider()
        
    def _valider(self):
        """Valide les invariants de l'entité."""
        if not self.nom:
            raise ValueError("Le nom de l'intervention chirurgicale ne peut pas être vide")
            
    def ajouter_specialite(self, specialite: SpecialiteChirurgicale) -> None:
        """
        Ajoute une spécialité chirurgicale à cette intervention.
        
        Paramètres
        ----------
        specialite : SpecialiteChirurgicale
            La spécialité chirurgicale à ajouter
        """
        if specialite not in self.specialites:
            self.specialites.append(specialite)
            
    def retirer_specialite(self, specialite: SpecialiteChirurgicale) -> bool:
        """
        Retire une spécialité chirurgicale de cette intervention.
        
        Paramètres
        ----------
        specialite : SpecialiteChirurgicale
            La spécialité chirurgicale à retirer
            
        Retourne
        --------
        bool
            True si la spécialité a été retirée, False si elle n'était pas présente
        """
        if specialite in self.specialites:
            self.specialites.remove(specialite)
            return True
        return False
