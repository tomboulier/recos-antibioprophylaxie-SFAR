"""
Définition des dépendances de l'API.

Ce module définit les fonctions qui fournissent les dépendances nécessaires aux routes.
Il s'agit principalement de fournir les services applicatifs qui encapsulent la logique métier.
"""

import logging
from functools import lru_cache
from typing import Generator

from fastapi import Depends

from application.services.service_intervention_chirurgicale import ServiceApplicationInterventionChirurgicale
from application.services.service_specialite_chirurgicale import ServiceApplicationSpecialiteChirurgicale
from domaine.services.service_intervention_chirurgicale import ServiceInterventionChirurgicale
from domaine.services.service_specialite_chirurgicale import ServiceSpecialiteChirurgicale
from infrastructure.persistance.repositories.repository_intervention_chirurgicale import RepositoryInterventionChirurgicale
from infrastructure.persistance.repositories.repository_specialite_chirurgicale import RepositorySpecialiteChirurgicale
from infrastructure.persistance.database import get_session

# Configuration du logger
logger = logging.getLogger(__name__)


# Services du domaine
# Ces fonctions instancient les services métier de la couche domaine
@lru_cache()
def get_repository_specialite_chirurgicale() -> RepositorySpecialiteChirurgicale:
    """
    Fournit un repository pour les spécialités chirurgicales.
    
    Retourne
    --------
    RepositorySpecialiteChirurgicale
        Repository pour accéder aux données des spécialités chirurgicales
    """
    logger.debug("Création du repository pour les spécialités chirurgicales")
    return RepositorySpecialiteChirurgicale(session_factory=get_session)


@lru_cache()
def get_repository_intervention_chirurgicale() -> RepositoryInterventionChirurgicale:
    """
    Fournit un repository pour les interventions chirurgicales.
    
    Retourne
    --------
    RepositoryInterventionChirurgicale
        Repository pour accéder aux données des interventions chirurgicales
    """
    logger.debug("Création du repository pour les interventions chirurgicales")
    return RepositoryInterventionChirurgicale(session_factory=get_session)


@lru_cache()
def get_service_domaine_specialite_chirurgicale(
    repository: RepositorySpecialiteChirurgicale = Depends(get_repository_specialite_chirurgicale),
) -> ServiceSpecialiteChirurgicale:
    """
    Fournit un service domaine pour les spécialités chirurgicales.
    
    Paramètres
    ----------
    repository : RepositorySpecialiteChirurgicale
        Repository pour accéder aux données des spécialités chirurgicales
        
    Retourne
    --------
    ServiceSpecialiteChirurgicale
        Service métier pour les spécialités chirurgicales
    """
    logger.debug("Création du service domaine pour les spécialités chirurgicales")
    return ServiceSpecialiteChirurgicale(repository=repository)


@lru_cache()
def get_service_domaine_intervention_chirurgicale(
    repository: RepositoryInterventionChirurgicale = Depends(get_repository_intervention_chirurgicale),
) -> ServiceInterventionChirurgicale:
    """
    Fournit un service domaine pour les interventions chirurgicales.
    
    Paramètres
    ----------
    repository : RepositoryInterventionChirurgicale
        Repository pour accéder aux données des interventions chirurgicales
        
    Retourne
    --------
    ServiceInterventionChirurgicale
        Service métier pour les interventions chirurgicales
    """
    logger.debug("Création du service domaine pour les interventions chirurgicales")
    return ServiceInterventionChirurgicale(repository=repository)


# Services de l'application
# Ces fonctions instancient les services de la couche application
@lru_cache()
def get_service_specialite_chirurgicale(
    service_domaine: ServiceSpecialiteChirurgicale = Depends(get_service_domaine_specialite_chirurgicale),
) -> ServiceApplicationSpecialiteChirurgicale:
    """
    Fournit un service d'application pour les spécialités chirurgicales.
    
    Paramètres
    ----------
    service_domaine : ServiceSpecialiteChirurgicale
        Service domaine pour les spécialités chirurgicales
        
    Retourne
    --------
    ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales
    """
    logger.debug("Création du service d'application pour les spécialités chirurgicales")
    return ServiceApplicationSpecialiteChirurgicale(service_domaine=service_domaine)


@lru_cache()
def get_service_intervention_chirurgicale(
    service_domaine: ServiceInterventionChirurgicale = Depends(get_service_domaine_intervention_chirurgicale),
    service_specialite: ServiceApplicationSpecialiteChirurgicale = Depends(get_service_specialite_chirurgicale),
) -> ServiceApplicationInterventionChirurgicale:
    """
    Fournit un service d'application pour les interventions chirurgicales.
    
    Paramètres
    ----------
    service_domaine : ServiceInterventionChirurgicale
        Service domaine pour les interventions chirurgicales
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales
        
    Retourne
    --------
    ServiceApplicationInterventionChirurgicale
        Service d'application pour les interventions chirurgicales
    """
    logger.debug("Création du service d'application pour les interventions chirurgicales")
    return ServiceApplicationInterventionChirurgicale(
        service_domaine=service_domaine,
        service_specialite=service_specialite,
    )
