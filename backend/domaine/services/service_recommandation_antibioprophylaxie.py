"""
Service pour les recommandations d'antibioprophylaxie.

Ce module définit le service gérant les opérations métier liées aux recommandations
d'antibioprophylaxie selon les directives de la SFAR.
"""

from typing import List, Optional

from domaine.entites.recommandation_antibioprophylaxie import RecommandationAntibioprophylaxie
from domaine.ports.repository_antibiotique import RepositoryAntibiotique
from domaine.ports.repository_intervention_chirurgicale import RepositoryInterventionChirurgicale
from domaine.ports.repository_recommandation_antibioprophylaxie import RepositoryRecommandationAntibioprophylaxie
from domaine.services.service_base import ServiceBase


class ServiceRecommandationAntibioprophylaxie(ServiceBase[RecommandationAntibioprophylaxie]):
    """
    Service pour les recommandations d'antibioprophylaxie.
    
    Ce service étend le service de base avec des méthodes spécifiques
    aux recommandations d'antibioprophylaxie et implémente les règles métier associées.
    
    Attributs
    ---------
    repository_recommandation : RepositoryRecommandationAntibioprophylaxie
        Repository utilisé pour accéder aux données des recommandations
    repository_intervention : RepositoryInterventionChirurgicale
        Repository utilisé pour accéder aux données des interventions chirurgicales
    repository_antibiotique : RepositoryAntibiotique
        Repository utilisé pour accéder aux données des antibiotiques
    """
    
    def __init__(
        self, 
        repository_recommandation: RepositoryRecommandationAntibioprophylaxie,
        repository_intervention: RepositoryInterventionChirurgicale,
        repository_antibiotique: RepositoryAntibiotique
    ):
        """
        Initialise une nouvelle instance du service avec les repositories nécessaires.
        
        Paramètres
        ----------
        repository_recommandation : RepositoryRecommandationAntibioprophylaxie
            Repository utilisé pour accéder aux données des recommandations
        repository_intervention : RepositoryInterventionChirurgicale
            Repository utilisé pour accéder aux données des interventions chirurgicales
        repository_antibiotique : RepositoryAntibiotique
            Repository utilisé pour accéder aux données des antibiotiques
        """
        super().__init__(repository_recommandation)
        self.repository_recommandation = repository_recommandation
        self.repository_intervention = repository_intervention
        self.repository_antibiotique = repository_antibiotique
    
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
            
        Lève
        ----
        ValueError
            Si l'intervention chirurgicale n'existe pas
        """
        intervention = self.repository_intervention.obtenir_par_id(intervention_id)
        if not intervention:
            raise ValueError(f"Aucune intervention chirurgicale trouvée avec l'identifiant {intervention_id}")
            
        return self.repository_recommandation.obtenir_par_intervention(intervention_id)
    
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
            
        Lève
        ----
        ValueError
            Si l'antibiotique n'existe pas
        """
        antibiotique = self.repository_antibiotique.obtenir_par_id(antibiotique_id)
        if not antibiotique:
            raise ValueError(f"Aucun antibiotique trouvé avec l'identifiant {antibiotique_id}")
            
        return self.repository_recommandation.obtenir_par_antibiotique(
            antibiotique_id=antibiotique_id,
            debut=debut,
            limite=limite
        )
    
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
        return self.repository_recommandation.obtenir_par_specialite(
            specialite_id=specialite_id,
            debut=debut,
            limite=limite
        )
    
    def creer(self, recommandation: RecommandationAntibioprophylaxie) -> RecommandationAntibioprophylaxie:
        """
        Crée une nouvelle recommandation d'antibioprophylaxie après validation.
        
        Paramètres
        ----------
        recommandation : RecommandationAntibioprophylaxie
            Recommandation d'antibioprophylaxie à créer
            
        Retourne
        --------
        RecommandationAntibioprophylaxie
            La recommandation d'antibioprophylaxie créée avec son identifiant
            
        Lève
        ----
        ValueError
            Si l'intervention chirurgicale ou l'antibiotique n'existe pas
        """
        # Vérification de l'existence de l'intervention
        if recommandation.intervention.id:
            intervention = self.repository_intervention.obtenir_par_id(recommandation.intervention.id)
            if not intervention:
                raise ValueError(f"L'intervention chirurgicale avec l'identifiant {recommandation.intervention.id} n'existe pas")
        
        # Vérification de l'existence de l'antibiotique
        if recommandation.antibiotique.id:
            antibiotique = self.repository_antibiotique.obtenir_par_id(recommandation.antibiotique.id)
            if not antibiotique:
                raise ValueError(f"L'antibiotique avec l'identifiant {recommandation.antibiotique.id} n'existe pas")
        
        return self.repository_recommandation.creer(recommandation)
    
    def mettre_a_jour(self, recommandation: RecommandationAntibioprophylaxie) -> RecommandationAntibioprophylaxie:
        """
        Met à jour une recommandation d'antibioprophylaxie existante après validation.
        
        Paramètres
        ----------
        recommandation : RecommandationAntibioprophylaxie
            Recommandation d'antibioprophylaxie à mettre à jour
            
        Retourne
        --------
        RecommandationAntibioprophylaxie
            La recommandation d'antibioprophylaxie mise à jour
            
        Lève
        ----
        ValueError
            Si la recommandation n'existe pas, ou si l'intervention chirurgicale
            ou l'antibiotique n'existe pas
        """
        if not recommandation.id:
            raise ValueError("L'identifiant de la recommandation est requis pour la mise à jour")
            
        recommandation_existante = self.obtenir_par_id(recommandation.id)
        if not recommandation_existante:
            raise ValueError(f"Aucune recommandation trouvée avec l'identifiant {recommandation.id}")
            
        # Vérification de l'existence de l'intervention
        if recommandation.intervention.id:
            intervention = self.repository_intervention.obtenir_par_id(recommandation.intervention.id)
            if not intervention:
                raise ValueError(f"L'intervention chirurgicale avec l'identifiant {recommandation.intervention.id} n'existe pas")
        
        # Vérification de l'existence de l'antibiotique
        if recommandation.antibiotique.id:
            antibiotique = self.repository_antibiotique.obtenir_par_id(recommandation.antibiotique.id)
            if not antibiotique:
                raise ValueError(f"L'antibiotique avec l'identifiant {recommandation.antibiotique.id} n'existe pas")
        
        return self.repository_recommandation.mettre_a_jour(recommandation)
