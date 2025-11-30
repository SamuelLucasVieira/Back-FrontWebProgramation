"""
Testes para TaskRepository - Repository Pattern
Testa as operações de acesso a dados de tarefas.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.repositories.task_repository import TaskRepository


@pytest.mark.repository
class TestTaskRepository:
    """Testes para TaskRepository."""
    
    def test_find_all(self):
        """Testa busca de todas as tarefas."""
        # Arrange
        repository = TaskRepository()
        mock_rows = [
            (1, "Tarefa 1", "Desc 1", "pendente", 1, None, "user1"),
            (2, "Tarefa 2", "Desc 2", "em_andamento", 1, None, "user1")
        ]
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("titulo",), ("descricao",), ("status",), ("owner_id",), ("created_at",), ("owner_username",)
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_all()
        
        # Assert
        assert len(result) == 2
        assert result[0]["titulo"] == "Tarefa 1"
        assert result[1]["titulo"] == "Tarefa 2"
    
    def test_find_by_id_success(self):
        """Testa busca de tarefa por ID com sucesso."""
        # Arrange
        repository = TaskRepository()
        mock_row = (1, "Tarefa 1", "Desc 1", "pendente", 1, None, "user1")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("titulo",), ("descricao",), ("status",), ("owner_id",), ("created_at",), ("owner_username",)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_id(1)
        
        # Assert
        assert result is not None
        assert result["id"] == 1
        assert result["titulo"] == "Tarefa 1"
    
    def test_find_by_id_not_found(self):
        """Testa busca de tarefa por ID quando não encontrada."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_id(999)
        
        # Assert
        assert result is None
    
    def test_find_by_owner(self):
        """Testa busca de tarefas por owner."""
        # Arrange
        repository = TaskRepository()
        mock_rows = [
            (1, "Tarefa 1", "Desc 1", "pendente", 1, None, "user1"),
            (2, "Tarefa 2", "Desc 2", "em_andamento", 1, None, "user1")
        ]
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("titulo",), ("descricao",), ("status",), ("owner_id",), ("created_at",), ("owner_username",)
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_owner(1)
        
        # Assert
        assert len(result) == 2
        assert all(task["owner_id"] == 1 for task in result)
    
    def test_find_by_status(self):
        """Testa busca de tarefas por status."""
        # Arrange
        repository = TaskRepository()
        mock_rows = [
            (1, "Tarefa 1", "Desc 1", "pendente", 1, None, "user1"),
            (2, "Tarefa 2", "Desc 2", "pendente", 2, None, "user2")
        ]
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("titulo",), ("descricao",), ("status",), ("owner_id",), ("created_at",), ("owner_username",)
        ]
        mock_cursor.fetchall.return_value = mock_rows
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.find_by_status("pendente")
        
        # Assert
        assert len(result) == 2
        assert all(task["status"] == "pendente" for task in result)
    
    def test_create_task(self):
        """Testa criação de nova tarefa."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # ID retornado
        
        # Mock para buscar username do owner
        mock_owner_cursor = MagicMock()
        mock_owner_cursor.fetchone.return_value = ("user1",)
        
        # Act
        call_count = [0]  # Usar lista para permitir modificação dentro da closure
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            # Primeira chamada: criar tarefa
            if call_count[0] == 1:
                return lambda processor: processor(mock_cursor)
            # Segunda chamada: buscar owner (dentro do process_result)
            return lambda processor: processor(mock_owner_cursor)
        
        with patch.object(repository, '_execute_with_cursor', side_effect=side_effect):
            result = repository.create(
                titulo="Nova Tarefa",
                descricao="Descrição",
                status="pendente",
                owner_id=1
            )
        
        # Assert
        assert result["id"] == 1
        assert result["titulo"] == "Nova Tarefa"
        assert result["status"] == "pendente"
        assert result["owner_id"] == 1
        assert result["owner_username"] == "user1"
    
    def test_update_task(self):
        """Testa atualização de tarefa."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # ID atualizado
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.update(
                task_id=1,
                titulo="Tarefa Atualizada",
                status="em_andamento"
            )
        
        # Assert
        assert result is True
    
    def test_update_task_no_changes(self):
        """Testa atualização de tarefa sem alterações."""
        # Arrange
        repository = TaskRepository()
        
        # Act
        result = repository.update(task_id=1)
        
        # Assert
        assert result is False
    
    def test_delete_task(self):
        """Testa deleção de tarefa."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)  # ID deletado
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.delete(1)
        
        # Assert
        assert result is True
    
    def test_delete_task_not_found(self):
        """Testa deleção de tarefa inexistente."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.delete(999)
        
        # Assert
        assert result is False
    
    def test_exists_true(self):
        """Testa verificação de existência de tarefa quando existe."""
        # Arrange
        repository = TaskRepository()
        mock_row = (1, "Tarefa 1", "Desc 1", "pendente", 1, None, "user1")
        mock_cursor = MagicMock()
        mock_cursor.description = [
            ("id",), ("titulo",), ("descricao",), ("status",), ("owner_id",), ("created_at",), ("owner_username",)
        ]
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.exists(1)
        
        # Assert
        assert result is True
    
    def test_exists_false(self):
        """Testa verificação de existência de tarefa quando não existe."""
        # Arrange
        repository = TaskRepository()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        # Act
        with patch.object(repository, '_execute_with_cursor') as mock_exec:
            mock_exec.return_value = lambda processor: processor(mock_cursor)
            result = repository.exists(999)
        
        # Assert
        assert result is False

