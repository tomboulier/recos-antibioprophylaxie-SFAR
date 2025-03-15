"""
Service d'application pour les spécialités chirurgicales.

Ce module définit le service d'application pour les spécialités chirurgicales,
gérant la conversion entre DTOs et entités du domaine.
"""

import logging
from typing import Optional

from application.dto.specialite_chirurgicale_dto import (
    SpecialiteChirurgicaleCollection,
    SpecialiteChirurgicaleCreation,
    SpecialiteChirurgicaleMiseAJour,
    SpecialiteChirurgicaleReponse,
)
from application.services.service_application_base import ServiceApplicationBase
from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale
from domaine.services.service_specialite_chirurgicale import ServiceSpecialiteChirurgicale

# Configuration du logger
logger = logging.getLogger(__name__)


class ServiceApplicationSpecialiteChirurgicale(
    ServiceApplicationBase[
        SpecialiteChirurgicale,
        SpecialiteChirurgicaleCreation,
        SpecialiteChirurgicaleMiseAJour,
        SpecialiteChirurgicaleReponse,
        SpecialiteChirurgicaleCollection,
    ]
):
    """
    Service d'application pour les spécialités chirurgicales.
    
    Ce service gère les opérations CRUD pour les spécialités chirurgicales,
    en convertissant les DTOs en entités du domaine et vice-versa.
    
    Attributs
    ---------
    service_domaine : ServiceSpecialiteChirurgicale
        Service domaine pour les spécialités chirurgicales
    """
    
    def __init__(self, service_domaine: ServiceSpecialiteChirurgicale):
        """
        Initialise une nouvelle instance du service d'application.
        
        Paramètres
        ----------
        service_domaine : ServiceSpecialiteChirurgicale
            Service domaine pour les spécialités chirurgicales
        """
        super().__init__(
            service_domaine=service_domaine,
            response_dto_class=SpecialiteChirurgicaleReponse,
            collection_dto_class=SpecialiteChirurgicaleCollection,
        )
        # Pour le typage spécifique
        self.service_domaine_specialite = service_domaine
    
    def obtenir_par_nom(self, nom: str) -> Optional[SpecialiteChirurgicaleReponse]:
        """
        Récupère une spécialité chirurgicale par son nom.
        
        Paramètres
        ----------
        nom : str
            Nom de la spécialité chirurgicale à rechercher
            
        Retourne
        --------
        Optional[SpecialiteChirurgicaleReponse]
            DTO de réponse si la spécialité est trouvée, None sinon
        """
        specialite = self.service_domaine_specialite.obtenir_par_nom(nom)
        if not specialite:
            logger.info(f"Aucune spécialité chirurgicale trouvée avec le nom '{nom}'")
            return None
        
        return self._convertir_entite_vers_dto(specialite)
    
    def _convertir_entite_vers_dto(self, entite: SpecialiteChirurgicale) -> SpecialiteChirurgicaleReponse:
        """
        Convertit une entité spécialité chirurgicale en DTO de réponse.
        
        Paramètres
        ----------
        entite : SpecialiteChirurgicale
            Entité du domaine à convertir
            
        Retourne
        --------
        SpecialiteChirurgicaleReponse
            DTO de réponse correspondant
        """
        return SpecialiteChirurgicaleReponse(
            id=entite.id,
            nom=entite.nom,
            description=entite.description,
            date_creation=entite.date_creation,
            date_modification=entite.date_modification,
        )
    
    def _convertir_dto_creation_vers_entite(self, dto: SpecialiteChirurgicaleCreation) -> SpecialiteChirurgicale:
        """
        Convertit un DTO de création en entité du domaine.
        
        Paramètres
        ----------
        dto : SpecialiteChirurgicaleCreation
            DTO de création à convertir
            
        Retourne
        --------
        SpecialiteChirurgicale
            Entité du domaine correspondante
        """
        return SpecialiteChirurgicale(
            nom=dto.nom,
            description=dto.description,
        )
    
    def _convertir_dto_mise_a_jour_vers_entite(
        self, dto: SpecialiteChirurgicaleMiseAJour, entite_existante: SpecialiteChirurgicale
    ) -> SpecialiteChirurgicale:
        """
        Convertit un DTO de mise à jour en entité du domaine.
        
        Paramètres
        ----------
        dto : SpecialiteChirurgicaleMiseAJour
            DTO de mise à jour à convertir
        entite_existante : SpecialiteChirurgicale
            Entité existante à mettre à jour
            
        Retourne
        --------
        SpecialiteChirurgicale
            Entité du domaine mise à jour
        """
        # Créer une nouvelle instance avec les valeurs existantes
        entite_mise_a_jour = SpecialiteChirurgicale(
            id=entite_existante.id,
            nom=dto.nom if dto.nom is not None else entite_existante.nom,
            description=dto.description if dto.description is not None else entite_existante.description,
            date_creation=entite_existante.date_creation,
        )
        
        return entite_mise_a_jour
