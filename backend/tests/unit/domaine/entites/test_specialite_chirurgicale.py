"""
Tests unitaires pour la classe SpecialiteChirurgicale.

Ce module contient les tests pour vérifier le comportement de l'entité
SpecialiteChirurgicale du domaine.
"""

import pytest
from datetime import datetime

from domaine.entites.specialite_chirurgicale import SpecialiteChirurgicale


class TestSpecialiteChirurgicale:
    """Tests pour la classe SpecialiteChirurgicale."""

    def test_creation_specialite_chirurgicale(self) -> None:
        """
        Teste la création d'une spécialité chirurgicale avec des paramètres valides.
        
        Vérifie que la spécialité est correctement initialisée avec les valeurs fournies.
        """
        # Arrangement & Action
        specialite = SpecialiteChirurgicale(
            nom="Chirurgie orthopédique",
            description="Spécialité chirurgicale concernant le système musculo-squelettique."
        )
        
        # Assertion
        assert specialite.nom == "Chirurgie orthopédique"
        assert specialite.description == "Spécialité chirurgicale concernant le système musculo-squelettique."
        assert specialite.id is None

    def test_creation_specialite_chirurgicale_sans_description(self) -> None:
        """
        Teste la création d'une spécialité chirurgicale sans description.
        
        Vérifie que la description est correctement initialisée à None si non fournie.
        """
        # Arrangement & Action
        specialite = SpecialiteChirurgicale(nom="Chirurgie orthopédique")
        
        # Assertion
        assert specialite.nom == "Chirurgie orthopédique"
        assert specialite.description is None

    def test_creation_specialite_chirurgicale_avec_id(self) -> None:
        """
        Teste la création d'une spécialité chirurgicale avec un ID spécifié.
        
        Vérifie que l'ID est correctement assigné lors de l'initialisation.
        """
        # Arrangement & Action
        specialite = SpecialiteChirurgicale(
            id=42,
            nom="Chirurgie orthopédique"
        )
        
        # Assertion
        assert specialite.id == 42
        assert specialite.nom == "Chirurgie orthopédique"

    def test_creation_specialite_chirurgicale_nom_vide(self) -> None:
        """
        Teste la création d'une spécialité chirurgicale avec un nom vide.
        
        Vérifie que la validation post-initialisation lève une ValueError.
        """
        # Arrangement & Action & Assertion
        with pytest.raises(ValueError) as excinfo:
            SpecialiteChirurgicale(nom="")
        
        assert "Le nom de la spécialité chirurgicale ne peut pas être vide" in str(excinfo.value)

    def test_egalite_specialites_chirurgicales(self) -> None:
        """
        Teste l'égalité entre deux spécialités chirurgicales.
        
        Vérifie que deux spécialités avec les mêmes attributs sont considérées égales.
        """
        # Arrangement
        date_creation = datetime(2025, 1, 1)
        
        # Action
        specialite1 = SpecialiteChirurgicale(
            id=1,
            nom="Chirurgie orthopédique",
            description="Spécialité chirurgicale concernant le système musculo-squelettique.",
            date_creation=date_creation
        )
        specialite2 = SpecialiteChirurgicale(
            id=1,
            nom="Chirurgie orthopédique",
            description="Spécialité chirurgicale concernant le système musculo-squelettique.",
            date_creation=date_creation
        )
        
        # Assertion
        assert specialite1 == specialite2

    def test_inegalite_specialites_chirurgicales(self) -> None:
        """
        Teste l'inégalité entre deux spécialités chirurgicales.
        
        Vérifie que deux spécialités avec des noms différents sont considérées inégales.
        """
        # Arrangement & Action
        specialite1 = SpecialiteChirurgicale(
            id=1,
            nom="Chirurgie orthopédique"
        )
        specialite2 = SpecialiteChirurgicale(
            id=1,
            nom="Chirurgie digestive"
        )
        
        # Assertion
        assert specialite1 != specialite2
