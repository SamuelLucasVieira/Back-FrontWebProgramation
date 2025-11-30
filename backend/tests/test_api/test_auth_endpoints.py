"""
Testes para endpoints de autenticação.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.mark.api
@pytest.mark.auth
class TestAuthEndpoints:
    """Testes para endpoints de autenticação."""
    
    def test_login_success(self, client):
        """Testa login bem-sucedido."""
        # Arrange
        from src.main import app
        from src.dependencies import get_auth_service
        
        mock_service = MagicMock()
        mock_service.authenticate.return_value = {
            "access_token": "mock_token_123",
            "token_type": "bearer"
        }
        
        app.dependency_overrides[get_auth_service] = lambda: mock_service
        
        try:
            # Act
            response = client.post(
                "/token",
                data={"username": "admin", "password": "admin123"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"
        finally:
            app.dependency_overrides.clear()
    
    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas."""
        # Arrange
        from src.main import app
        from src.dependencies import get_auth_service
        from fastapi import HTTPException
        
        mock_service = MagicMock()
        mock_service.authenticate.side_effect = HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos"
        )
        
        app.dependency_overrides[get_auth_service] = lambda: mock_service
        
        try:
            # Act
            response = client.post(
                "/token",
                data={"username": "admin", "password": "wrongpassword"}
            )
            
            # Assert
            assert response.status_code == 401
        finally:
            # Limpar override
            app.dependency_overrides.clear()
    
    def test_login_missing_credentials(self, client):
        """Testa login sem credenciais."""
        # Act
        response = client.post("/token", data={})
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity

