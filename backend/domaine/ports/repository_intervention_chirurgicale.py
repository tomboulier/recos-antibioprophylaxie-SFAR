"""
Interface du repository pour les interventions chirurgicales.

Ce module définit l'interface du repository pour les interventions chirurgicales,
avec les méthodes spécifiques à cette entité.
"""

from abc import abstractmethod
from typing import List, Optional

from domaine.entites.intervention_chirurgicale import InterventionChirurgicale
from domaine.ports.repository_base import RepositoryBase


class RepositoryInterventionChirurgicale(RepositoryBase[InterventionChirurgicale]):
    """
    Interface du repository pour les interventions chirurgicales.
    
    Cette interface étend le repository de base avec des méthodes
    spécifiques aux interventions chirurgicales.
    """
    
    @abstractmethod
    def obtenir_par_nom(self, nom: str) -> Optional[InterventionChirurgicale]:
        """
        Récupère une intervention chirurgicale par son nom.
        
        Paramètres
        ----------
        nom : str
            Nom de l'intervention chirurgicale à rechercher
            
        Retourne
        --------
        Optional[InterventionChirurgicale]
            L'intervention chirurgicale si trouvée, None sinon
        """
        pass
    
    @abstractmethod
    def obtenir_par_specialite(self, specialite_id: int, debut: int = 0, limite: int = 100) -> List[InterventionChirurgicale]:
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
        List[InterventionChirurgicale]
            Liste des interventions chirurgicales appartenant à la spécialité
        """
        pass
    
    @abstractmethod
    def rechercher_par_terme(self, terme_recherche: str, debut: int = 0, limite: int = 100) -> List[InterventionChirurgicale]:
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
        List[InterventionChirurgicale]
            Liste des interventions chirurgicales correspondant au terme de recherche
        """
        pass
