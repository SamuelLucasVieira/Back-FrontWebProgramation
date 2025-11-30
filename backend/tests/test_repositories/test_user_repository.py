"""
Testes para UserRepository - Repository Pattern
Testa as operações de acesso a dados de usuários.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.repositories.user_repository import UserRepository
from src.config.database import get_db_cursor


@pytest.mark.repository
class TestUserRepository:
    """Testes para UserRepository."""
    
    def test_find_by_username_success(self):
        """Testa busca de usuário por username com sucesso."""
        # Arrange
        repository = UserRepository()
        mock_row = (1, "testuser", "test@example.com", "hashed_pass", "admin", "2024-01-01")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("username",), ("email",), ("hashed_password",), ("role",), ("created_at",)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_username("testuser")
        
        # Assert
        assert result is not None
        assert result["username"] == "testuser"
        assert result["email"] == "test@example.com"
        assert result["role"] == "admin"
    
    def test_find_by_username_not_found(self):
        """Testa busca de usuário por username quando não encontrado."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_username("nonexistent")
        
        # Assert
        assert result is None
    
    def test_find_by_id_success(self):
        """Testa busca de usuário por ID com sucesso."""
        # Arrange
        repository = UserRepository()
        mock_row = (1, "testuser", "test@example.com", "admin", "2024-01-01")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("username",), ("email",), ("role",), ("created_at",)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_id(1)
        
        # Assert
        assert result is not None
        assert result["id"] == 1
        assert result["username"] == "testuser"
    
    def test_find_by_id_not_found(self):
        """Testa busca de usuário por ID quando não encontrado."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_id(999)
        
        # Assert
        assert result is None
    
    def test_find_all(self):
        """Testa busca de todos os usuários."""
        # Arrange
        repository = UserRepository()
        mock_rows = [
            (1, "user1", "user1@example.com", "admin", "2024-01-01"),
            (2, "user2", "user2@example.com", "gerencial", "2024-01-02")
        ]
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("username",), ("email",), ("role",), ("created_at",)
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_all()
        
        # Assert
        assert len(result) == 2
        assert result[0]["username"] == "user1"
        assert result[1]["username"] == "user2"
    
    def test_find_by_max_role(self):
        """Testa busca de usuários por nível máximo de role."""
        # Arrange
        repository = UserRepository()
        mock_rows = [
            (1, "admin", "admin@example.com", "admin", "2024-01-01"),
            (2, "gerencial", "gerencial@example.com", "gerencial", "2024-01-02"),
            (3, "visual", "visual@example.com", "visualizacao", "2024-01-03")
        ]
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("username",), ("email",), ("role",), ("created_at",)
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_max_role("gerencial")
        
        # Assert
        # Deve retornar apenas gerencial e visualizacao (não admin)
        assert len(result) == 2
        assert all(user["role"] != "admin" for user in result)
    
    def test_create_user(self):
        """Testa criação de novo usuário."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # ID retornado
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            with patch('src.repositories.user_repository.get_password_hash', return_value='hashed_password'):
                result = repository.create(
                    username="newuser",
                    email="newuser@example.com",
                    password="password123",
                    role="visualizacao"
                )
        
        # Assert
        assert result["id"] == 1
        assert result["username"] == "newuser"
        assert result["email"] == "newuser@example.com"
        assert result["role"] == "visualizacao"
    
    def test_update_user(self):
        """Testa atualização de usuário."""
        # Arrange
        repository = UserRepository()
        mock_row = (1, "updateduser", "updated@example.com", "gerencial", "2024-01-01")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("username",), ("email",), ("role",), ("created_at",)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.update(
                user_id=1,
                username="updateduser",
                email="updated@example.com"
            )
        
        # Assert
        assert result is not None
        assert result["username"] == "updateduser"
        assert result["email"] == "updated@example.com"
    
    def test_update_user_no_changes(self):
        """Testa atualização de usuário sem alterações."""
        # Arrange
        repository = UserRepository()
        
        # Act
        result = repository.update(user_id=1)
        
        # Assert
        assert result is None
    
    def test_delete_user(self):
        """Testa deleção de usuário."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # ID deletado
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.delete(1)
        
        # Assert
        assert result is True
    
    def test_delete_user_not_found(self):
        """Testa deleção de usuário inexistente."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.delete(999)
        
        # Assert
        assert result is False
    
    def test_exists_by_username_true(self):
        """Testa verificação de existência de username quando existe."""
        # Arrange
        repository = UserRepository()
        mock_row = (1, "testuser", "test@example.com", "hashed_pass", "admin", "2024-01-01")
        mock_cursor = MagicMock()
        mock_cursor.description = [("id",), ("username",), ("email",), ("hashed_password",), ("role",), ("created_at",)]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.exists_by_username("testuser")
        
        # Assert
        assert result is True
    
    def test_exists_by_username_false(self):
        """Testa verificação de existência de username quando não existe."""
        # Arrange
        repository = UserRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.exists_by_username("nonexistent")
        
        # Assert
        assert result is False

