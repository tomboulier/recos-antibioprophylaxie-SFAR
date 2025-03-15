"""
Service pour les antibiotiques.

Ce module définit le service gérant les opérations métier liées aux antibiotiques.
"""

from typing import List, Optional

from domaine.entites.antibiotique import Antibiotique
from domaine.ports.repository_antibiotique import RepositoryAntibiotique
from domaine.services.service_base import ServiceBase


class ServiceAntibiotique(ServiceBase[Antibiotique]):
    """
    Service pour les antibiotiques.
    
    Ce service étend le service de base avec des méthodes spécifiques
    aux antibiotiques et implémente les règles métier associées.
    
    Attributs
    ---------
    repository_antibiotique : RepositoryAntibiotique
        Repository utilisé pour accéder aux données des antibiotiques
    """
    
    def __init__(self, repository_antibiotique: RepositoryAntibiotique):
        """
        Initialise une nouvelle instance du service avec un repository d'antibiotiques.
        
        Paramètres
        ----------
        repository_antibiotique : RepositoryAntibiotique
            Repository utilisé pour accéder aux données des antibiotiques
        """
        super().__init__(repository_antibiotique)
        self.repository_antibiotique = repository_antibiotique
    
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
        return self.repository_antibiotique.obtenir_par_nom(nom)
    
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
        return self.repository_antibiotique.rechercher_par_terme(
            terme_recherche=terme_recherche,
            debut=debut,
            limite=limite
        )
    
    def creer(self, antibiotique: Antibiotique) -> Antibiotique:
        """
        Crée un nouvel antibiotique après validation.
        
        Paramètres
        ----------
        antibiotique : Antibiotique
            Antibiotique à créer
            
        Retourne
        --------
        Antibiotique
            L'antibiotique créé avec son identifiant
            
        Lève
        ----
        ValueError
            Si un antibiotique avec le même nom existe déjà
        """
        antibiotique_existant = self.obtenir_par_nom(antibiotique.nom)
        if antibiotique_existant:
            raise ValueError(f"Un antibiotique avec le nom '{antibiotique.nom}' existe déjà")
        
        return super().creer(antibiotique)
    
    def mettre_a_jour(self, antibiotique: Antibiotique) -> Antibiotique:
        """
        Met à jour un antibiotique existant après validation.
        
        Paramètres
        ----------
        antibiotique : Antibiotique
            Antibiotique à mettre à jour
            
        Retourne
        --------
        Antibiotique
            L'antibiotique mis à jour
            
        Lève
        ----
        ValueError
            Si l'antibiotique n'existe pas ou si le nouveau nom est déjà utilisé
        """
        if not antibiotique.id:
            raise ValueError("L'identifiant de l'antibiotique est requis pour la mise à jour")
            
        antibiotique_existant = self.obtenir_par_id(antibiotique.id)
        if not antibiotique_existant:
            raise ValueError(f"Aucun antibiotique trouvé avec l'identifiant {antibiotique.id}")
            
        antibiotique_meme_nom = self.obtenir_par_nom(antibiotique.nom)
        if antibiotique_meme_nom and antibiotique_meme_nom.id != antibiotique.id:
            raise ValueError(f"Un autre antibiotique avec le nom '{antibiotique.nom}' existe déjà")
            
        return super().mettre_a_jour(antibiotique)
