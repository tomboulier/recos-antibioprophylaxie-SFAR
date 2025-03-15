"""
Entité de base pour toutes les entités du domaine.

Cette classe fournit les fonctionnalités communes à toutes les entités,
notamment la gestion de l'identifiant unique.
"""
from abc import ABC
from datetime import datetime
from typing import Optional


class EntiteBase(ABC):
    """
    Classe de base pour toutes les entités du domaine.
    
    Cette classe abstraite fournit les attributs communs à toutes 
    les entités métier, notamment un identifiant unique.
    
    Attributs
    ---------
    id : Optional[int]
        Identifiant unique de l'entité. None si l'entité n'est pas persistée.
    date_creation : datetime
        Date et heure de création de l'entité
    date_modification : datetime
        Date et heure de dernière modification de l'entité
    """
    
    def __init__(
        self,
        id: Optional[int] = None,
        date_creation: Optional[datetime] = None,
        date_modification: Optional[datetime] = None,
    ):
        """
        Initialise une nouvelle instance de EntiteBase.
        
        Paramètres
        ----------
        id : Optional[int], optional
            Identifiant unique de l'entité, par défaut None
        date_creation : Optional[datetime], optional
            Date et heure de création, par défaut datetime.utcnow()
        date_modification : Optional[datetime], optional
            Date et heure de dernière modification, par défaut datetime.utcnow()
        """
        self.id = id
        self.date_creation = date_creation or datetime.utcnow()
        self.date_modification = date_modification or datetime.utcnow()
