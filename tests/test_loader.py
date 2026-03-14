"""Tests pour le chargement des données JSON."""

import json
from pathlib import Path

import pytest

from app.data.loader import load_rfe_data
from app.data.models import RFEData


class TestLoadRfeData:
    """Tests pour la fonction load_rfe_data."""

    def test_charge_donnees_valides(self, tmp_path):
        """Charge un fichier JSON valide et retourne un RFEData."""
        data = {
            "version": "RFE SFAR 2024",
            "date_extraction": "2026-02-16",
            "specialites": [
                {
                    "id": "test",
                    "nom": "Test",
                    "interventions": [
                        {
                            "id": "test-01",
                            "nom": "Intervention test",
                            "specialite": "Test",
                            "protocole": {
                                "molecule": "Céfazoline",
                                "dose_initiale": "2g IVL",
                            },
                            "force_recommandation": "Avis d'experts",
                            "source_page": 1,
                            "source_tableau": "Tableau test",
                        }
                    ],
                }
            ],
        }
        json_path = tmp_path / "rfe.json"
        json_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_rfe_data(json_path)

        assert isinstance(result, RFEData)
        assert result.version == "RFE SFAR 2024"
        assert len(result.specialites) == 1
        assert len(result.specialites[0].interventions) == 1

    def test_fichier_inexistant_leve_erreur(self, tmp_path):
        """Un fichier inexistant lève FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_rfe_data(tmp_path / "inexistant.json")

    def test_json_invalide_leve_erreur(self, tmp_path):
        """Un JSON invalide lève une erreur."""
        json_path = tmp_path / "rfe.json"
        json_path.write_text("{broken json", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            load_rfe_data(json_path)

    def test_donnees_non_conformes_leve_erreur(self, tmp_path):
        """Des données qui ne respectent pas le schéma lèvent ValidationError."""
        from pydantic import ValidationError

        json_path = tmp_path / "rfe.json"
        json_path.write_text('{"version": 42}', encoding="utf-8")

        with pytest.raises(ValidationError):
            load_rfe_data(json_path)

    def test_charge_vrai_fichier(self):
        """Charge le vrai fichier data/rfe.json du projet."""
        project_root = Path(__file__).parent.parent
        json_path = project_root / "data" / "rfe.json"

        result = load_rfe_data(json_path)

        assert isinstance(result, RFEData)
        assert len(result.specialites) >= 2
        total = sum(len(s.interventions) for s in result.specialites)
        assert total >= 40

    def test_champ_inconnu_rejete(self, tmp_path):
        """Un champ inconnu dans le JSON est rejeté (extra='forbid')."""
        from pydantic import ValidationError

        data = {
            "version": "RFE SFAR 2024",
            "date_extraction": "2026-02-16",
            "specialites": [],
            "champ_inconnu": "valeur",
        }
        json_path = tmp_path / "rfe.json"
        json_path.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValidationError):
            load_rfe_data(json_path)

    def test_sous_categorie_extraite_depuis_source_tableau(self, tmp_path):
        """La sous-catégorie est extraite de source_tableau après le «\u00a0—\u00a0»."""
        data = {
            "version": "RFE SFAR 2024",
            "date_extraction": "2026-02-16",
            "specialites": [
                {
                    "id": "ortho",
                    "nom": "Chirurgie orthopédique",
                    "interventions": [
                        {
                            "id": "ortho-01",
                            "nom": "Prothèse de hanche",
                            "specialite": "Chirurgie orthopédique",
                            "protocole": {
                                "molecule": "Céfazoline",
                                "dose_initiale": "2g IVL",
                            },
                            "force_recommandation": "Avis d'experts",
                            "source_page": 1,
                            "source_tableau": (
                                "Tableau Chirurgie orthopédique \u2014 Membre inférieur"
                            ),
                        }
                    ],
                }
            ],
        }
        json_path = tmp_path / "rfe.json"
        json_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_rfe_data(json_path)
        interv = result.specialites[0].interventions[0]

        assert interv.sous_categorie == "Membre inférieur"

    def test_sous_categorie_none_si_pas_tiret(self, tmp_path):
        """Si source_tableau ne contient pas «\u00a0—\u00a0», sous_categorie vaut None."""
        data = {
            "version": "RFE SFAR 2024",
            "date_extraction": "2026-02-16",
            "specialites": [
                {
                    "id": "test",
                    "nom": "Test",
                    "interventions": [
                        {
                            "id": "test-01",
                            "nom": "Intervention test",
                            "specialite": "Test",
                            "protocole": {
                                "molecule": "Céfazoline",
                                "dose_initiale": "2g IVL",
                            },
                            "force_recommandation": "Avis d'experts",
                            "source_page": 1,
                            "source_tableau": "Tableau sans tiret",
                        }
                    ],
                }
            ],
        }
        json_path = tmp_path / "rfe.json"
        json_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_rfe_data(json_path)
        interv = result.specialites[0].interventions[0]

        assert interv.sous_categorie is None

    def test_sous_categorie_extraite_vrai_fichier(self):
        """Dans le vrai fichier, les interventions orthopédiques ont des sous-catégories."""
        project_root = Path(__file__).parent.parent
        json_path = project_root / "data" / "rfe.json"

        result = load_rfe_data(json_path)

        ortho = next(
            (s for s in result.specialites if s.id == "chirurgie-orthopedique-programmee"),
            None,
        )
        assert ortho is not None
        sous_cats = {i.sous_categorie for i in ortho.interventions if i.sous_categorie}
        assert "Membre inférieur" in sous_cats
        assert "Épaule et coude" in sous_cats
