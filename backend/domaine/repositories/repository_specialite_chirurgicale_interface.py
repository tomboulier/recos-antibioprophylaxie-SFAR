"""
Interface du repository pour les spécialités chirurgicales.

Ce module définit l'interface de repository pour les spécialités chirurgicales
selon les principes du Domain-Driven Design. Cette interface est indépendante
de toute technologie de persistance spécifique.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale


class RepositorySpecialiteChirurgicaleInterface(ABC):
    """
    Interface du repository pour les spécialités chirurgicales.
    
    Cette interface définit les méthodes que doit implémenter tout repository
    concret pour l'accès aux données des spécialités chirurgicales.
    """
    
    @abstractmethod
    def get_by_id(self, session: Session, id: int) -> Optional[SpecialiteChirurgicale]:
        """
        Récupère une spécialité chirurgicale par son identifiant.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de la spécialité chirurgicale
            
        Returns
        -------
        Optional[SpecialiteChirurgicale]
            La spécialité chirurgicale si trouvée, None sinon
        """
        pass
    
    @abstractmethod
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[SpecialiteChirurgicale]:
        """
        Récupère toutes les spécialités chirurgicales avec pagination.
        
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
        List[SpecialiteChirurgicale]
            Liste des spécialités chirurgicales
        """
        pass
    
    @abstractmethod
    def create(self, session: Session, specialite: SpecialiteChirurgicale) -> Optional[SpecialiteChirurgicale]:
        """
        Crée une nouvelle spécialité chirurgicale.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        specialite : SpecialiteChirurgicale
            Spécialité chirurgicale à créer
            
        Returns
        -------
        Optional[SpecialiteChirurgicale]
            La spécialité chirurgicale créée si succès, None sinon
        """
        pass
    
    @abstractmethod
    def update(self, session: Session, id: int, data: Dict[str, Any]) -> Optional[SpecialiteChirurgicale]:
        """
        Met à jour une spécialité chirurgicale existante.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de la spécialité chirurgicale à mettre à jour
        data : Dict[str, Any]
            Données à mettre à jour
            
        Returns
        -------
        Optional[SpecialiteChirurgicale]
            La spécialité chirurgicale mise à jour si succès, None sinon
        """
        pass
    
    @abstractmethod
    def delete(self, session: Session, id: int) -> bool:
        """
        Supprime une spécialité chirurgicale.
        
        Parameters
        ----------
        session : Session
            Session de base de données
        id : int
            Identifiant de la spécialité chirurgicale à supprimer
            
        Returns
        -------
        bool
            True si la suppression a réussi, False sinon
        """
        pass
    
    @abstractmethod
    def search_by_name(self, session: Session, name: str, skip: int = 0, limit: int = 100) -> List[SpecialiteChirurgicale]:
        """
        Recherche des spécialités chirurgicales par nom.
        
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
        List[SpecialiteChirurgicale]
            Liste des spécialités chirurgicales correspondant à la recherche
        """
        pass
