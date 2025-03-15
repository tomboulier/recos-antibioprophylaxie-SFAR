"""
Repository pour les interventions chirurgicales.

Ce module implémente l'interface de repository définie dans le domaine pour l'accès
aux données des interventions chirurgicales.
"""

import logging
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from domaine.entites.intervention_chirurgicale import InterventionChirurgicale
from domaine.repositories.repository_intervention_chirurgicale_interface import RepositoryInterventionChirurgicaleInterface

# Configuration du logger
logger = logging.getLogger(__name__)


class RepositoryInterventionChirurgicale(RepositoryInterventionChirurgicaleInterface):
    """
    Implémentation SQLAlchemy du repository pour les interventions chirurgicales.
    
    Cette classe implémente les méthodes définies dans l'interface du repository
    pour la persistance des interventions chirurgicales.
    """
    
    def __init__(self) -> None:
        """Initialise le repository."""
        super().__init__()
    
    def get_by_id(self, session: Session, id: int) -> Optional[InterventionChirurgicale]:
        """
        Récupère une intervention chirurgicale par son identifiant.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de l'intervention chirurgicale
            
        Returns
        -------
        Optional[InterventionChirurgicale]
            L'intervention chirurgicale si trouvée, None sinon
        """
        try:
            # Implémentation temporaire pour le développement
            # Dans une version réelle, cette méthode interrogerait la base de données
            # via un modèle SQLAlchemy
            logger.info(f"Recherche de l'intervention chirurgicale avec l'id {id}")
            
            # Simulation d'une requête à la base de données
            # Retourne un objet statique pour le développement
            if id == 1:
                return InterventionChirurgicale(
                    id=1,
                    nom="Dérivation ventriculaire externe (DVE)",
                    description="Mise en place d'une dérivation du LCS ventriculaire vers l'extérieur",
                    specialites_ids=[1]  # Neurochirurgie
                )
            elif id == 2:
                return InterventionChirurgicale(
                    id=2,
                    nom="Dérivation lombaire externe (DLE)",
                    description="Mise en place d'une dérivation du LCS lombaire vers l'extérieur",
                    specialites_ids=[1]  # Neurochirurgie
                )
            # Autres interventions simulées...
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la récupération de l'intervention chirurgicale {id}: {str(e)}")
            return None
    
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[InterventionChirurgicale]:
        """
        Récupère toutes les interventions chirurgicales avec pagination.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        skip : int, optional
            Nombre d'éléments à sauter, par défaut 0
        limit : int, optional
            Nombre maximum d'éléments à retourner, par défaut 100
            
        Returns
        -------
        List[InterventionChirurgicale]
            Liste des interventions chirurgicales
        """
        try:
            logger.info(f"Récupération des interventions chirurgicales (skip={skip}, limit={limit})")
            
            # Simulation de données pour le développement
            interventions = [
                InterventionChirurgicale(
                    id=1,
                    nom="Dérivation ventriculaire externe (DVE)",
                    description="Mise en place d'une dérivation du LCS ventriculaire vers l'extérieur",
                    specialites_ids=[1]  # Neurochirurgie
                ),
                InterventionChirurgicale(
                    id=2,
                    nom="Dérivation lombaire externe (DLE)",
                    description="Mise en place d'une dérivation du LCS lombaire vers l'extérieur",
                    specialites_ids=[1]  # Neurochirurgie
                ),
                InterventionChirurgicale(
                    id=3,
                    nom="Dérivation ventriculo-péritonéale (DVP)",
                    description="Mise en place d'une dérivation du LCS ventriculaire vers le péritoine",
                    specialites_ids=[1]  # Neurochirurgie
                ),
                InterventionChirurgicale(
                    id=4,
                    nom="Dérivation ventriculo-atriale (DVA)",
                    description="Mise en place d'une dérivation du LCS ventriculaire vers l'oreillette droite",
                    specialites_ids=[1]  # Neurochirurgie
                ),
                InterventionChirurgicale(
                    id=5,
                    nom="Cystectomie sustrigonale partielle ou totale, quel que soit le mode de dérivation",
                    description="Ablation partielle ou totale de la vessie au-dessus du trigone vésical",
                    specialites_ids=[3]  # Urologie
                ),
                InterventionChirurgicale(
                    id=6,
                    nom="Chirurgie gastro-duodénale",
                    description="Intervention chirurgicale sur l'estomac et/ou le duodénum",
                    specialites_ids=[2]  # Chirurgie digestive
                ),
                InterventionChirurgicale(
                    id=7,
                    nom="Chirurgie colo-rectale",
                    description="Intervention chirurgicale sur le côlon et/ou le rectum",
                    specialites_ids=[2]  # Chirurgie digestive
                ),
                InterventionChirurgicale(
                    id=8,
                    nom="Chirurgie hépato-biliaire",
                    description="Intervention chirurgicale sur le foie et/ou les voies biliaires",
                    specialites_ids=[2]  # Chirurgie digestive
                ),
                InterventionChirurgicale(
                    id=9,
                    nom="Chirurgie pancréatique",
                    description="Intervention chirurgicale sur le pancréas",
                    specialites_ids=[2]  # Chirurgie digestive
                ),
                InterventionChirurgicale(
                    id=10,
                    nom="Prothèse de hanche",
                    description="Mise en place d'une prothèse articulaire de la hanche",
                    specialites_ids=[4]  # Orthopédie
                ),
                InterventionChirurgicale(
                    id=11,
                    nom="Prothèse de genou",
                    description="Mise en place d'une prothèse articulaire du genou",
                    specialites_ids=[4]  # Orthopédie
                ),
                InterventionChirurgicale(
                    id=12,
                    nom="Chirurgie rachidienne",
                    description="Intervention chirurgicale sur la colonne vertébrale",
                    specialites_ids=[4, 1]  # Orthopédie, Neurochirurgie
                ),
                InterventionChirurgicale(
                    id=13,
                    nom="Arthroscopie",
                    description="Examen endoscopique d'une articulation",
                    specialites_ids=[4]  # Orthopédie
                )
            ]
            
            # Application de la pagination
            start = skip
            end = skip + limit
            return interventions[start:end]
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la récupération des interventions chirurgicales: {str(e)}")
            return []
    
    def get_by_specialite(self, session: Session, specialite_id: int, skip: int = 0, limit: int = 100) -> List[InterventionChirurgicale]:
        """
        Récupère les interventions chirurgicales pour une spécialité donnée.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        specialite_id : int
            Identifiant de la spécialité
        skip : int, optional
            Nombre d'éléments à sauter, par défaut 0
        limit : int, optional
            Nombre maximum d'éléments à retourner, par défaut 100
            
        Returns
        -------
        List[InterventionChirurgicale]
            Liste des interventions chirurgicales pour la spécialité
        """
        try:
            logger.info(f"Récupération des interventions pour la spécialité {specialite_id}")
            
            # Récupérer toutes les interventions puis filtrer
            all_interventions = self.get_all(session, 0, 1000)  # Récupérer un grand nombre pour la simulation
            
            # Filtrer les interventions qui appartiennent à la spécialité demandée
            filtered_interventions = [
                intervention for intervention in all_interventions
                if specialite_id in intervention.specialites_ids
            ]
            
            # Appliquer la pagination
            start = skip
            end = skip + limit
            return filtered_interventions[start:end]
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la récupération des interventions pour la spécialité {specialite_id}: {str(e)}")
            return []
    
    def search_by_name(self, session: Session, name: str, skip: int = 0, limit: int = 100) -> List[InterventionChirurgicale]:
        """
        Recherche des interventions chirurgicales par nom.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        name : str
            Terme de recherche (au moins 3 caractères)
        skip : int, optional
            Nombre d'éléments à sauter, par défaut 0
        limit : int, optional
            Nombre maximum d'éléments à retourner, par défaut 100
            
        Returns
        -------
        List[InterventionChirurgicale]
            Liste des interventions chirurgicales correspondant à la recherche
        """
        try:
            logger.info(f"Recherche d'interventions avec le terme '{name}'")
            
            if len(name) < 3:
                logger.warning("Terme de recherche trop court (minimum 3 caractères)")
                return []
            
            # Récupérer toutes les interventions puis filtrer
            all_interventions = self.get_all(session, 0, 1000)  # Récupérer un grand nombre pour la simulation
            
            # Filtrer les interventions dont le nom contient le terme recherché (insensible à la casse)
            # et normaliser les accents
            normalized_search = name.lower().strip()
            
            # Recherche simple pour la simulation
            filtered_interventions = [
                intervention for intervention in all_interventions
                if normalized_search in intervention.nom.lower()
            ]
            
            # Appliquer la pagination
            start = skip
            end = skip + limit
            return filtered_interventions[start:end]
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la recherche d'interventions avec le terme '{name}': {str(e)}")
            return []
    
    def create(self, session: Session, intervention: InterventionChirurgicale) -> Optional[InterventionChirurgicale]:
        """
        Crée une nouvelle intervention chirurgicale.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        intervention : InterventionChirurgicale
            Intervention chirurgicale à créer
            
        Returns
        -------
        Optional[InterventionChirurgicale]
            L'intervention chirurgicale créée si succès, None sinon
        """
        try:
            logger.info(f"Création de l'intervention chirurgicale: {intervention.nom}")
            
            # Dans une implémentation réelle, nous ajouterions l'entité à la base de données
            # Pour la simulation, nous retournons simplement l'entité avec un ID généré
            intervention.id = 999  # ID fictif pour la simulation
            
            return intervention
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la création de l'intervention chirurgicale: {str(e)}")
            return None
    
    def update(self, session: Session, id: int, data: Dict[str, Any]) -> Optional[InterventionChirurgicale]:
        """
        Met à jour une intervention chirurgicale existante.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de l'intervention chirurgicale à mettre à jour
        data : Dict[str, Any]
            Données à mettre à jour
            
        Returns
        -------
        Optional[InterventionChirurgicale]
            L'intervention chirurgicale mise à jour si succès, None sinon
        """
        try:
            logger.info(f"Mise à jour de l'intervention chirurgicale {id}")
            
            # Récupérer l'intervention existante
            intervention = self.get_by_id(session, id)
            if not intervention:
                logger.warning(f"Intervention chirurgicale {id} non trouvée")
                return None
            
            # Mettre à jour les attributs
            if "nom" in data:
                intervention.nom = data["nom"]
            if "description" in data:
                intervention.description = data["description"]
            if "specialites_ids" in data:
                intervention.specialites_ids = data["specialites_ids"]
            
            # Dans une implémentation réelle, nous mettrions à jour l'entité dans la base de données
            # Pour la simulation, nous retournons simplement l'entité modifiée
            
            return intervention
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la mise à jour de l'intervention chirurgicale {id}: {str(e)}")
            return None
    
    def delete(self, session: Session, id: int) -> bool:
        """
        Supprime une intervention chirurgicale.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de l'intervention chirurgicale à supprimer
            
        Returns
        -------
        bool
            True si la suppression a réussi, False sinon
        """
        try:
            logger.info(f"Suppression de l'intervention chirurgicale {id}")
            
            # Vérifier si l'intervention existe
            intervention = self.get_by_id(session, id)
            if not intervention:
                logger.warning(f"Intervention chirurgicale {id} non trouvée")
                return False
            
            # Dans une implémentation réelle, nous supprimerions l'entité de la base de données
            # Pour la simulation, nous retournons simplement True
            
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Erreur lors de la suppression de l'intervention chirurgicale {id}: {str(e)}")
            return False
