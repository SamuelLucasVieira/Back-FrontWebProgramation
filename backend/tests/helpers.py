"""
Helpers para testes - Funções auxiliares para mockar dependências do FastAPI.
"""
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.config import schemas


def create_mock_user(role="admin", user_id=1, username="admin"):
    """Cria um mock de usuário."""
    return schemas.User(
        id=user_id,
        username=username,
        email=f"{username}@example.com",
        role=role
    )


def override_auth_dependency(app, user_role="admin", user_id=1, username="admin", raise_403=False):
    """Override da dependência de autenticação."""
    from src.models import auth
    mock_user = create_mock_user(role=user_role, user_id=user_id, username=username)
    
    def mock_get_current_user():
        return mock_user
    
    # require_role retorna uma função que é uma dependência assíncrona
    # Vamos criar uma função que retorna uma função mockada
    def create_mock_require_role(required_roles):
        def role_checker():
            if raise_403 or mock_user.role not in required_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Acesso negado. Requer um dos seguintes papéis: {', '.join(required_roles)}"
                )
            return mock_user
        return role_checker
    
    # Override das dependências
    app.dependency_overrides[auth.get_current_user] = mock_get_current_user
    
    # Para require_role, precisamos fazer override da função retornada
    # Mas como ela é chamada com diferentes required_roles, vamos criar uma função genérica
    def mock_require_role_factory(required_roles):
        return create_mock_require_role(required_roles)
    
    # Salvar a função original e substituir temporariamente
    if not hasattr(app, '_original_require_role'):
        app._original_require_role = auth.require_role
    
    # Criar uma nova função que retorna o mock
    def new_require_role(required_roles):
        return create_mock_require_role(required_roles)
    
    auth.require_role = new_require_role
    
    return mock_user


def clear_overrides(app):
    """Limpa todos os overrides de dependências."""
    from src.models import auth
    app.dependency_overrides.clear()
    # Restaurar função original se foi salva
    if hasattr(app, '_original_require_role'):
        auth.require_role = app._original_require_role
        del app._original_require_role

