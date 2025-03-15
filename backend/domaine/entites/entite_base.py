"""
Entité de base pour toutes les entités du domaine.

Cette classe fournit les fonctionnalités communes à toutes les entités,
notamment la gestion de l'identifiant unique.
"""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
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
    
    id: Optional[int] = None
    date_creation: datetime = field(default_factory=datetime.utcnow)
    date_modification: datetime = field(default_factory=datetime.utcnow)
