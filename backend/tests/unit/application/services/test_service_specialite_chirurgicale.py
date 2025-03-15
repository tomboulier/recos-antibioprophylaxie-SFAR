"""
Tests unitaires pour le service d'application des spécialités chirurgicales.

Ce module contient les tests pour vérifier le comportement du service d'application
pour les spécialités chirurgicales.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale
from domaine.services.service_specialite_chirurgicale import ServiceSpecialiteChirurgicale
from application.dto.specialite_chirurgicale_dto import (
    SpecialiteChirurgicaleCreation,
    SpecialiteChirurgicaleMiseAJour,
    SpecialiteChirurgicaleReponse,
    SpecialiteChirurgicaleCollection,
)
from application.services.service_specialite_chirurgicale import ServiceApplicationSpecialiteChirurgicale


class TestServiceApplicationSpecialiteChirurgicale:
    """Tests pour le service d'application des spécialités chirurgicales."""

    @pytest.fixture
    def mock_service_domaine(self):
        """Fixture pour mocker le service domaine."""
        return MagicMock(spec=ServiceSpecialiteChirurgicale)

    @pytest.fixture
    def service_application(self, mock_service_domaine):
        """Fixture pour créer le service d'application avec un mock du service domaine."""
        return ServiceApplicationSpecialiteChirurgicale(service_domaine=mock_service_domaine)

    def test_obtenir_par_id_existant(self, mock_service_domaine, service_application):
        """
        Teste la récupération d'une spécialité chirurgicale par ID quand elle existe.
        
        Vérifie que le service d'application convertit correctement l'entité en DTO.
        """
        # Arrangement
        specialite_id = 1
        date_creation = datetime(2025, 1, 1)
        date_modification = datetime(2025, 1, 2)
        
        specialite = SpecialiteChirurgicale(
            nom="Chirurgie orthopédique",
            description="Spécialité chirurgicale concernant le système musculo-squelettique.",
            id=specialite_id,
            date_creation=date_creation,
            date_modification=date_modification,
        )
        mock_service_domaine.obtenir_par_id.return_value = specialite
        
        # Action
        resultat = service_application.obtenir_par_id(specialite_id)
        
        # Assertion
        mock_service_domaine.obtenir_par_id.assert_called_once_with(specialite_id)
        assert isinstance(resultat, SpecialiteChirurgicaleReponse)
        assert resultat.id == specialite_id
        assert resultat.nom == "Chirurgie orthopédique"
        assert resultat.description == "Spécialité chirurgicale concernant le système musculo-squelettique."
        assert resultat.date_creation == date_creation
        assert resultat.date_modification == date_modification

    def test_obtenir_par_id_inexistant(self, mock_service_domaine, service_application):
        """
        Teste la récupération d'une spécialité chirurgicale par ID quand elle n'existe pas.
        
        Vérifie que le service d'application gère correctement le cas où l'entité n'est pas trouvée.
        """
        # Arrangement
        specialite_id = 999
        mock_service_domaine.obtenir_par_id.return_value = None
        
        # Action
        resultat = service_application.obtenir_par_id(specialite_id)
        
        # Assertion
        mock_service_domaine.obtenir_par_id.assert_called_once_with(specialite_id)
        assert resultat is None

    def test_obtenir_par_nom_existant(self, mock_service_domaine, service_application):
        """
        Teste la récupération d'une spécialité chirurgicale par nom quand elle existe.
        
        Vérifie que le service d'application convertit correctement l'entité en DTO.
        """
        # Arrangement
        nom = "Chirurgie orthopédique"
        specialite = SpecialiteChirurgicale(
            nom=nom,
            description="Spécialité chirurgicale concernant le système musculo-squelettique.",
            id=1,
        )
        mock_service_domaine.obtenir_par_nom.return_value = specialite
        
        # Action
        resultat = service_application.obtenir_par_nom(nom)
        
        # Assertion
        mock_service_domaine.obtenir_par_nom.assert_called_once_with(nom)
        assert isinstance(resultat, SpecialiteChirurgicaleReponse)
        assert resultat.nom == nom

    def test_obtenir_par_nom_inexistant(self, mock_service_domaine, service_application):
        """
        Teste la récupération d'une spécialité chirurgicale par nom quand elle n'existe pas.
        
        Vérifie que le service d'application gère correctement le cas où l'entité n'est pas trouvée.
        """
        # Arrangement
        nom = "Spécialité inexistante"
        mock_service_domaine.obtenir_par_nom.return_value = None
        
        # Action
        resultat = service_application.obtenir_par_nom(nom)
        
        # Assertion
        mock_service_domaine.obtenir_par_nom.assert_called_once_with(nom)
        assert resultat is None

    def test_creer_specialite(self, mock_service_domaine, service_application):
        """
        Teste la création d'une nouvelle spécialité chirurgicale.
        
        Vérifie que le service d'application convertit correctement le DTO de création
        en entité et retourne le DTO de réponse correspondant.
        """
        # Arrangement
        specialite_id = 1
        nom = "Chirurgie orthopédique"
        description = "Spécialité chirurgicale concernant le système musculo-squelettique."
        
        dto_creation = SpecialiteChirurgicaleCreation(
            nom=nom,
            description=description
        )
        
        date_creation = datetime(2025, 1, 1)
        date_modification = datetime(2025, 1, 1)
        
        specialite_creee = SpecialiteChirurgicale(
            nom=nom,
            description=description,
            id=specialite_id,
            date_creation=date_creation,
            date_modification=date_modification,
        )
        
        mock_service_domaine.creer.return_value = specialite_creee
        
        # Action
        resultat = service_application.creer(dto_creation)
        
        # Assertion
        mock_service_domaine.creer.assert_called_once()
        assert isinstance(resultat, SpecialiteChirurgicaleReponse)
        assert resultat.id == specialite_id
        assert resultat.nom == nom
        assert resultat.description == description
        assert resultat.date_creation == date_creation
        assert resultat.date_modification == date_modification

    def test_mettre_a_jour_specialite(self, mock_service_domaine, service_application):
        """
        Teste la mise à jour d'une spécialité chirurgicale.
        
        Vérifie que le service d'application convertit correctement le DTO de mise à jour
        en entité et retourne le DTO de réponse correspondant.
        """
        # Arrangement
        specialite_id = 1
        nom = "Nouvelle chirurgie orthopédique"
        description = "Nouvelle description de la spécialité."
        
        dto_mise_a_jour = SpecialiteChirurgicaleMiseAJour(
            nom=nom,
            description=description
        )
        
        date_creation = datetime(2025, 1, 1)
        date_modification = datetime(2025, 1, 2)
        
        specialite_mise_a_jour = SpecialiteChirurgicale(
            nom=nom,
            description=description,
            id=specialite_id,
            date_creation=date_creation,
            date_modification=date_modification,
        )
        
        mock_service_domaine.mettre_a_jour.return_value = specialite_mise_a_jour
        
        # Action
        resultat = service_application.mettre_a_jour(specialite_id, dto_mise_a_jour)
        
        # Assertion
        mock_service_domaine.mettre_a_jour.assert_called_once()
        assert isinstance(resultat, SpecialiteChirurgicaleReponse)
        assert resultat.id == specialite_id
        assert resultat.nom == nom
        assert resultat.description == description
        assert resultat.date_creation == date_creation
        assert resultat.date_modification == date_modification

    def test_supprimer_specialite(self, mock_service_domaine, service_application):
        """
        Teste la suppression d'une spécialité chirurgicale.
        
        Vérifie que le service d'application délègue correctement la suppression au service domaine.
        """
        # Arrangement
        specialite_id = 1
        mock_service_domaine.supprimer.return_value = True
        
        # Action
        resultat = service_application.supprimer(specialite_id)
        
        # Assertion
        mock_service_domaine.supprimer.assert_called_once_with(specialite_id)
        assert resultat is True

    def test_obtenir_tous(self, mock_service_domaine, service_application):
        """
        Teste la récupération de toutes les spécialités chirurgicales.
        
        Vérifie que le service d'application convertit correctement la liste d'entités
        en DTO de collection.
        """
        # Arrangement
        specialites = [
            SpecialiteChirurgicale(nom="Chirurgie orthopédique", id=1),
            SpecialiteChirurgicale(nom="Chirurgie digestive", id=2),
            SpecialiteChirurgicale(nom="Chirurgie vasculaire", id=3),
        ]
        # Modifier le comportement du mock pour qu'il renvoie juste la liste,
        # conformément à l'implémentation actuelle
        mock_service_domaine.obtenir_tous.return_value = specialites
        
        # Action
        resultat = service_application.obtenir_tous(debut=0, limite=10)
        
        # Assertion
        mock_service_domaine.obtenir_tous.assert_called_once_with(debut=0, limite=10)
        assert isinstance(resultat, SpecialiteChirurgicaleCollection)
        assert resultat.total == 3
        assert len(resultat.items) == 3
        for i, item in enumerate(resultat.items):
            assert isinstance(item, SpecialiteChirurgicaleReponse)
            assert item.id == specialites[i].id
            assert item.nom == specialites[i].nom
