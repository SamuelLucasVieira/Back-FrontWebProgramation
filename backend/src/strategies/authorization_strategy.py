"""
Estratégias de Autorização - Strategy Pattern
Define diferentes estratégias de autorização baseadas no perfil do usuário.
"""
from abc import ABC, abstractmethod
from typing import List
from src.config import schemas


class AuthorizationStrategy(ABC):
    """Interface base para estratégias de autorização."""
    
    @abstractmethod
    def can_list_users(self) -> bool:
        """Verifica se pode listar usuários."""
        pass
    
    @abstractmethod
    def can_create_users(self) -> bool:
        """Verifica se pode criar usuários."""
        pass
    
    @abstractmethod
    def can_edit_user(self, target_user: schemas.User) -> bool:
        """Verifica se pode editar um usuário específico."""
        pass
    
    @abstractmethod
    def can_delete_users(self) -> bool:
        """Verifica se pode deletar usuários."""
        pass
    
    @abstractmethod
    def can_create_tasks(self) -> bool:
        """Verifica se pode criar tarefas."""
        pass
    
    @abstractmethod
    def can_edit_task(self, task: dict) -> bool:
        """Verifica se pode editar uma tarefa específica."""
        pass
    
    @abstractmethod
    def can_delete_tasks(self) -> bool:
        """Verifica se pode deletar tarefas."""
        pass
    
    @abstractmethod
    def can_complete_task(self) -> bool:
        """Verifica se pode concluir tarefas."""
        pass


class AdminStrategy(AuthorizationStrategy):
    """Estratégia de autorização para administradores."""
    
    def can_list_users(self) -> bool:
        return True
    
    def can_create_users(self) -> bool:
        return True
    
    def can_edit_user(self, target_user: schemas.User) -> bool:
        return True
    
    def can_delete_users(self) -> bool:
        return True
    
    def can_create_tasks(self) -> bool:
        return True
    
    def can_edit_task(self, task: dict) -> bool:
        return True
    
    def can_delete_tasks(self) -> bool:
        return True
    
    def can_complete_task(self) -> bool:
        return True


class GerencialStrategy(AuthorizationStrategy):
    """Estratégia de autorização para usuários gerenciais."""
    
    def can_list_users(self) -> bool:
        return True
    
    def can_create_users(self) -> bool:
        return False
    
    def can_edit_user(self, target_user: schemas.User) -> bool:
        # Gerencial não pode editar admin
        return target_user.role != "admin"
    
    def can_delete_users(self) -> bool:
        return False
    
    def can_create_tasks(self) -> bool:
        return True
    
    def can_edit_task(self, task: dict) -> bool:
        return True
    
    def can_delete_tasks(self) -> bool:
        return False
    
    def can_complete_task(self) -> bool:
        return True


class VisualizacaoStrategy(AuthorizationStrategy):
    """Estratégia de autorização para usuários de visualização."""
    
    def can_list_users(self) -> bool:
        return False
    
    def can_create_users(self) -> bool:
        return False
    
    def can_edit_user(self, target_user: schemas.User) -> bool:
        return False
    
    def can_delete_users(self) -> bool:
        return False
    
    def can_create_tasks(self) -> bool:
        return False
    
    def can_edit_task(self, task: dict) -> bool:
        # Visualização pode alterar apenas o status (mas não pode concluir)
        return True
    
    def can_delete_tasks(self) -> bool:
        return False
    
    def can_complete_task(self) -> bool:
        return False


def get_authorization_strategy(role: str) -> AuthorizationStrategy:
    """Factory function para obter a estratégia de autorização baseada no role."""
    strategies = {
        "admin": AdminStrategy(),
        "gerencial": GerencialStrategy(),
        "visualizacao": VisualizacaoStrategy()
    }
    return strategies.get(role, VisualizacaoStrategy())

