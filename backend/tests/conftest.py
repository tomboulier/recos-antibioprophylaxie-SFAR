"""
Configuration et fixtures générales pour les tests avec pytest.

Ce module contient les fixtures réutilisables dans toute la suite de tests.
"""

import os
import logging
import pytest
from typing import Generator, Dict, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.persistance.database import Base


# Configuration du logger pour les tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def engine():
    """
    Fixture de session qui fournit un moteur SQLAlchemy pour la base de données de test.
    
    Cette fixture utilise une base de données SQLite en mémoire pour les tests.
    
    Yields
    ------
    Engine
        Moteur SQLAlchemy pour les tests
    """
    # Utiliser une base de données SQLite en mémoire pour les tests
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    logger.info("Création du schéma de la base de données de test")
    Base.metadata.create_all(test_engine)
    
    yield test_engine
    
    logger.info("Suppression du schéma de la base de données de test")
    Base.metadata.drop_all(test_engine)


@pytest.fixture(scope="session")
def session_factory(engine) -> sessionmaker:
    """
    Fixture de session qui fournit une factory de session SQLAlchemy.
    
    Paramètres
    ----------
    engine
        Moteur SQLAlchemy fourni par la fixture engine
        
    Retourne
    --------
    sessionmaker
        Factory pour créer des sessions SQLAlchemy
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session(session_factory) -> Generator[Session, None, None]:
    """
    Fixture qui fournit une session SQLAlchemy pour les tests.
    
    Cette fixture crée une nouvelle session pour chaque test et
    effectue un rollback à la fin pour isoler les tests.
    
    Paramètres
    ----------
    session_factory
        Factory de session fournie par la fixture session_factory
        
    Yields
    ------
    Session
        Session SQLAlchemy pour les tests
    """
    session = session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def specialite_test_data() -> Dict[str, Any]:
    """
    Fixture qui fournit des données de test pour une spécialité chirurgicale.
    
    Retourne
    --------
    Dict[str, Any]
        Données de test pour une spécialité chirurgicale
    """
    return {
        "nom": "Chirurgie Orthopédique",
        "description": "Spécialité chirurgicale concernant le système musculo-squelettique."
    }


@pytest.fixture
def intervention_test_data() -> Dict[str, Any]:
    """
    Fixture qui fournit des données de test pour une intervention chirurgicale.
    
    Retourne
    --------
    Dict[str, Any]
        Données de test pour une intervention chirurgicale
    """
    return {
        "nom": "Prothèse totale de hanche",
        "description": "Remplacement complet de l'articulation de la hanche par une prothèse.",
        "facteurs_risque": "Âge > 65 ans, immunodépression, diabète, obésité."
    }


@pytest.fixture
def antibiotique_test_data() -> Dict[str, Any]:
    """
    Fixture qui fournit des données de test pour un antibiotique.
    
    Retourne
    --------
    Dict[str, Any]
        Données de test pour un antibiotique
    """
    return {
        "nom": "Céfazoline",
        "nom_generique": "Céfazoline",
        "description": "Céphalosporine de première génération.",
        "posologie_standard": "2g IV (bolus) chez l'adulte.",
        "contre_indications": "Allergie aux céphalosporines ou aux pénicillines (réaction croisée possible)."
    }


@pytest.fixture
def recommandation_test_data() -> Dict[str, Any]:
    """
    Fixture qui fournit des données de test pour une recommandation d'antibioprophylaxie.
    
    Retourne
    --------
    Dict[str, Any]
        Données de test pour une recommandation d'antibioprophylaxie
    """
    return {
        "posologie": "2g IV (bolus) chez l'adulte.",
        "moment_administration": "30 à 60 minutes avant l'incision",
        "duree_max": "24 heures post-opératoire",
        "reinjection": "1g toutes les 4 heures pendant l'intervention si celle-ci est prolongée",
        "indications_specifiques": "Recommandé pour toutes les poses de prothèses articulaires",
        "niveau_preuve": "Grade A",
        "statut": "active",
        "est_premiere_intention": True
    }
