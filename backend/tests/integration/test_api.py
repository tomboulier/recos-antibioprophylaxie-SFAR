"""
Tests d'intégration pour l'API.

Ce module contient des tests qui vérifient le bon fonctionnement de l'API
et de ses différentes routes.
"""

import pytest
from fastapi.testclient import TestClient

from infrastructure.api.main import app


@pytest.fixture
def client():
    """
    Fixture qui fournit un client de test pour l'API FastAPI.
    
    Retourne
    --------
    TestClient
        Client pour tester l'API
    """
    return TestClient(app)


class TestAPIBase:
    """Tests d'intégration pour les routes de base de l'API."""

    def test_route_racine(self, client):
        """
        Teste la route racine de l'API.
        
        Vérifie que la route racine répond avec un statut 200 et 
        contient les informations attendues.
        """
        # Action
        response = client.get("/")
        
        # Assertion
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Bienvenue sur l'API Antibioprophylaxie SFAR" in data["message"]
        assert "documentation" in data
        assert "version" in data

    def test_route_health(self, client):
        """
        Teste la route de vérification de l'état de santé de l'API.
        
        Vérifie que la route health répond avec un statut 200 et 
        indique que l'API est opérationnelle.
        """
        # Action
        response = client.get("/health")
        
        # Assertion
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_documentation_openapi(self, client):
        """
        Teste l'accès à la documentation OpenAPI.
        
        Vérifie que la route de documentation est accessible.
        """
        # Action
        response = client.get("/docs")
        
        # Assertion
        assert response.status_code == 200
        # Vérifie que la page HTML de Swagger UI est retournée
        assert "swagger-ui" in response.text.lower()

    def test_schema_openapi(self, client):
        """
        Teste l'accès au schéma OpenAPI.
        
        Vérifie que le schéma JSON de l'API est accessible et contient
        les informations de base sur l'API.
        """
        # Action
        response = client.get("/openapi.json")
        
        # Assertion
        assert response.status_code == 200
        schema = response.json()
        assert "info" in schema
        assert schema["info"]["title"] == "API Antibioprophylaxie SFAR"
        assert "paths" in schema
        # Vérifie que les routes de base sont dans le schéma
        assert "/" in schema["paths"]
        assert "/health" in schema["paths"]
