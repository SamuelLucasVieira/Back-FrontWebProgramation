"""
Configurações e fixtures compartilhadas para todos os testes.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any

# Importações condicionais para evitar erros se dependências não estiverem instaladas
try:
    from fastapi.testclient import TestClient
    from src.repositories import UserRepository, TaskRepository
    from src.services import UserService, TaskService, AuthService
    # Importar app e schemas de forma lazy para evitar erros de dependências
    _app = None
    _schemas = None
    
    def get_app():
        global _app
        if _app is None:
            from src.main import app as _app_module
            _app = _app_module
        return _app
    
    def get_schemas():
        global _schemas
        if _schemas is None:
            from src.config import schemas as _schemas_module
            _schemas = _schemas_module
        return _schemas
except ImportError as e:
    # Se houver erro de importação, criar mocks básicos
    TestClient = None
    UserRepository = None
    TaskRepository = None
    UserService = None
    TaskService = None
    AuthService = None
    _app = None
    _schemas = None
    
    def get_app():
        raise ImportError("Dependências não instaladas. Execute: pip install -r requirements.txt")
    
    def get_schemas():
        raise ImportError("Dependências não instaladas. Execute: pip install -r requirements.txt")


# ============================================================================
# Fixtures de Aplicação
# ============================================================================

@pytest.fixture
def client():
    """Cliente de teste para a aplicação FastAPI."""
    if TestClient is None:
        pytest.skip("Dependências não instaladas. Execute: pip install -r requirements.txt")
    app = get_app()
    return TestClient(app)


# ============================================================================
# Fixtures de Dados de Teste
# ============================================================================

@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Dados de exemplo para um usuário."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "visualizacao",
        "hashed_password": "$2b$12$EixZa80l8sScZ8jDQ5uresrzQWfBWvA0o1M1bvoUn1gZWtV0I9/Ey",
        "created_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_admin_user() -> Dict[str, Any]:
    """Dados de exemplo para um usuário admin."""
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "hashed_password": "$2b$12$EixZa80l8sScZ8jDQ5uresrzQWfBWvA0o1M1bvoUn1gZWtV0I9/Ey",
        "created_at": "2024-01-01T00:00:00"
    }


@pytest.fixture
def sample_task_data() -> Dict[str, Any]:
    """Dados de exemplo para uma tarefa."""
    return {
        "id": 1,
        "titulo": "Tarefa de Teste",
        "descricao": "Descrição da tarefa de teste",
        "status": "pendente",
        "owner_id": 1,
        "owner_username": "testuser"
    }


@pytest.fixture
def sample_user_schema():
    """Schema de usuário para testes."""
    schemas = get_schemas()
    return schemas.User(
        id=1,
        username="testuser",
        email="test@example.com",
        role="visualizacao"
    )


@pytest.fixture
def sample_user_create():
    """Schema de criação de usuário para testes."""
    schemas = get_schemas()
    return schemas.UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="password123",
        role="visualizacao"
    )


@pytest.fixture
def sample_task_create():
    """Schema de criação de tarefa para testes."""
    schemas = get_schemas()
    return schemas.TaskCreate(
        titulo="Nova Tarefa",
        descricao="Descrição da nova tarefa",
        status="pendente",
        owner_id=1
    )


# ============================================================================
# Fixtures de Repositórios Mockados
# ============================================================================

@pytest.fixture
def mock_user_repository():
    """Repositório de usuários mockado."""
    if UserRepository is None:
        return Mock()
    return Mock(spec=UserRepository)


@pytest.fixture
def mock_task_repository():
    """Repositório de tarefas mockado."""
    if TaskRepository is None:
        return Mock()
    return Mock(spec=TaskRepository)


# ============================================================================
# Fixtures de Serviços
# ============================================================================

@pytest.fixture
def user_service(mock_user_repository):
    """Serviço de usuários com repositório mockado."""
    if UserService is None:
        pytest.skip("Dependências não instaladas. Execute: pip install -r requirements.txt")
    return UserService(repository=mock_user_repository)


@pytest.fixture
def task_service(mock_task_repository, mock_user_repository):
    """Serviço de tarefas com repositórios mockados."""
    if TaskService is None:
        pytest.skip("Dependências não instaladas. Execute: pip install -r requirements.txt")
    return TaskService(
        task_repository=mock_task_repository,
        user_repository=mock_user_repository
    )


@pytest.fixture
def auth_service(mock_user_repository):
    """Serviço de autenticação com repositório mockado."""
    if AuthService is None:
        pytest.skip("Dependências não instaladas. Execute: pip install -r requirements.txt")
    return AuthService(repository=mock_user_repository)


# ============================================================================
# Fixtures de Tokens JWT
# ============================================================================

@pytest.fixture
def admin_token():
    """Token JWT para usuário admin (mock)."""
    return "mock_admin_token"


@pytest.fixture
def gerencial_token():
    """Token JWT para usuário gerencial (mock)."""
    return "mock_gerencial_token"


@pytest.fixture
def visualizacao_token():
    """Token JWT para usuário visualização (mock)."""
    return "mock_visualizacao_token"


# ============================================================================
# Fixtures de Autenticação
# ============================================================================

@pytest.fixture
def authenticated_admin_client(client, admin_token):
    """Cliente autenticado como admin."""
    client.headers.update({"Authorization": f"Bearer {admin_token}"})
    return client


@pytest.fixture
def authenticated_gerencial_client(client, gerencial_token):
    """Cliente autenticado como gerencial."""
    client.headers.update({"Authorization": f"Bearer {gerencial_token}"})
    return client

