"""
Tests unitaires pour la classe EntiteBase.

Ce module contient les tests pour vérifier le comportement de la classe
de base pour toutes les entités du domaine.
"""

import pytest
from datetime import datetime, timedelta
from dataclasses import dataclass

from domaine.entites.entite_base import EntiteBase


@dataclass
class EntiteTest(EntiteBase):
    """Classe concrète d'entité pour les tests."""
    nom: str = "Test"


class TestEntiteBase:
    """Tests pour la classe EntiteBase."""

    def test_creation_entite_base(self) -> None:
        """
        Teste la création d'une entité avec les valeurs par défaut.
        
        Vérifie que l'entité est correctement initialisée avec un ID à None
        et des dates de création et modification automatiques.
        """
        # Arrangement
        avant_creation = datetime.utcnow()
        
        # Action
        entite = EntiteTest()
        
        # Assertion
        assert entite.id is None
        assert entite.date_creation >= avant_creation
        assert entite.date_modification >= avant_creation
        assert entite.nom == "Test"

    def test_creation_entite_base_avec_id(self) -> None:
        """
        Teste la création d'une entité avec un ID spécifié.
        
        Vérifie que l'ID est correctement assigné lors de l'initialisation.
        """
        # Arrangement & Action
        entite = EntiteTest(id=42)
        
        # Assertion
        assert entite.id == 42

    def test_modification_date_creation(self) -> None:
        """
        Teste la modification de la date de création.
        
        Vérifie que la date de création peut être modifiée explicitement.
        """
        # Arrangement
        date_specifique = datetime(2025, 1, 1)
        
        # Action
        entite = EntiteTest(date_creation=date_specifique)
        
        # Assertion
        assert entite.date_creation == date_specifique

    def test_modification_date_modification(self) -> None:
        """
        Teste la modification de la date de modification.
        
        Vérifie que la date de modification peut être modifiée explicitement.
        """
        # Arrangement
        date_specifique = datetime(2025, 1, 1)
        
        # Action
        entite = EntiteTest(date_modification=date_specifique)
        
        # Assertion
        assert entite.date_modification == date_specifique

    def test_egalite_entites(self) -> None:
        """
        Teste l'égalité entre deux entités.
        
        Vérifie que deux entités avec les mêmes attributs sont considérées égales.
        """
        # Arrangement
        date_creation = datetime(2025, 1, 1)
        date_modification = datetime(2025, 1, 2)
        
        # Action
        entite1 = EntiteTest(id=1, date_creation=date_creation, date_modification=date_modification)
        entite2 = EntiteTest(id=1, date_creation=date_creation, date_modification=date_modification)
        
        # Assertion
        assert entite1 == entite2

    def test_inegalite_entites(self) -> None:
        """
        Teste l'inégalité entre deux entités.
        
        Vérifie que deux entités avec des attributs différents sont considérées inégales.
        """
        # Arrangement
        date_creation = datetime(2025, 1, 1)
        date_modification = datetime(2025, 1, 2)
        
        # Action
        entite1 = EntiteTest(id=1, date_creation=date_creation, date_modification=date_modification)
        entite2 = EntiteTest(id=2, date_creation=date_creation, date_modification=date_modification)
        
        # Assertion
        assert entite1 != entite2
