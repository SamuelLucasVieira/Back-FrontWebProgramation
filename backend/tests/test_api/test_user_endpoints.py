"""
Testes para endpoints de usuários.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from tests.helpers import override_auth_dependency, clear_overrides, create_mock_user


@pytest.mark.api
class TestUserEndpoints:
    """Testes para endpoints de usuários."""
    
    def test_get_users_me_success(self, client):
        """Testa obtenção de dados do usuário logado."""
        # Arrange
        from src.main import app
        override_auth_dependency(app, user_role="admin")
        
        try:
            # Act
            response = client.get("/users/me/", headers={"Authorization": "Bearer mock_token"})
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "admin"
            assert data["role"] == "admin"
        finally:
            clear_overrides(app)
    
    def test_get_users_unauthorized(self, client):
        """Testa acesso sem autenticação."""
        # Act
        response = client.get("/users/")
        
        # Assert
        assert response.status_code == 401  # Unauthorized
    
    def test_create_user_success(self, client):
        """Testa criação de usuário por admin."""
        # Arrange
        from src.main import app
        from src.dependencies import get_user_service
        
        mock_created_user = {
            "id": 2,
            "username": "newuser",
            "email": "newuser@example.com",
            "role": "visualizacao"
        }
        
        mock_service = MagicMock()
        mock_service.create_user.return_value = mock_created_user
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_user_service] = lambda: mock_service
        
        try:
            # Act
            response = client.post(
                "/users/",
                json={
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "password123",
                    "role": "visualizacao"
                },
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 201
            data = response.json()
            assert data["username"] == "newuser"
        finally:
            clear_overrides(app)
    
    def test_create_user_duplicate_username(self, client):
        """Testa criação de usuário com username duplicado."""
        # Arrange
        from src.main import app
        from src.dependencies import get_user_service
        from fastapi import HTTPException
        
        mock_service = MagicMock()
        mock_service.create_user.side_effect = HTTPException(
            status_code=400,
            detail="Username já registrado"
        )
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_user_service] = lambda: mock_service
        
        try:
            # Act
            response = client.post(
                "/users/",
                json={
                    "username": "existinguser",
                    "email": "existing@example.com",
                    "password": "password123",
                    "role": "visualizacao"
                },
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 400
        finally:
            clear_overrides(app)
    
    def test_update_user_success(self, client):
        """Testa atualização de usuário."""
        # Arrange
        from src.main import app
        from src.dependencies import get_user_service
        
        mock_updated_user = {
            "id": 1,
            "username": "updateduser",
            "email": "updated@example.com",
            "role": "gerencial"
        }
        
        mock_service = MagicMock()
        mock_service.update_user.return_value = mock_updated_user
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_user_service] = lambda: mock_service
        
        try:
            # Act
            response = client.put(
                "/users/1",
                json={
                    "username": "updateduser",
                    "email": "updated@example.com",
                    "role": "gerencial"
                },
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "updateduser"
        finally:
            clear_overrides(app)
    
    def test_delete_user_success(self, client):
        """Testa deleção de usuário."""
        # Arrange
        from src.main import app
        from src.dependencies import get_user_service
        
        mock_service = MagicMock()
        mock_service.delete_user.return_value = True
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_user_service] = lambda: mock_service
        
        try:
            # Act
            response = client.delete(
                "/users/1",
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
        finally:
            clear_overrides(app)

