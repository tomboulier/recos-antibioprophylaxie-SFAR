"""
Interface du repository pour les recommandations d'antibioprophylaxie.

Ce module définit l'interface du repository pour les recommandations d'antibioprophylaxie,
avec les méthodes spécifiques à cette entité.
"""

from abc import abstractmethod
from typing import List, Optional

from domaine.entites.recommandation_antibioprophylaxie import RecommandationAntibioprophylaxie
from domaine.ports.repository_base import RepositoryBase


class RepositoryRecommandationAntibioprophylaxie(RepositoryBase[RecommandationAntibioprophylaxie]):
    """
    Interface du repository pour les recommandations d'antibioprophylaxie.
    
    Cette interface étend le repository de base avec des méthodes
    spécifiques aux recommandations d'antibioprophylaxie.
    """
    
    @abstractmethod
    def obtenir_par_intervention(self, intervention_id: int) -> List[RecommandationAntibioprophylaxie]:
        """
        Récupère les recommandations d'antibioprophylaxie pour une intervention donnée.
        
        Paramètres
        ----------
        intervention_id : int
            Identifiant de l'intervention chirurgicale
            
        Retourne
        --------
        List[RecommandationAntibioprophylaxie]
            Liste des recommandations d'antibioprophylaxie pour l'intervention
        """
        pass
    
    @abstractmethod
    def obtenir_par_antibiotique(self, antibiotique_id: int, debut: int = 0, limite: int = 100) -> List[RecommandationAntibioprophylaxie]:
        """
        Récupère les recommandations d'antibioprophylaxie utilisant un antibiotique donné.
        
        Paramètres
        ----------
        antibiotique_id : int
            Identifiant de l'antibiotique
        debut : int, optionnel
            Index de départ pour la pagination, par défaut 0
        limite : int, optionnel
            Nombre maximum d'entités à retourner, par défaut 100
            
        Retourne
        --------
        List[RecommandationAntibioprophylaxie]
            Liste des recommandations d'antibioprophylaxie utilisant l'antibiotique
        """
        pass
    
    @abstractmethod
    def obtenir_par_specialite(self, specialite_id: int, debut: int = 0, limite: int = 100) -> List[RecommandationAntibioprophylaxie]:
        """
        Récupère les recommandations d'antibioprophylaxie pour une spécialité donnée.
        
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
        List[RecommandationAntibioprophylaxie]
            Liste des recommandations d'antibioprophylaxie pour la spécialité
        """
        pass
