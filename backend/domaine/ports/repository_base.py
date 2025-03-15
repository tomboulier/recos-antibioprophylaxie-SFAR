"""
Interface de base pour tous les repositories.

Ce module définit l'interface générique pour tous les repositories
suivant le pattern Repository, assurant l'indépendance du domaine.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from domaine.entites.entite_base import EntiteBase

# Type générique pour les entités
T = TypeVar('T', bound=EntiteBase)


class RepositoryBase(Generic[T], ABC):
    """
    Interface de base pour tous les repositories.
    
    Cette interface abstraite définit les méthodes que tous les
    repositories doivent implémenter, quelle que soit la technologie
    de persistance sous-jacente.
    """
    
    @abstractmethod
    def obtenir_par_id(self, id_entite: int) -> Optional[T]:
        """
        Récupère une entité par son identifiant.
        
        Paramètres
        ----------
        id_entite : int
            Identifiant de l'entité à récupérer
            
        Retourne
        --------
        Optional[T]
            L'entité si trouvée, None sinon
        """
        pass
    
    @abstractmethod
    def obtenir_tous(self, debut: int = 0, limite: int = 100) -> List[T]:
        """
        Récupère toutes les entités avec pagination.
        
        Paramètres
        ----------
        debut : int, optionnel
            Index de départ pour la pagination, par défaut 0
        limite : int, optionnel
            Nombre maximum d'entités à retourner, par défaut 100
            
        Retourne
        --------
        List[T]
            Liste des entités
        """
        pass
    
    @abstractmethod
    def creer(self, entite: T) -> T:
        """
        Crée une nouvelle entité.
        
        Paramètres
        ----------
        entite : T
            Entité à créer
            
        Retourne
        --------
        T
            L'entité créée avec son identifiant
        """
        pass
    
    @abstractmethod
    def mettre_a_jour(self, entite: T) -> T:
        """
        Met à jour une entité existante.
        
        Paramètres
        ----------
        entite : T
            Entité à mettre à jour
            
        Retourne
        --------
        T
            L'entité mise à jour
        """
        pass
    
    @abstractmethod
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
        pass
