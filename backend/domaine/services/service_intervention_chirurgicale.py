"""
Service pour les interventions chirurgicales.

Ce module définit le service gérant les opérations métier liées aux interventions chirurgicales.
"""

from typing import List, Optional

from domaine.entites.intervention_chirurgicale import InterventionChirurgicale
from domaine.ports.repository_intervention_chirurgicale import RepositoryInterventionChirurgicale
from domaine.ports.repository_specialite_chirurgicale import RepositorySpecialiteChirurgicale
from domaine.services.service_base import ServiceBase


class ServiceInterventionChirurgicale(ServiceBase[InterventionChirurgicale]):
    """
    Service pour les interventions chirurgicales.
    
    Ce service étend le service de base avec des méthodes spécifiques
    aux interventions chirurgicales et implémente les règles métier associées.
    
    Attributs
    ---------
    repository_intervention : RepositoryInterventionChirurgicale
        Repository utilisé pour accéder aux données des interventions chirurgicales
    repository_specialite : RepositorySpecialiteChirurgicale
        Repository utilisé pour accéder aux données des spécialités chirurgicales
    """
    
    def __init__(
        self, 
        repository_intervention: RepositoryInterventionChirurgicale,
        repository_specialite: RepositorySpecialiteChirurgicale
    ):
        """
        Initialise une nouvelle instance du service avec les repositories nécessaires.
        
        Paramètres
        ----------
        repository_intervention : RepositoryInterventionChirurgicale
            Repository utilisé pour accéder aux données des interventions chirurgicales
        repository_specialite : RepositorySpecialiteChirurgicale
            Repository utilisé pour accéder aux données des spécialités chirurgicales
        """
        super().__init__(repository_intervention)
        self.repository_intervention = repository_intervention
        self.repository_specialite = repository_specialite
    
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
        return self.repository_intervention.obtenir_par_nom(nom)
    
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
            
        Lève
        ----
        ValueError
            Si la spécialité chirurgicale n'existe pas
        """
        specialite = self.repository_specialite.obtenir_par_id(specialite_id)
        if not specialite:
            raise ValueError(f"Aucune spécialité chirurgicale trouvée avec l'identifiant {specialite_id}")
            
        return self.repository_intervention.obtenir_par_specialite(
            specialite_id=specialite_id, 
            debut=debut, 
            limite=limite
        )
    
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
        return self.repository_intervention.rechercher_par_terme(
            terme_recherche=terme_recherche,
            debut=debut,
            limite=limite
        )
    
    def creer(self, intervention: InterventionChirurgicale) -> InterventionChirurgicale:
        """
        Crée une nouvelle intervention chirurgicale après validation.
        
        Paramètres
        ----------
        intervention : InterventionChirurgicale
            Intervention chirurgicale à créer
            
        Retourne
        --------
        InterventionChirurgicale
            L'intervention chirurgicale créée avec son identifiant
            
        Lève
        ----
        ValueError
            Si une intervention chirurgicale avec le même nom existe déjà
            ou si une des spécialités associées n'existe pas
        """
        intervention_existante = self.obtenir_par_nom(intervention.nom)
        if intervention_existante:
            raise ValueError(f"Une intervention chirurgicale avec le nom '{intervention.nom}' existe déjà")
        
        # Vérification des spécialités existantes
        for specialite in intervention.specialites:
            if specialite.id and not self.repository_specialite.obtenir_par_id(specialite.id):
                raise ValueError(f"La spécialité chirurgicale avec l'identifiant {specialite.id} n'existe pas")
        
        return self.repository_intervention.creer(intervention)
    
    def mettre_a_jour(self, intervention: InterventionChirurgicale) -> InterventionChirurgicale:
        """
        Met à jour une intervention chirurgicale existante après validation.
        
        Paramètres
        ----------
        intervention : InterventionChirurgicale
            Intervention chirurgicale à mettre à jour
            
        Retourne
        --------
        InterventionChirurgicale
            L'intervention chirurgicale mise à jour
            
        Lève
        ----
        ValueError
            Si l'intervention chirurgicale n'existe pas, 
            si le nouveau nom est déjà utilisé,
            ou si une des spécialités associées n'existe pas
        """
        if not intervention.id:
            raise ValueError("L'identifiant de l'intervention chirurgicale est requis pour la mise à jour")
            
        intervention_existante = self.obtenir_par_id(intervention.id)
        if not intervention_existante:
            raise ValueError(f"Aucune intervention chirurgicale trouvée avec l'identifiant {intervention.id}")
            
        intervention_meme_nom = self.obtenir_par_nom(intervention.nom)
        if intervention_meme_nom and intervention_meme_nom.id != intervention.id:
            raise ValueError(f"Une autre intervention chirurgicale avec le nom '{intervention.nom}' existe déjà")
            
        # Vérification des spécialités existantes
        for specialite in intervention.specialites:
            if specialite.id and not self.repository_specialite.obtenir_par_id(specialite.id):
                raise ValueError(f"La spécialité chirurgicale avec l'identifiant {specialite.id} n'existe pas")
        
        return self.repository_intervention.mettre_a_jour(intervention)
