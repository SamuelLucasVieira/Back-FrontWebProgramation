# 🧪 Guia de Testes - TDD

Este documento descreve a estratégia de testes do projeto usando TDD (Test-Driven Development).

## 📋 Visão Geral

O projeto utiliza **TDD** (Test-Driven Development) com as seguintes características:

- ✅ **Testes Unitários**: Testam componentes isolados (repositories, services)
- ✅ **Testes de Integração**: Testam a interação entre componentes (endpoints)
- ✅ **Mocks e Stubs**: Isolam dependências para testes rápidos e confiáveis
- ✅ **Cobertura de Código**: Acompanha a porcentagem de código testado

## 🏗️ Arquitetura de Testes

### Camadas de Teste

```
┌─────────────────────────────────────┐
│   Testes de API (Endpoints)          │  ← Testes de Integração
│   - test_auth_endpoints.py           │
│   - test_user_endpoints.py            │
│   - test_task_endpoints.py            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Testes de Services                │  ← Testes de Lógica de Negócio
│   - test_user_service.py             │
│   - test_task_service.py             │
│   - test_auth_service.py             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Testes de Repositories             │  ← Testes de Acesso a Dados
│   - test_user_repository.py          │
│   - test_task_repository.py          │
└─────────────────────────────────────┘
```

## 🎯 Estratégia de Testes

### 1. Testes de Repositórios

**Objetivo**: Testar operações de acesso a dados isoladamente.

**Abordagem**: 
- Mock do cursor do banco de dados
- Testa conversão de dados
- Valida queries SQL indiretamente

**Exemplo**:
```python
def test_find_by_username_success(self):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, "user", "email", ...)
    # Testa busca de usuário
```

### 2. Testes de Services

**Objetivo**: Testar lógica de negócio e validações.

**Abordagem**:
- Mock dos repositórios
- Testa regras de negócio
- Valida tratamento de erros

**Exemplo**:
```python
def test_create_user_username_exists(self, user_service, mock_user_repository):
    mock_user_repository.exists_by_username.return_value = True
    # Deve lançar HTTPException
```

### 3. Testes de API

**Objetivo**: Testar endpoints HTTP e integração completa.

**Abordagem**:
- Usa TestClient do FastAPI
- Mock de autenticação
- Testa respostas HTTP

**Exemplo**:
```python
def test_create_user_success(self, client):
    response = client.post("/users/", json={...})
    assert response.status_code == 201
```

## 📊 Cobertura de Testes

### Métricas Alvo

- **Repositories**: >90% de cobertura
- **Services**: >85% de cobertura
- **Endpoints**: >80% de cobertura
- **Geral**: >80% de cobertura total

### Verificar Cobertura

```bash
# Gerar relatório HTML
pytest --cov=src --cov-report=html

# Abrir relatório
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## 🔄 Ciclo TDD

### 1. Red (Vermelho)
Escreva um teste que falha:
```python
def test_new_feature(self):
    result = service.new_feature()
    assert result == expected
```

### 2. Green (Verde)
Implemente o mínimo necessário para passar:
```python
def new_feature(self):
    return expected
```

### 3. Refactor (Refatorar)
Melhore o código mantendo os testes passando:
```python
def new_feature(self):
    # Código melhorado
    return expected
```

## 🛠️ Ferramentas

### pytest
Framework de testes principal.

### pytest-mock
Para criar mocks facilmente.

### pytest-cov
Para medir cobertura de código.

### httpx
Cliente HTTP para testes de API (usado pelo TestClient do FastAPI).

## 📝 Convenções

### Nomenclatura

- Arquivos: `test_*.py`
- Classes: `Test*`
- Métodos: `test_*`
- Fixtures: `*_fixture` ou nomes descritivos

### Estrutura de Teste

```python
def test_feature_scenario(self, fixtures):
    """Descrição do que está sendo testado."""
    # Arrange - Configurar
    mock.return_value = data
    
    # Act - Executar
    result = service.method()
    
    # Assert - Verificar
    assert result == expected
    mock.assert_called_once()
```

## 🚀 Executando Testes

### Todos os Testes
```bash
pytest
```

### Com Cobertura
```bash
pytest --cov=src --cov-report=html
```

### Testes Específicos
```bash
pytest tests/test_services/test_user_service.py
```

### Modo Watch (desenvolvimento)
```bash
pytest-watch  # Requer instalação: pip install pytest-watch
```

## 📚 Recursos Adicionais

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [TDD Best Practices](https://www.agilealliance.org/glossary/tdd/)

