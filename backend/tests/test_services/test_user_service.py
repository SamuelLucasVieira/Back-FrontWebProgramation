"""
Testes para UserService - Service Layer Pattern
Testa a lógica de negócio relacionada a usuários.
"""
import pytest
from fastapi import HTTPException
from src.services.user_service import UserService
from src.config import schemas
from tests.conftest import mock_user_repository


@pytest.mark.service
class TestUserService:
    """Testes para UserService."""
    
    def test_get_user_by_username_success(self, user_service, mock_user_repository, sample_user_data):
        """Testa busca de usuário por username com sucesso."""
        # Arrange
        mock_user_repository.find_by_username.return_value = sample_user_data
        
        # Act
        result = user_service.get_user_by_username("testuser")
        
        # Assert
        assert result is not None
        assert result["username"] == "testuser"
        mock_user_repository.find_by_username.assert_called_once_with("testuser")
    
    def test_get_user_by_id_success(self, user_service, mock_user_repository, sample_user_data):
        """Testa busca de usuário por ID com sucesso."""
        # Arrange
        mock_user_repository.find_by_id.return_value = sample_user_data
        
        # Act
        result = user_service.get_user_by_id(1)
        
        # Assert
        assert result is not None
        assert result["id"] == 1
        mock_user_repository.find_by_id.assert_called_once_with(1)
    
    def test_get_user_by_id_not_found(self, user_service, mock_user_repository):
        """Testa busca de usuário por ID quando não encontrado."""
        # Arrange
        mock_user_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user_by_id(999)
        
        assert exc_info.value.status_code == 404
        assert "Usuário não encontrado" in str(exc_info.value.detail)
    
    def test_get_all_users_admin(self, user_service, mock_user_repository):
        """Testa listagem de todos os usuários para admin."""
        # Arrange
        mock_users = [
            {"id": 1, "username": "admin", "role": "admin"},
            {"id": 2, "username": "user1", "role": "gerencial"}
        ]
        mock_user_repository.find_all.return_value = mock_users
        
        # Act
        result = user_service.get_all_users("admin")
        
        # Assert
        assert len(result) == 2
        mock_user_repository.find_all.assert_called_once()
    
    def test_get_all_users_gerencial(self, user_service, mock_user_repository):
        """Testa listagem de usuários para gerencial (filtrado)."""
        # Arrange
        mock_users = [
            {"id": 2, "username": "user1", "role": "gerencial"},
            {"id": 3, "username": "user2", "role": "visualizacao"}
        ]
        mock_user_repository.find_by_max_role.return_value = mock_users
        
        # Act
        result = user_service.get_all_users("gerencial")
        
        # Assert
        assert len(result) == 2
        mock_user_repository.find_by_max_role.assert_called_once_with("gerencial")
    
    def test_create_user_success(self, user_service, mock_user_repository, sample_user_create):
        """Testa criação de usuário com sucesso."""
        # Arrange
        mock_user_repository.exists_by_username.return_value = False
        mock_user_repository.create.return_value = {
            "id": 1,
            "username": "newuser",
            "email": "newuser@example.com",
            "role": "visualizacao"
        }
        
        # Act
        result = user_service.create_user(sample_user_create)
        
        # Assert
        assert result["username"] == "newuser"
        mock_user_repository.exists_by_username.assert_called_once_with("newuser")
        mock_user_repository.create.assert_called_once()
    
    def test_create_user_username_exists(self, user_service, mock_user_repository, sample_user_create):
        """Testa criação de usuário quando username já existe."""
        # Arrange
        mock_user_repository.exists_by_username.return_value = True
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.create_user(sample_user_create)
        
        assert exc_info.value.status_code == 400
        assert "Username já registrado" in str(exc_info.value.detail)
    
    def test_update_user_success(self, user_service, mock_user_repository):
        """Testa atualização de usuário com sucesso."""
        # Arrange
        existing_user = {"id": 1, "username": "olduser", "email": "old@example.com", "role": "visualizacao"}
        updated_user = {"id": 1, "username": "newuser", "email": "new@example.com", "role": "visualizacao"}
        user_update = schemas.UserUpdate(username="newuser", email="new@example.com")
        
        mock_user_repository.find_by_id.return_value = existing_user
        mock_user_repository.exists_by_username.return_value = False
        mock_user_repository.update.return_value = updated_user
        
        # Act
        result = user_service.update_user(1, user_update, "admin")
        
        # Assert
        assert result["username"] == "newuser"
        mock_user_repository.find_by_id.assert_called_once_with(1)
        mock_user_repository.update.assert_called_once()
    
    def test_update_user_not_found(self, user_service, mock_user_repository):
        """Testa atualização de usuário inexistente."""
        # Arrange
        mock_user_repository.find_by_id.return_value = None
        user_update = schemas.UserUpdate(username="newuser")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(999, user_update, "admin")
        
        assert exc_info.value.status_code == 404
        assert "Usuário não encontrado" in str(exc_info.value.detail)
    
    def test_update_user_gerencial_cannot_edit_admin(self, user_service, mock_user_repository):
        """Testa que gerencial não pode editar admin."""
        # Arrange
        existing_user = {"id": 1, "username": "admin", "role": "admin"}
        user_update = schemas.UserUpdate(username="newuser")
        
        mock_user_repository.find_by_id.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(1, user_update, "gerencial")
        
        assert exc_info.value.status_code == 403
        assert "Gerenciais não podem editar administradores" in str(exc_info.value.detail)
    
    def test_update_user_gerencial_cannot_set_admin_role(self, user_service, mock_user_repository):
        """Testa que gerencial não pode alterar role para admin."""
        # Arrange
        existing_user = {"id": 1, "username": "user1", "role": "gerencial"}
        user_update = schemas.UserUpdate(role="admin")
        
        mock_user_repository.find_by_id.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(1, user_update, "gerencial")
        
        assert exc_info.value.status_code == 403
        assert "Gerenciais não podem alterar role para admin" in str(exc_info.value.detail)
    
    def test_update_user_username_already_in_use(self, user_service, mock_user_repository):
        """Testa atualização quando novo username já está em uso."""
        # Arrange
        existing_user = {"id": 1, "username": "olduser", "role": "visualizacao"}
        user_update = schemas.UserUpdate(username="existinguser")
        
        mock_user_repository.find_by_id.return_value = existing_user
        mock_user_repository.exists_by_username.return_value = True
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(1, user_update, "admin")
        
        assert exc_info.value.status_code == 400
        assert "Username já está em uso" in str(exc_info.value.detail)
    
    def test_delete_user_success(self, user_service, mock_user_repository):
        """Testa deleção de usuário com sucesso."""
        # Arrange
        mock_user_repository.delete.return_value = True
        
        # Act
        result = user_service.delete_user(1)
        
        # Assert
        assert result is True
        mock_user_repository.delete.assert_called_once_with(1)
    
    def test_delete_user_not_found(self, user_service, mock_user_repository):
        """Testa deleção de usuário inexistente."""
        # Arrange
        mock_user_repository.delete.return_value = False
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            user_service.delete_user(999)
        
        assert exc_info.value.status_code == 404
        assert "Usuário não encontrado" in str(exc_info.value.detail)

