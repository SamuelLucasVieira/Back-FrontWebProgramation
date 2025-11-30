"""
Módulo de serviços - Service Layer Pattern
Contém a lógica de negócio da aplicação, separada das rotas e do acesso a dados.
"""
from .user_service import UserService
from .task_service import TaskService
from .auth_service import AuthService

__all__ = ['UserService', 'TaskService', 'AuthService']

