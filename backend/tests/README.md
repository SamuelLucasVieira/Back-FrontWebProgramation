# 🧪 Testes - TDD (Test-Driven Development)

Este diretório contém todos os testes do projeto, organizados seguindo os princípios de TDD.

## 📁 Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py                    # Fixtures e configurações compartilhadas
├── test_repositories/             # Testes de repositórios (Repository Pattern)
│   ├── test_user_repository.py
│   └── test_task_repository.py
├── test_services/                 # Testes de serviços (Service Layer)
│   ├── test_user_service.py
│   ├── test_task_service.py
│   └── test_auth_service.py
└── test_api/                      # Testes de endpoints/API
    ├── test_auth_endpoints.py
    ├── test_user_endpoints.py
    └── test_task_endpoints.py
```

## 🚀 Como Executar os Testes

### Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes com Cobertura

```bash
pytest --cov=src --cov-report=html
```

Isso gerará um relatório HTML em `htmlcov/index.html`.

### Executar Testes por Categoria

```bash
# Apenas testes de repositórios
pytest -m repository

# Apenas testes de serviços
pytest -m service

# Apenas testes de API
pytest -m api

# Apenas testes de autenticação
pytest -m auth

# Apenas testes unitários
pytest -m unit
```

### Executar Testes Específicos

```bash
# Um arquivo específico
pytest tests/test_services/test_user_service.py

# Uma classe específica
pytest tests/test_services/test_user_service.py::TestUserService

# Um teste específico
pytest tests/test_services/test_user_service.py::TestUserService::test_create_user_success
```

### Executar com Verbosidade

```bash
# Mais detalhes
pytest -v

# Ainda mais detalhes
pytest -vv

# Mostrar prints
pytest -s
```

## 📊 Cobertura de Código

O projeto está configurado para gerar relatórios de cobertura:

```bash
# Gerar relatório HTML
pytest --cov=src --cov-report=html

# Gerar relatório no terminal
pytest --cov=src --cov-report=term-missing

# Gerar relatório XML (para CI/CD)
pytest --cov=src --cov-report=xml
```

## 🏷️ Marcadores de Teste

Os testes são marcados com categorias para facilitar a execução seletiva:

- `@pytest.mark.repository` - Testes de repositórios
- `@pytest.mark.service` - Testes de serviços
- `@pytest.mark.api` - Testes de API/endpoints
- `@pytest.mark.auth` - Testes de autenticação
- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração

## 🔧 Fixtures Disponíveis

As fixtures estão definidas em `conftest.py`:

### Fixtures de Dados
- `sample_user_data` - Dados de exemplo de usuário
- `sample_admin_user` - Dados de usuário admin
- `sample_task_data` - Dados de exemplo de tarefa
- `sample_user_schema` - Schema de usuário
- `sample_user_create` - Schema de criação de usuário
- `sample_task_create` - Schema de criação de tarefa

### Fixtures de Mocks
- `mock_user_repository` - Repositório de usuários mockado
- `mock_task_repository` - Repositório de tarefas mockado

### Fixtures de Serviços
- `user_service` - Serviço de usuários com repositório mockado
- `task_service` - Serviço de tarefas com repositórios mockados
- `auth_service` - Serviço de autenticação com repositório mockado

### Fixtures de Cliente
- `client` - Cliente de teste FastAPI
- `authenticated_admin_client` - Cliente autenticado como admin
- `authenticated_gerencial_client` - Cliente autenticado como gerencial

## 📝 Escrevendo Novos Testes

### Estrutura de um Teste

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.service
class TestMyService:
    """Testes para MyService."""
    
    def test_my_method_success(self, my_service, mock_repository):
        """Testa método com sucesso."""
        # Arrange
        mock_repository.find.return_value = {"id": 1, "name": "Test"}
        
        # Act
        result = my_service.my_method(1)
        
        # Assert
        assert result["name"] == "Test"
        mock_repository.find.assert_called_once_with(1)
    
    def test_my_method_not_found(self, my_service, mock_repository):
        """Testa método quando não encontrado."""
        # Arrange
        mock_repository.find.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            my_service.my_method(999)
        
        assert exc_info.value.status_code == 404
```

### Padrão AAA (Arrange-Act-Assert)

Todos os testes seguem o padrão AAA:

1. **Arrange** - Configurar dados e mocks
2. **Act** - Executar a ação sendo testada
3. **Assert** - Verificar os resultados

## 🎯 Boas Práticas

1. **Nomes Descritivos**: Use nomes que descrevam claramente o que está sendo testado
2. **Um Teste, Uma Coisa**: Cada teste deve verificar uma única funcionalidade
3. **Testes Independentes**: Testes não devem depender uns dos outros
4. **Mocks e Stubs**: Use mocks para isolar unidades de código
5. **Cobertura**: Procure manter alta cobertura de código (idealmente >80%)

## 🐛 Troubleshooting

### Erro: ModuleNotFoundError

Certifique-se de estar executando os testes a partir do diretório `backend`:

```bash
cd backend
pytest
```

### Erro: Import Error

Verifique se todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

### Testes Lentos

Use marcadores para executar apenas os testes necessários:

```bash
pytest -m "not integration"
```

## 📚 Recursos

- [Documentação do pytest](https://docs.pytest.org/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

