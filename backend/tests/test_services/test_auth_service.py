"""
Testes para AuthService - Service Layer Pattern
Testa a lógica de autenticação.
"""
import pytest
from fastapi import HTTPException
from src.services.auth_service import AuthService
from tests.conftest import mock_user_repository


@pytest.mark.service
@pytest.mark.auth
class TestAuthService:
    """Testes para AuthService."""
    
    def test_authenticate_success(self, auth_service, mock_user_repository, sample_user_data):
        """Testa autenticação bem-sucedida."""
        # Arrange
        from unittest.mock import patch
        mock_user_repository.find_by_username.return_value = sample_user_data
        
        # Mock da verificação de senha (assumindo que a senha está correta)
        with patch('src.services.auth_service.auth.verify_password', return_value=True):
            with patch('src.services.auth_service.auth.create_access_token', return_value="mock_token"):
                # Act
                result = auth_service.authenticate("testuser", "password123")
        
        # Assert
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        mock_user_repository.find_by_username.assert_called_once_with("testuser")
    
    def test_authenticate_user_not_found(self, auth_service, mock_user_repository):
        """Testa autenticação quando usuário não existe."""
        # Arrange
        mock_user_repository.find_by_username.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_service.authenticate("nonexistent", "password123")
        
        assert exc_info.value.status_code == 401
        assert "Usuário ou senha incorretos" in str(exc_info.value.detail)
    
    def test_authenticate_wrong_password(self, auth_service, mock_user_repository, sample_user_data):
        """Testa autenticação com senha incorreta."""
        # Arrange
        from unittest.mock import patch
        mock_user_repository.find_by_username.return_value = sample_user_data
        
        # Mock da verificação de senha (retorna False)
        with patch('src.services.auth_service.auth.verify_password', return_value=False):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                auth_service.authenticate("testuser", "wrongpassword")
        
        assert exc_info.value.status_code == 401
        assert "Usuário ou senha incorretos" in str(exc_info.value.detail)

