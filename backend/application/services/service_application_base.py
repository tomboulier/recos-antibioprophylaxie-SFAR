"""
Service de base pour la couche application.

Ce module définit une classe de service générique pour la couche application,
gérant la conversion entre les entités domaine et les DTOs.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, Type, TypeVar, cast

from pydantic import BaseModel

from application.dto.dto_base import DTOBase
from domaine.entites.entite_base import EntiteBase
from domaine.services.service_base import ServiceBase

# Définition des types génériques
T = TypeVar('T', bound=EntiteBase)  # Type d'entité domaine
CreateDTO = TypeVar('CreateDTO', bound=BaseModel)  # DTO de création
UpdateDTO = TypeVar('UpdateDTO', bound=BaseModel)  # DTO de mise à jour
ResponseDTO = TypeVar('ResponseDTO', bound=DTOBase)  # DTO de réponse
CollectionDTO = TypeVar('CollectionDTO', bound=DTOBase)  # DTO de collection

# Configuration du logger
logger = logging.getLogger(__name__)


class ServiceApplicationBase(Generic[T, CreateDTO, UpdateDTO, ResponseDTO, CollectionDTO], ABC):
    """
    Classe abstraite de base pour les services de la couche application.
    
    Cette classe gère la conversion entre entités du domaine et DTOs, et délègue
    les opérations métier au service de domaine correspondant.
    
    Attributs
    ---------
    service_domaine : ServiceBase[T]
        Service de domaine utilisé pour effectuer les opérations métier
    response_dto_class : Type[ResponseDTO]
        Classe du DTO de réponse
    collection_dto_class : Type[CollectionDTO]
        Classe du DTO de collection
    """
    
    def __init__(
        self, 
        service_domaine: ServiceBase[T],
        response_dto_class: Type[ResponseDTO],
        collection_dto_class: Type[CollectionDTO]
    ):
        """
        Initialise une nouvelle instance du service application.
        
        Paramètres
        ----------
        service_domaine : ServiceBase[T]
            Service de domaine utilisé pour effectuer les opérations métier
        response_dto_class : Type[ResponseDTO]
            Classe du DTO de réponse
        collection_dto_class : Type[CollectionDTO]
            Classe du DTO de collection
        """
        self.service_domaine = service_domaine
        self.response_dto_class = response_dto_class
        self.collection_dto_class = collection_dto_class
    
    def obtenir_par_id(self, id_entite: int) -> Optional[ResponseDTO]:
        """
        Récupère une entité par son identifiant et la convertit en DTO.
        
        Paramètres
        ----------
        id_entite : int
            Identifiant de l'entité à récupérer
            
        Retourne
        --------
        Optional[ResponseDTO]
            DTO de réponse si l'entité est trouvée, None sinon
        """
        entite = self.service_domaine.obtenir_par_id(id_entite)
        if not entite:
            logger.info(f"Aucune entité trouvée avec l'identifiant {id_entite}")
            return None
        
        return self._convertir_entite_vers_dto(entite)
    
    def obtenir_tous(self, debut: int = 0, limite: int = 100) -> CollectionDTO:
        """
        Récupère toutes les entités avec pagination et les convertit en DTOs.
        
        Paramètres
        ----------
        debut : int, optionnel
            Index de départ pour la pagination, par défaut 0
        limite : int, optionnel
            Nombre maximum d'entités à retourner, par défaut 100
            
        Retourne
        --------
        CollectionDTO
            DTO de collection contenant les entités converties
        """
        entites = self.service_domaine.obtenir_tous(debut=debut, limite=limite)
        total = len(entites)  # À remplacer par un compte réel dans une implémentation plus avancée
        
        dto_items = [self._convertir_entite_vers_dto(entite) for entite in entites]
        return self.collection_dto_class(items=dto_items, total=total)
    
    def creer(self, dto_creation: CreateDTO) -> ResponseDTO:
        """
        Crée une nouvelle entité à partir d'un DTO de création.
        
        Paramètres
        ----------
        dto_creation : CreateDTO
            DTO contenant les données pour la création
            
        Retourne
        --------
        ResponseDTO
            DTO de réponse pour l'entité créée
        """
        entite = self._convertir_dto_creation_vers_entite(dto_creation)
        entite_creee = self.service_domaine.creer(entite)
        
        logger.info(f"Entité créée avec succès, id: {entite_creee.id}")
        return self._convertir_entite_vers_dto(entite_creee)
    
    def mettre_a_jour(self, id_entite: int, dto_mise_a_jour: UpdateDTO) -> ResponseDTO:
        """
        Met à jour une entité existante à partir d'un DTO de mise à jour.
        
        Paramètres
        ----------
        id_entite : int
            Identifiant de l'entité à mettre à jour
        dto_mise_a_jour : UpdateDTO
            DTO contenant les données pour la mise à jour
            
        Retourne
        --------
        ResponseDTO
            DTO de réponse pour l'entité mise à jour
            
        Lève
        ----
        ValueError
            Si l'entité n'existe pas
        """
        entite_existante = self.service_domaine.obtenir_par_id(id_entite)
        if not entite_existante:
            logger.error(f"Tentative de mise à jour d'une entité inexistante, id: {id_entite}")
            raise ValueError(f"Aucune entité trouvée avec l'identifiant {id_entite}")
        
        entite_mise_a_jour = self._convertir_dto_mise_a_jour_vers_entite(dto_mise_a_jour, entite_existante)
        entite_mise_a_jour.id = id_entite  # S'assurer que l'ID est préservé
        
        entite_sauvegardee = self.service_domaine.mettre_a_jour(entite_mise_a_jour)
        logger.info(f"Entité mise à jour avec succès, id: {entite_sauvegardee.id}")
        
        return self._convertir_entite_vers_dto(entite_sauvegardee)
    
    def supprimer(self, id_entite: int) -> bool:
        """
        Supprime une entité par son identifiant.
        
        Paramètres
        ----------
        id_entite : int
            Identifiant de l'entité à supprimer
            
        Retourne
        --------
        bool
            True si la suppression a réussi, False sinon
        """
        resultat = self.service_domaine.supprimer(id_entite)
        if resultat:
            logger.info(f"Entité supprimée avec succès, id: {id_entite}")
        else:
            logger.warning(f"Tentative de suppression d'une entité inexistante, id: {id_entite}")
        
        return resultat
    
    @abstractmethod
    def _convertir_entite_vers_dto(self, entite: T) -> ResponseDTO:
        """
        Convertit une entité du domaine en DTO de réponse.
        
        Paramètres
        ----------
        entite : T
            Entité du domaine à convertir
            
        Retourne
        --------
        ResponseDTO
            DTO de réponse correspondant
        """
        pass
    
    @abstractmethod
    def _convertir_dto_creation_vers_entite(self, dto: CreateDTO) -> T:
        """
        Convertit un DTO de création en entité du domaine.
        
        Paramètres
        ----------
        dto : CreateDTO
            DTO de création à convertir
            
        Retourne
        --------
        T
            Entité du domaine correspondante
        """
        pass
    
    @abstractmethod
    def _convertir_dto_mise_a_jour_vers_entite(self, dto: UpdateDTO, entite_existante: T) -> T:
        """
        Convertit un DTO de mise à jour en entité du domaine, en conservant 
        les valeurs existantes pour les champs non spécifiés.
        
        Paramètres
        ----------
        dto : UpdateDTO
            DTO de mise à jour à convertir
        entite_existante : T
            Entité existante à mettre à jour
            
        Retourne
        --------
        T
            Entité du domaine mise à jour
        """
        pass
