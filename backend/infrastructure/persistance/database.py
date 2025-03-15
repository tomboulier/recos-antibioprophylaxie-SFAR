"""
Configuration de la base de données.

Ce module gère la connexion à la base de données et fournit une session SQLAlchemy.
"""

import logging
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Configuration du logger
logger = logging.getLogger(__name__)

# Configuration de la base de données
# Utilisation d'une variable d'environnement pour la configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./antibioprophylaxie.db"
)

# Création du moteur de base de données
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,  # Mettre à True pour voir les requêtes SQL
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles déclaratifs
Base = declarative_base()


def get_session() -> Generator[Session, None, None]:
    """
    Crée une nouvelle session de base de données à utiliser dans un contexte.
    
    Cette fonction est destinée à être utilisée comme une dépendance FastAPI,
    garantissant que la session est correctement fermée après utilisation.
    
    Yields
    ------
    Generator[Session, None, None]
        Session SQLAlchemy
    """
    session = SessionLocal()
    try:
        logger.debug("Ouverture d'une nouvelle session de base de données")
        yield session
    finally:
        logger.debug("Fermeture de la session de base de données")
        session.close()


def init_db() -> None:
    """
    Initialise la base de données en créant toutes les tables.
    
    Cette fonction doit être appelée lors du démarrage de l'application
    si la création des tables est nécessaire.
    """
    logger.info("Initialisation de la base de données")
    
    # Import des modèles pour s'assurer qu'ils sont enregistrés avec Base
    # avant de créer les tables
    from infrastructure.persistance.models import (
        modele_specialite_chirurgicale,
        modele_intervention_chirurgicale,
        modele_antibiotique,
        modele_recommandation_antibioprophylaxie,
    )
    
    Base.metadata.create_all(bind=engine)
    logger.info("Base de données initialisée avec succès")
