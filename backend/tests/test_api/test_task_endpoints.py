"""
Testes para endpoints de tarefas - Versão corrigida.
"""
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from tests.helpers import override_auth_dependency, clear_overrides


@pytest.mark.api
class TestTaskEndpoints:
    """Testes para endpoints de tarefas."""
    
    def test_get_tasks_success(self, client):
        """Testa listagem de tarefas."""
        # Arrange
        from src.main import app
        from src.dependencies import get_task_service
        
        mock_tasks = [
            {"id": 1, "titulo": "Tarefa 1", "status": "pendente", "owner_id": 1},
            {"id": 2, "titulo": "Tarefa 2", "status": "em_andamento", "owner_id": 1}
        ]
        
        mock_service = MagicMock()
        mock_service.get_all_tasks.return_value = mock_tasks
        
        override_auth_dependency(app, user_role="visualizacao")
        app.dependency_overrides[get_task_service] = lambda: mock_service
        
        try:
            # Act
            response = client.get(
                "/tasks/",
                headers={"Authorization": "Bearer mock_token"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
        finally:
            clear_overrides(app)
    
    def test_create_task_success(self, client):
        """Testa criação de tarefa."""
        # Arrange
        from src.main import app
        from src.dependencies import get_task_service
        
        mock_created_task = {
            "id": 1,
            "titulo": "Nova Tarefa",
            "descricao": "Descrição",
            "status": "pendente",
            "owner_id": 1,
            "owner_username": "user1"
        }
        
        mock_service = MagicMock()
        mock_service.create_task.return_value = mock_created_task
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_task_service] = lambda: mock_service
        
        try:
            # Act
            response = client.post(
                "/tasks/",
                json={
                    "titulo": "Nova Tarefa",
                    "descricao": "Descrição",
                    "status": "pendente"
                },
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 201
            data = response.json()
            assert data["titulo"] == "Nova Tarefa"
        finally:
            clear_overrides(app)
    
    def test_create_task_unauthorized(self, client):
        """Testa criação de tarefa sem permissão."""
        # Arrange
        from src.main import app
        
        override_auth_dependency(app, user_role="visualizacao", raise_403=True)
        
        try:
            # Act
            response = client.post(
                "/tasks/",
                json={
                    "titulo": "Nova Tarefa",
                    "status": "pendente"
                },
                headers={"Authorization": "Bearer visualizacao_token"}
            )
            
            # Assert
            assert response.status_code == 403
        finally:
            clear_overrides(app)
    
    def test_update_task_success(self, client):
        """Testa atualização de tarefa."""
        # Arrange
        from src.main import app
        from src.dependencies import get_task_service
        
        mock_updated_task = {
            "id": 1,
            "titulo": "Tarefa Atualizada",
            "status": "em_andamento",
            "owner_id": 1
        }
        
        mock_service = MagicMock()
        mock_service.update_task.return_value = mock_updated_task
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_task_service] = lambda: mock_service
        
        try:
            # Act
            response = client.put(
                "/tasks/1",
                json={
                    "titulo": "Tarefa Atualizada",
                    "status": "em_andamento"
                },
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["titulo"] == "Tarefa Atualizada"
        finally:
            clear_overrides(app)
    
    def test_delete_task_success(self, client):
        """Testa deleção de tarefa."""
        # Arrange
        from src.main import app
        from src.dependencies import get_task_service
        
        mock_service = MagicMock()
        mock_service.delete_task.return_value = True
        
        override_auth_dependency(app, user_role="admin")
        app.dependency_overrides[get_task_service] = lambda: mock_service
        
        try:
            # Act
            response = client.delete(
                "/tasks/1",
                headers={"Authorization": "Bearer admin_token"}
            )
            
            # Assert
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
        finally:
            clear_overrides(app)
    
    def test_delete_task_unauthorized(self, client):
        """Testa deleção de tarefa sem permissão (apenas admin pode deletar)."""
        # Arrange
        from src.main import app
        
        override_auth_dependency(app, user_role="gerencial", raise_403=True)
        
        try:
            # Act
            response = client.delete(
                "/tasks/1",
                headers={"Authorization": "Bearer gerencial_token"}
            )
            
            # Assert
            assert response.status_code == 403
        finally:
            clear_overrides(app)

