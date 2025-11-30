"""
Testes para TaskService - Service Layer Pattern
Testa a lógica de negócio relacionada a tarefas.
"""
import pytest
from fastapi import HTTPException
from src.services.task_service import TaskService
from src.config import schemas
from tests.conftest import mock_task_repository, mock_user_repository


@pytest.mark.service
class TestTaskService:
    """Testes para TaskService."""
    
    def test_get_all_tasks(self, task_service, mock_task_repository):
        """Testa listagem de todas as tarefas."""
        # Arrange
        mock_tasks = [
            {"id": 1, "titulo": "Tarefa 1", "status": "pendente"},
            {"id": 2, "titulo": "Tarefa 2", "status": "em_andamento"}
        ]
        mock_task_repository.find_all.return_value = mock_tasks
        
        # Act
        result = task_service.get_all_tasks()
        
        # Assert
        assert len(result) == 2
        mock_task_repository.find_all.assert_called_once()
    
    def test_get_task_by_id_success(self, task_service, mock_task_repository, sample_task_data):
        """Testa busca de tarefa por ID com sucesso."""
        # Arrange
        mock_task_repository.find_by_id.return_value = sample_task_data
        
        # Act
        result = task_service.get_task_by_id(1)
        
        # Assert
        assert result is not None
        assert result["id"] == 1
        mock_task_repository.find_by_id.assert_called_once_with(1)
    
    def test_get_task_by_id_not_found(self, task_service, mock_task_repository):
        """Testa busca de tarefa por ID quando não encontrada."""
        # Arrange
        mock_task_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task_by_id(999)
        
        assert exc_info.value.status_code == 404
        assert "Tarefa não encontrada" in str(exc_info.value.detail)
    
    def test_create_task_success(self, task_service, mock_task_repository, sample_task_create):
        """Testa criação de tarefa com sucesso."""
        # Arrange
        created_task = {
            "id": 1,
            "titulo": "Nova Tarefa",
            "descricao": "Descrição",
            "status": "pendente",
            "owner_id": 1,
            "owner_username": "user1"
        }
        mock_task_repository.create.return_value = created_task
        
        # Act
        result = task_service.create_task(sample_task_create, current_user_id=1)
        
        # Assert
        assert result["titulo"] == "Nova Tarefa"
        mock_task_repository.create.assert_called_once()
    
    def test_create_task_with_owner_id(self, task_service, mock_task_repository, mock_user_repository):
        """Testa criação de tarefa atribuída a outro usuário."""
        # Arrange
        task_create = schemas.TaskCreate(
            titulo="Nova Tarefa",
            descricao="Descrição",
            status="pendente",
            owner_id=2
        )
        target_user = {"id": 2, "username": "user2", "role": "visualizacao"}
        created_task = {"id": 1, "titulo": "Nova Tarefa", "owner_id": 2}
        
        mock_user_repository.find_by_id.return_value = target_user
        mock_task_repository.create.return_value = created_task
        
        # Act
        result = task_service.create_task(task_create, current_user_id=1)
        
        # Assert
        assert result["owner_id"] == 2
        mock_user_repository.find_by_id.assert_called_once_with(2)
        mock_task_repository.create.assert_called_once()
    
    def test_create_task_owner_not_found(self, task_service, mock_task_repository, mock_user_repository):
        """Testa criação de tarefa com owner_id inexistente."""
        # Arrange
        task_create = schemas.TaskCreate(
            titulo="Nova Tarefa",
            owner_id=999
        )
        mock_user_repository.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            task_service.create_task(task_create, current_user_id=1)
        
        assert exc_info.value.status_code == 404
        assert "Usuário destino não encontrado" in str(exc_info.value.detail)
    
    def test_update_task_admin_success(self, task_service, mock_task_repository, mock_user_repository):
        """Testa atualização de tarefa por admin."""
        # Arrange
        existing_task = {"id": 1, "titulo": "Tarefa Antiga", "status": "pendente"}
        updated_task = {"id": 1, "titulo": "Tarefa Atualizada", "status": "em_andamento"}
        task_update = schemas.TaskCreate(
            titulo="Tarefa Atualizada",
            descricao="Nova descrição",
            status="em_andamento"
        )
        
        mock_task_repository.find_by_id.side_effect = [existing_task, updated_task]
        mock_task_repository.update.return_value = True
        
        # Act
        result = task_service.update_task(1, task_update, "admin")
        
        # Assert
        assert result["titulo"] == "Tarefa Atualizada"
        mock_task_repository.update.assert_called_once()
    
    def test_update_task_visualizacao_cannot_complete(self, task_service, mock_task_repository):
        """Testa que visualização não pode concluir tarefas."""
        # Arrange
        existing_task = {"id": 1, "titulo": "Tarefa", "status": "pendente"}
        task_update = schemas.TaskCreate(titulo="Tarefa", status="concluida")
        
        mock_task_repository.find_by_id.return_value = existing_task
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(1, task_update, "visualizacao")
        
        assert exc_info.value.status_code == 403
        assert "não podem concluir tarefas" in str(exc_info.value.detail)
    
    def test_update_task_visualizacao_can_update_status(self, task_service, mock_task_repository):
        """Testa que visualização pode atualizar status (exceto concluida)."""
        # Arrange
        existing_task = {"id": 1, "titulo": "Tarefa", "status": "pendente"}
        updated_task = {"id": 1, "titulo": "Tarefa", "status": "em_andamento"}
        task_update = schemas.TaskCreate(titulo="Tarefa", status="em_andamento")
        
        mock_task_repository.find_by_id.side_effect = [existing_task, updated_task]
        mock_task_repository.update.return_value = True
        
        # Act
        result = task_service.update_task(1, task_update, "visualizacao")
        
        # Assert
        assert result["status"] == "em_andamento"
        # Deve atualizar apenas status, ignorando outros campos
        call_args = mock_task_repository.update.call_args
        assert call_args[1]["titulo"] is None
        assert call_args[1]["status"] == "em_andamento"
    
    def test_update_task_not_found(self, task_service, mock_task_repository):
        """Testa atualização de tarefa inexistente."""
        # Arrange
        mock_task_repository.find_by_id.return_value = None
        task_update = schemas.TaskCreate(titulo="Nova Tarefa")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(999, task_update, "admin")
        
        assert exc_info.value.status_code == 404
        assert "Tarefa não encontrada" in str(exc_info.value.detail)
    
    def test_delete_task_success(self, task_service, mock_task_repository):
        """Testa deleção de tarefa com sucesso."""
        # Arrange
        mock_task_repository.delete.return_value = True
        
        # Act
        result = task_service.delete_task(1)
        
        # Assert
        assert result is True
        mock_task_repository.delete.assert_called_once_with(1)
    
    def test_delete_task_not_found(self, task_service, mock_task_repository):
        """Testa deleção de tarefa inexistente."""
        # Arrange
        mock_task_repository.delete.return_value = False
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            task_service.delete_task(999)
        
        assert exc_info.value.status_code == 404
        assert "Tarefa não encontrada" in str(exc_info.value.detail)

