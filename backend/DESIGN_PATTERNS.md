# 🏗️ Design Patterns Aplicados no Backend

Este documento descreve os Design Patterns implementados no projeto para melhorar a arquitetura, manutenibilidade e testabilidade do código.

## 📋 Padrões Implementados

### 1. **Repository Pattern** (Padrão de Repositório)

**Localização:** `src/repositories/`

**Objetivo:** Abstrair o acesso ao banco de dados, separando a lógica de persistência da lógica de negócio.

**Estrutura:**
```
repositories/
├── __init__.py
├── base_repository.py      # Classe base com métodos utilitários
├── user_repository.py      # Repositório de usuários
└── task_repository.py      # Repositório de tarefas
```

**Benefícios:**
- ✅ Facilita testes unitários (pode mockar repositórios)
- ✅ Permite trocar o banco de dados sem alterar a lógica de negócio
- ✅ Centraliza queries SQL
- ✅ Reutilização de código através de `BaseRepository`

**Exemplo de uso:**
```python
from src.repositories import UserRepository

repository = UserRepository()
user = repository.find_by_username("admin")
```

---

### 2. **Service Layer Pattern** (Camada de Serviço)

**Localização:** `src/services/`

**Objetivo:** Separar a lógica de negócio das rotas HTTP e do acesso a dados.

**Estrutura:**
```
services/
├── __init__.py
├── user_service.py      # Lógica de negócio de usuários
├── task_service.py      # Lógica de negócio de tarefas
└── auth_service.py      # Lógica de autenticação
```

**Benefícios:**
- ✅ Lógica de negócio reutilizável
- ✅ Rotas HTTP mais limpas e focadas
- ✅ Facilita testes de lógica de negócio
- ✅ Validações e regras de negócio centralizadas

**Exemplo de uso:**
```python
from src.services import UserService

service = UserService()
user = service.create_user(user_data)
```

---

### 3. **Dependency Injection** (Injeção de Dependências)

**Localização:** `src/dependencies.py` e uso via FastAPI `Depends()`

**Objetivo:** Inverter o controle de dependências, facilitando testes e manutenção.

**Estrutura:**
```python
# dependencies.py
def get_user_service() -> UserService:
    return UserService()

# main.py
@app.get("/users/")
def read_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()
```

**Benefícios:**
- ✅ Facilita testes (pode injetar mocks)
- ✅ Baixo acoplamento entre componentes
- ✅ Fácil substituição de implementações
- ✅ Integração nativa com FastAPI

---

### 4. **Strategy Pattern** (Padrão de Estratégia)

**Localização:** `src/strategies/`

**Objetivo:** Definir diferentes estratégias de autorização baseadas no perfil do usuário.

**Estrutura:**
```
strategies/
├── __init__.py
└── authorization_strategy.py
    ├── AuthorizationStrategy (interface)
    ├── AdminStrategy
    ├── GerencialStrategy
    └── VisualizacaoStrategy
```

**Benefícios:**
- ✅ Fácil adicionar novos perfis de acesso
- ✅ Lógica de autorização isolada e testável
- ✅ Evita múltiplos `if/else` nas rotas
- ✅ Código mais limpo e manutenível

**Exemplo de uso:**
```python
from src.strategies import get_authorization_strategy

strategy = get_authorization_strategy("admin")
if strategy.can_create_users():
    # criar usuário
```

---

### 5. **Factory Pattern** (Padrão de Fábrica)

**Localização:** `src/strategies/authorization_strategy.py`

**Objetivo:** Criar instâncias de estratégias baseadas em parâmetros.

**Implementação:**
```python
def get_authorization_strategy(role: str) -> AuthorizationStrategy:
    strategies = {
        "admin": AdminStrategy(),
        "gerencial": GerencialStrategy(),
        "visualizacao": VisualizacaoStrategy()
    }
    return strategies.get(role, VisualizacaoStrategy())
```

**Benefícios:**
- ✅ Centraliza a criação de objetos
- ✅ Facilita adicionar novas estratégias
- ✅ Encapsula a lógica de seleção

---

## 🏛️ Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│         FastAPI Routes               │  ← Camada de Apresentação
│         (main.py)                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Services Layer               │  ← Camada de Lógica de Negócio
│  (UserService, TaskService, etc)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Repositories                 │  ← Camada de Acesso a Dados
│  (UserRepository, TaskRepository)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Database                     │  ← Banco de Dados
│         (PostgreSQL)                 │
└─────────────────────────────────────┘
```

---

## 📦 Estrutura de Diretórios

```
backend/src/
├── config/              # Configurações (schemas, database, etc)
├── core/                # Funcionalidades centrais (security)
├── models/              # Modelos antigos (mantidos para compatibilidade)
├── repositories/        # ✨ Repository Pattern
│   ├── base_repository.py
│   ├── user_repository.py
│   └── task_repository.py
├── services/            # ✨ Service Layer Pattern
│   ├── user_service.py
│   ├── task_service.py
│   └── auth_service.py
├── strategies/          # ✨ Strategy Pattern
│   └── authorization_strategy.py
├── dependencies.py      # ✨ Dependency Injection
└── main.py              # Rotas FastAPI
```

---

## 🔄 Fluxo de Dados

### Exemplo: Criar um Usuário

1. **Rota HTTP** (`main.py`)
   ```python
   @app.post("/users/")
   def create_user(user: UserCreate, service: UserService = Depends(...)):
       return service.create_user(user)
   ```

2. **Service Layer** (`user_service.py`)
   ```python
   def create_user(self, user_data):
       # Validações de negócio
       if self.repository.exists_by_username(...):
           raise HTTPException(...)
       # Chama repositório
       return self.repository.create(...)
   ```

3. **Repository** (`user_repository.py`)
   ```python
   def create(self, username, email, ...):
       # Executa SQL
       cursor.execute("INSERT INTO usuarios ...")
       return result
   ```

---

## ✅ Benefícios Gerais

1. **Manutenibilidade:** Código organizado e fácil de entender
2. **Testabilidade:** Cada camada pode ser testada independentemente
3. **Escalabilidade:** Fácil adicionar novas funcionalidades
4. **Reutilização:** Lógica de negócio pode ser reutilizada
5. **Separação de Responsabilidades:** Cada camada tem uma responsabilidade clara

---

## 🧪 Testabilidade

Com essa arquitetura, é fácil criar testes:

```python
# Teste de Service (mock do Repository)
def test_create_user():
    mock_repo = Mock(UserRepository)
    service = UserService(repository=mock_repo)
    # ... testar lógica de negócio
```

---

## 📚 Referências

- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Dependency Injection](https://martinfowler.com/articles/injection.html)

