"""
Service pour les spécialités chirurgicales.

Ce module définit le service gérant les opérations métier liées aux spécialités chirurgicales.
"""

from typing import List, Optional

from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale
from domaine.ports.repository_specialite_chirurgicale import RepositorySpecialiteChirurgicale
from domaine.services.service_base import ServiceBase


class ServiceSpecialiteChirurgicale(ServiceBase[SpecialiteChirurgicale]):
    """
    Service pour les spécialités chirurgicales.
    
    Ce service étend le service de base avec des méthodes spécifiques
    aux spécialités chirurgicales et implémente les règles métier associées.
    
    Attributs
    ---------
    repository : RepositorySpecialiteChirurgicale
        Repository utilisé pour accéder aux données des spécialités chirurgicales
    """
    
    def __init__(self, repository: RepositorySpecialiteChirurgicale):
        """
        Initialise une nouvelle instance du service avec un repository de spécialités chirurgicales.
        
        Paramètres
        ----------
        repository : RepositorySpecialiteChirurgicale
            Repository utilisé pour accéder aux données des spécialités chirurgicales
        """
        super().__init__(repository)
        self.repository_specialite = repository
    
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
        return self.repository_specialite.obtenir_par_nom(nom)
    
    def creer(self, specialite: SpecialiteChirurgicale) -> SpecialiteChirurgicale:
        """
        Crée une nouvelle spécialité chirurgicale après validation.
        
        Paramètres
        ----------
        specialite : SpecialiteChirurgicale
            Spécialité chirurgicale à créer
            
        Retourne
        --------
        SpecialiteChirurgicale
            La spécialité chirurgicale créée avec son identifiant
            
        Lève
        ----
        ValueError
            Si une spécialité chirurgicale avec le même nom existe déjà
        """
        specialite_existante = self.obtenir_par_nom(specialite.nom)
        if specialite_existante:
            raise ValueError(f"Une spécialité chirurgicale avec le nom '{specialite.nom}' existe déjà")
        
        return super().creer(specialite)
    
    def mettre_a_jour(self, specialite: SpecialiteChirurgicale) -> SpecialiteChirurgicale:
        """
        Met à jour une spécialité chirurgicale existante après validation.
        
        Paramètres
        ----------
        specialite : SpecialiteChirurgicale
            Spécialité chirurgicale à mettre à jour
            
        Retourne
        --------
        SpecialiteChirurgicale
            La spécialité chirurgicale mise à jour
            
        Lève
        ----
        ValueError
            Si la spécialité chirurgicale n'existe pas ou si le nouveau nom est déjà utilisé
        """
        if not specialite.id:
            raise ValueError("L'identifiant de la spécialité chirurgicale est requis pour la mise à jour")
            
        specialite_existante = self.obtenir_par_id(specialite.id)
        if not specialite_existante:
            raise ValueError(f"Aucune spécialité chirurgicale trouvée avec l'identifiant {specialite.id}")
            
        specialite_meme_nom = self.obtenir_par_nom(specialite.nom)
        if specialite_meme_nom and specialite_meme_nom.id != specialite.id:
            raise ValueError(f"Une autre spécialité chirurgicale avec le nom '{specialite.nom}' existe déjà")
            
        return super().mettre_a_jour(specialite)
