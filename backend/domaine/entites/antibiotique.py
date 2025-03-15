"""
Entité représentant un antibiotique.

Ce module définit la classe Antibiotique qui modélise les antibiotiques
utilisés dans les recommandations d'antibioprophylaxie de la SFAR.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from domaine.entites.entite_base import EntiteBase


@dataclass
class Antibiotique(EntiteBase):
    """
    Antibiotique utilisé dans les recommandations SFAR.
    
    Cette classe représente un antibiotique pouvant être utilisé 
    en antibioprophylaxie selon les recommandations SFAR.
    
    Attributs
    ---------
    nom : str
        Nom commercial de l'antibiotique
    nom_generique : Optional[str]
        Nom générique ou DCI (Dénomination Commune Internationale)
    description : Optional[str]
        Description de l'antibiotique
    posologie_standard : Optional[str]
        Informations générales sur la posologie standard
    contre_indications : Optional[str]
        Contre-indications notables
    """
    
    nom: str
    nom_generique: Optional[str] = None
    description: Optional[str] = None
    posologie_standard: Optional[str] = None
    contre_indications: Optional[str] = None
    
    def __init__(
        self,
        nom: str,
        nom_generique: Optional[str] = None,
        description: Optional[str] = None,
        posologie_standard: Optional[str] = None,
        contre_indications: Optional[str] = None,
        id: Optional[int] = None,
        date_creation: Optional[datetime] = None,
        date_modification: Optional[datetime] = None,
    ):
        """
        Initialise une nouvelle instance d'Antibiotique.
        
        Paramètres
        ----------
        nom : str
            Nom commercial de l'antibiotique
        nom_generique : Optional[str], optional
            Nom générique ou DCI, par défaut None
        description : Optional[str], optional
            Description de l'antibiotique, par défaut None
        posologie_standard : Optional[str], optional
            Informations sur la posologie standard, par défaut None
        contre_indications : Optional[str], optional
            Contre-indications notables, par défaut None
        id : Optional[int], optional
            Identifiant unique, par défaut None
        date_creation : Optional[datetime], optional
            Date et heure de création, par défaut None
        date_modification : Optional[datetime], optional
            Date et heure de dernière modification, par défaut None
        """
        super().__init__(id, date_creation, date_modification)
        self.nom = nom
        self.nom_generique = nom_generique
        self.description = description
        self.posologie_standard = posologie_standard
        self.contre_indications = contre_indications
        self._valider()
        
    def _valider(self):
        """Valide les invariants de l'entité."""
        if not self.nom:
            raise ValueError("Le nom de l'antibiotique ne peut pas être vide")
