"""
Módulo de estratégias - Strategy Pattern
Implementa diferentes estratégias para autorização e permissões.
"""
from .authorization_strategy import AuthorizationStrategy, AdminStrategy, GerencialStrategy, VisualizacaoStrategy

__all__ = [
    'AuthorizationStrategy',
    'AdminStrategy',
    'GerencialStrategy',
    'VisualizacaoStrategy'
]

