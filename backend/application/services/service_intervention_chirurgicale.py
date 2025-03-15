"""
Service d'application pour les interventions chirurgicales.

Ce module définit le service d'application pour les interventions chirurgicales,
gérant la conversion entre DTOs et entités du domaine.
"""

import logging
from typing import List, Optional

from application.dto.intervention_chirurgicale_dto import (
    InterventionChirurgicaleCollection,
    InterventionChirurgicaleCreation,
    InterventionChirurgicaleMiseAJour,
    InterventionChirurgicaleReponse,
)
from application.dto.specialite_chirurgicale_dto import SpecialiteChirurgicaleReponse
from application.services.service_application_base import ServiceApplicationBase
from application.services.service_specialite_chirurgicale import ServiceApplicationSpecialiteChirurgicale
from domaine.entites.intervention_chirurgicale import InterventionChirurgicale
from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale
from domaine.services.service_intervention_chirurgicale import ServiceInterventionChirurgicale

# Configuration du logger
logger = logging.getLogger(__name__)


class ServiceApplicationInterventionChirurgicale(
    ServiceApplicationBase[
        InterventionChirurgicale,
        InterventionChirurgicaleCreation,
        InterventionChirurgicaleMiseAJour,
        InterventionChirurgicaleReponse,
        InterventionChirurgicaleCollection,
    ]
):
    """
    Service d'application pour les interventions chirurgicales.
    
    Ce service gère les opérations CRUD pour les interventions chirurgicales,
    en convertissant les DTOs en entités du domaine et vice-versa.
    
    Attributs
    ---------
    service_domaine : ServiceInterventionChirurgicale
        Service domaine pour les interventions chirurgicales
    service_specialite : ServiceApplicationSpecialiteChirurgicale
        Service d'application pour les spécialités chirurgicales
    """
    
    def __init__(
        self, 
        service_domaine: ServiceInterventionChirurgicale,
        service_specialite: ServiceApplicationSpecialiteChirurgicale
    ):
        """
        Initialise une nouvelle instance du service d'application.
        
        Paramètres
        ----------
        service_domaine : ServiceInterventionChirurgicale
            Service domaine pour les interventions chirurgicales
        service_specialite : ServiceApplicationSpecialiteChirurgicale
            Service d'application pour les spécialités chirurgicales
        """
        super().__init__(
            service_domaine=service_domaine,
            response_dto_class=InterventionChirurgicaleReponse,
            collection_dto_class=InterventionChirurgicaleCollection,
        )
        # Pour le typage spécifique
        self.service_domaine_intervention = service_domaine
        self.service_specialite = service_specialite
    
    def obtenir_par_nom(self, nom: str) -> Optional[InterventionChirurgicaleReponse]:
        """
        Récupère une intervention chirurgicale par son nom.
        
        Paramètres
        ----------
        nom : str
            Nom de l'intervention chirurgicale à rechercher
            
        Retourne
        --------
        Optional[InterventionChirurgicaleReponse]
            DTO de réponse si l'intervention est trouvée, None sinon
        """
        intervention = self.service_domaine_intervention.obtenir_par_nom(nom)
        if not intervention:
            logger.info(f"Aucune intervention chirurgicale trouvée avec le nom '{nom}'")
            return None
        
        return self._convertir_entite_vers_dto(intervention)
    
    def obtenir_par_specialite(
        self, specialite_id: int, debut: int = 0, limite: int = 100
    ) -> InterventionChirurgicaleCollection:
        """
        Récupère les interventions chirurgicales par spécialité.
        
        Paramètres
        ----------
        specialite_id : int
            Identifiant de la spécialité chirurgicale
        debut : int, optionnel
            Index de départ pour la pagination, par défaut 0
        limite : int, optionnel
            Nombre maximum d'entités à retourner, par défaut 100
            
        Retourne
        --------
        InterventionChirurgicaleCollection
            Collection d'interventions chirurgicales
            
        Lève
        ----
        ValueError
            Si la spécialité chirurgicale n'existe pas
        """
        try:
            interventions = self.service_domaine_intervention.obtenir_par_specialite(
                specialite_id=specialite_id,
                debut=debut,
                limite=limite
            )
            
            dto_items = [self._convertir_entite_vers_dto(intervention) for intervention in interventions]
            return InterventionChirurgicaleCollection(items=dto_items, total=len(dto_items))
            
        except ValueError as e:
            logger.error(f"Erreur lors de la récupération des interventions par spécialité: {str(e)}")
            raise
    
    def rechercher_par_terme(
        self, terme_recherche: str, debut: int = 0, limite: int = 100
    ) -> InterventionChirurgicaleCollection:
        """
        Recherche des interventions chirurgicales par terme de recherche.
        
        Paramètres
        ----------
        terme_recherche : str
            Terme de recherche à utiliser (correspondance partielle)
        debut : int, optionnel
            Index de départ pour la pagination, par défaut 0
        limite : int, optionnel
            Nombre maximum d'entités à retourner, par défaut 100
            
        Retourne
        --------
        InterventionChirurgicaleCollection
            Collection d'interventions chirurgicales correspondant au terme de recherche
        """
        interventions = self.service_domaine_intervention.rechercher_par_terme(
            terme_recherche=terme_recherche,
            debut=debut,
            limite=limite
        )
        
        dto_items = [self._convertir_entite_vers_dto(intervention) for intervention in interventions]
        return InterventionChirurgicaleCollection(items=dto_items, total=len(dto_items))
    
    def _convertir_entite_vers_dto(self, entite: InterventionChirurgicale) -> InterventionChirurgicaleReponse:
        """
        Convertit une entité intervention chirurgicale en DTO de réponse.
        
        Paramètres
        ----------
        entite : InterventionChirurgicale
            Entité du domaine à convertir
            
        Retourne
        --------
        InterventionChirurgicaleReponse
            DTO de réponse correspondant
        """
        # Convertir les spécialités en DTOs de réponse
        specialites_dto = [
            SpecialiteChirurgicaleReponse(
                id=specialite.id,
                nom=specialite.nom,
                description=specialite.description,
                date_creation=specialite.date_creation,
                date_modification=specialite.date_modification,
            )
            for specialite in entite.specialites if specialite.id is not None
        ]
        
        return InterventionChirurgicaleReponse(
            id=entite.id,
            nom=entite.nom,
            description=entite.description,
            facteurs_risque=entite.facteurs_risque,
            specialites=specialites_dto,
            date_creation=entite.date_creation,
            date_modification=entite.date_modification,
        )
    
    def _convertir_dto_creation_vers_entite(self, dto: InterventionChirurgicaleCreation) -> InterventionChirurgicale:
        """
        Convertit un DTO de création en entité du domaine.
        
        Paramètres
        ----------
        dto : InterventionChirurgicaleCreation
            DTO de création à convertir
            
        Retourne
        --------
        InterventionChirurgicale
            Entité du domaine correspondante
            
        Lève
        ----
        ValueError
            Si une des spécialités associées n'existe pas
        """
        # Récupérer les entités spécialités à partir des IDs
        specialites = []
        for specialite_id in dto.specialites_ids:
            specialite_dto = self.service_specialite.obtenir_par_id(specialite_id)
            if not specialite_dto:
                logger.error(f"La spécialité chirurgicale avec l'identifiant {specialite_id} n'existe pas")
                raise ValueError(f"La spécialité chirurgicale avec l'identifiant {specialite_id} n'existe pas")
            
            # Convertir le DTO en entité domaine (simplifié, en pratique vous utiliseriez une méthode dédiée)
            specialite = SpecialiteChirurgicale(
                id=specialite_dto.id,
                nom=specialite_dto.nom,
                description=specialite_dto.description,
            )
            specialites.append(specialite)
        
        return InterventionChirurgicale(
            nom=dto.nom,
            description=dto.description,
            facteurs_risque=dto.facteurs_risque,
            specialites=specialites,
        )
    
    def _convertir_dto_mise_a_jour_vers_entite(
        self, dto: InterventionChirurgicaleMiseAJour, entite_existante: InterventionChirurgicale
    ) -> InterventionChirurgicale:
        """
        Convertit un DTO de mise à jour en entité du domaine.
        
        Paramètres
        ----------
        dto : InterventionChirurgicaleMiseAJour
            DTO de mise à jour à convertir
        entite_existante : InterventionChirurgicale
            Entité existante à mettre à jour
            
        Retourne
        --------
        InterventionChirurgicale
            Entité du domaine mise à jour
            
        Lève
        ----
        ValueError
            Si une des spécialités associées n'existe pas
        """
        # Si des nouvelles spécialités sont spécifiées, récupérer les entités
        specialites = entite_existante.specialites
        if dto.specialites_ids:
            specialites = []
            for specialite_id in dto.specialites_ids:
                specialite_dto = self.service_specialite.obtenir_par_id(specialite_id)
                if not specialite_dto:
                    logger.error(f"La spécialité chirurgicale avec l'identifiant {specialite_id} n'existe pas")
                    raise ValueError(f"La spécialité chirurgicale avec l'identifiant {specialite_id} n'existe pas")
                
                # Convertir le DTO en entité domaine
                specialite = SpecialiteChirurgicale(
                    id=specialite_dto.id,
                    nom=specialite_dto.nom,
                    description=specialite_dto.description,
                )
                specialites.append(specialite)
        
        # Créer une nouvelle instance avec les valeurs mises à jour
        return InterventionChirurgicale(
            id=entite_existante.id,
            nom=dto.nom if dto.nom is not None else entite_existante.nom,
            description=dto.description if dto.description is not None else entite_existante.description,
            facteurs_risque=dto.facteurs_risque if dto.facteurs_risque is not None else entite_existante.facteurs_risque,
            specialites=specialites,
            date_creation=entite_existante.date_creation,
        )
