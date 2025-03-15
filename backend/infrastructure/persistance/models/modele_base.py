"""
Modèle de base SQLAlchemy.

Ce module définit la classe de base dont héritent tous les modèles SQLAlchemy.
"""

import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from infrastructure.persistance.database import Base


class ModeleBase:
    """
    Classe de base pour tous les modèles SQLAlchemy.
    
    Cette classe fournit des fonctionnalités communes comme :
    - Nommage automatique des tables (basé sur le nom de la classe)
    - Identifiant autoincrémenté
    - Timestamps de création et de modification
    - Méthodes de conversion vers dictionnaire
    
    Attributs
    ---------
    id : int
        Identifiant unique autoincrémenté
    date_creation : datetime
        Date et heure de création de l'enregistrement
    date_modification : datetime
        Date et heure de la dernière modification de l'enregistrement
    """
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Génère le nom de la table automatiquement à partir du nom de la classe.
        
        Le nom de la table sera le nom de la classe en minuscules avec un 's' ajouté
        pour indiquer le pluriel.
        
        Retourne
        --------
        str
            Nom de la table en base de données
        """
        return cls.__name__.lower() + "s"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le modèle en dictionnaire.
        
        Retourne
        --------
        Dict[str, Any]
            Dictionnaire représentant le modèle
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
