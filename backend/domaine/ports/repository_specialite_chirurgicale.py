"""
Interface du repository pour les spécialités chirurgicales.

Ce module définit l'interface du repository pour les spécialités chirurgicales,
avec les méthodes spécifiques à cette entité.
"""

from abc import abstractmethod
from typing import List, Optional

from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale
from domaine.ports.repository_base import RepositoryBase


class RepositorySpecialiteChirurgicale(RepositoryBase[SpecialiteChirurgicale]):
    """
    Interface du repository pour les spécialités chirurgicales.
    
    Cette interface étend le repository de base avec des méthodes
    spécifiques aux spécialités chirurgicales.
    """
    
    @abstractmethod
    def obtenir_par_nom(self, nom: str) -> Optional[SpecialiteChirurgicale]:
        """
        Récupère une spécialité chirurgicale par son nom.
        
        Paramètres
        ----------
        nom : str
            Nom de la spécialité chirurgicale à rechercher
            
        Retourne
        --------
        Optional[SpecialiteChirurgicale]
            La spécialité chirurgicale si trouvée, None sinon
        """
        pass
