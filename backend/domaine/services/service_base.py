"""
Service de base pour tous les services du domaine.

Ce module définit une classe de service générique qui fournit
les opérations CRUD de base pour les entités du domaine.
"""

from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from domaine.entites.entite_base import EntiteBase
from domaine.ports.repository_base import RepositoryBase

# Type générique pour les entités
T = TypeVar('T', bound=EntiteBase)


class ServiceBase(Generic[T], ABC):
    """
    Service de base pour toutes les entités du domaine.
    
    Cette classe fournit les opérations CRUD de base pour toutes
    les entités du domaine, en utilisant le repository correspondant.
    
    Attributs
    ---------
    repository : RepositoryBase[T]
        Repository utilisé pour accéder aux données
    """
    
    def __init__(self, repository: RepositoryBase[T]):
        """
        Initialise une nouvelle instance du service avec un repository.
        
        Paramètres
        ----------
        repository : RepositoryBase[T]
            Repository utilisé pour accéder aux données
        """
        self.repository = repository
    
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
        return self.repository.obtenir_par_id(id_entite)
    
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
        return self.repository.obtenir_tous(debut=debut, limite=limite)
    
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
        return self.repository.creer(entite)
    
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
        return self.repository.mettre_a_jour(entite)
    
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
        return self.repository.supprimer(id_entite)
