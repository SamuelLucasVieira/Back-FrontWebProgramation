"""
Módulo de Dependências - Dependency Injection
Fornece funções de dependência para injeção no FastAPI.
"""
from src.services import UserService, TaskService, AuthService
from src.services.notification_service import NotificationService
from src.repositories import UserRepository, TaskRepository

# Instância compartilhada do NotificationService (singleton)
_shared_notification_service = None

def get_user_service() -> UserService:
    """Retorna uma instância do UserService."""
    return UserService()


def get_task_service() -> TaskService:
    """Retorna uma instância do TaskService com NotificationService compartilhado."""
    global _shared_notification_service
    if _shared_notification_service is None:
        _shared_notification_service = NotificationService()
    return TaskService(notification_service=_shared_notification_service)


def get_auth_service() -> AuthService:
    """Retorna uma instância do AuthService."""
    return AuthService()


def get_notification_service() -> NotificationService:
    """Retorna a instância compartilhada do NotificationService (singleton)."""
    global _shared_notification_service
    if _shared_notification_service is None:
        _shared_notification_service = NotificationService()
    return _shared_notification_service

