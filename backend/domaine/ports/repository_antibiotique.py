"""
Interface du repository pour les antibiotiques.

Ce module définit l'interface du repository pour les antibiotiques,
avec les méthodes spécifiques à cette entité.
"""

from abc import abstractmethod
from typing import List, Optional

from domaine.entites.antibiotique import Antibiotique
from domaine.ports.repository_base import RepositoryBase


class RepositoryAntibiotique(RepositoryBase[Antibiotique]):
    """
    Interface du repository pour les antibiotiques.
    
    Cette interface étend le repository de base avec des méthodes
    spécifiques aux antibiotiques.
    """
    
    @abstractmethod
    def obtenir_par_nom(self, nom: str) -> Optional[Antibiotique]:
        """
        Récupère un antibiotique par son nom.
        
        Paramètres
        ----------
        nom : str
            Nom de l'antibiotique à rechercher
            
        Retourne
        --------
        Optional[Antibiotique]
            L'antibiotique si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def rechercher_par_terme(self, terme_recherche: str, debut: int = 0, limite: int = 100) -> List[Antibiotique]:
        """
        Recherche des antibiotiques par terme de recherche.
        
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
        List[Antibiotique]
            Liste des antibiotiques correspondant au terme de recherche
        """
        pass
