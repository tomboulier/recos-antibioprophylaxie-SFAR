"""
Interface du repository pour les interventions chirurgicales.

Ce module définit l'interface de repository pour les interventions chirurgicales
selon les principes du Domain-Driven Design. Cette interface est indépendante
de toute technologie de persistance spécifique.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from domaine.entites.intervention_chirurgicale import InterventionChirurgicale


class RepositoryInterventionChirurgicaleInterface(ABC):
    """
    Interface du repository pour les interventions chirurgicales.
    
    Cette interface définit les méthodes que doit implémenter tout repository
    concret pour l'accès aux données des interventions chirurgicales.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
