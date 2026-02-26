"""Tests pour la configuration de l'application."""

from app.config import Settings


class TestSettings:
    """Tests pour la classe Settings."""

    def test_valeurs_par_defaut(self):
        """Les valeurs par défaut sont cohérentes."""
        settings = Settings()
        assert settings.app_name == "Antibioprophylaxie SFAR"
        assert settings.app_version == "0.1.0"
        assert settings.data_version == "RFE SFAR 2024"
        assert settings.debug is False

    def test_data_path_par_defaut(self):
        """Le chemin vers rfe.json est relatif à la racine du projet."""
        settings = Settings()
        assert settings.data_path.name == "rfe.json"
        assert settings.data_path.parent.name == "data"

    def test_surcharge_via_env(self, monkeypatch):
        """Les variables d'environnement surchargent les valeurs par défaut."""
        monkeypatch.setenv("DEBUG", "true")
        settings = Settings()
        assert settings.debug is True
