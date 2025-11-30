"""
Módulo de repositórios - Repository Pattern
Abstrai o acesso ao banco de dados, separando a lógica de persistência.
"""
from .user_repository import UserRepository
from .task_repository import TaskRepository

__all__ = ['UserRepository', 'TaskRepository']

