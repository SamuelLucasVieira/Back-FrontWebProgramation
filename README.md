# 🚀 Gerenciador de Tarefas (To-Do List)

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-green)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Um projeto Full-Stack de um Gerenciador de Tarefas (To-Do List) que demonstra a integração entre um backend robusto em Python com FastAPI e um frontend moderno e responsivo com React e Tailwind CSS.

## ✨ Funcionalidades

-   **➕ Adicionar novas tarefas:** Crie tarefas com título e descrição opcional.
-   **✏️ Editar tarefas existentes:** Altere o título e a descrição de qualquer tarefa.
-   **✔️ Gerenciar status:** Marque tarefas como "concluídas" ou "pendentes" com um único clique.
-   **🗑️ Excluir tarefas:** Remova tarefas que não são mais necessárias.
-   **✨ Interface Reativa:** Frontend construído com React para uma experiência de usuário fluida e dinâmica.
-   **📱 Design Responsivo:** A interface se adapta perfeitamente a desktops e dispositivos móveis graças ao Tailwind CSS.

---

## 💻 Tecnologias Utilizadas

Este projeto é dividido em duas partes principais: o backend e o frontend.

#### **Backend**

| Tecnologia | Descrição                                        |
| :--------- | :------------------------------------------------- |
| **Python** | Linguagem de programação principal.                |
| **FastAPI** | Framework web de alta performance para a API.      |
| **Uvicorn** | Servidor ASGI para rodar a aplicação FastAPI.    |

#### **Frontend**

| Tecnologia      | Descrição                                                    |
| :-------------- | :----------------------------------------------------------- |
| **React** | Biblioteca JavaScript para construir interfaces de usuário.    |
| **Vite** | Ferramenta de build e servidor de desenvolvimento rápido.    |
| **Tailwind CSS** | Framework CSS utility-first para estilização rápida e responsiva. |
| **JavaScript** | Linguagem de programação do frontend.                        |

---

## 📁 Estrutura do Projeto

Para uma melhor organização, sugerimos a seguinte estrutura de pastas:

```text
gerenciador-de-tarefas/
├── backend/
│   ├── src/
│   │   └── main.py          # Código da API FastAPI
│   ├── venv/                # Ambiente virtual do Python
│   └── requirements.txt     # Dependências do Python
└── frontend-react/
    ├── src/                 # Código fonte do React
    ├── package.json         # Dependências e scripts do Node.js
    └── ...
```

---

## 🛠️ Instalação e Configuração

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### **Pré-requisitos**

-   **Node.js** (versão 18 ou superior)
-   **Python** (versão 3.8 ou superior) e **pip**

### **1. Configuração do Backend**

Primeiro, vamos configurar o servidor da API.

```bash
# 1. Clone o repositório (ou navegue até a pasta do projeto)
# ...

# 2. Navegue até a pasta do backend
cd backend

# 3. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# 4. Instale as dependências do Python
pip install -r requirements.txt

# 5. Configure o banco de dados
# Edite o arquivo src/config/config.yaml com suas credenciais do PostgreSQL
# Exemplo:
#   user: postgres
#   host: localhost
#   database: databaseApi
#   password: sua_senha
#   port: 5432
```

**✨ Inicialização Automática do Banco de Dados:**

As tabelas são criadas **automaticamente** quando você iniciar o servidor FastAPI pela primeira vez. O sistema irá:
- Criar os tipos ENUM necessários
- Criar as tabelas `usuarios` e `tarefas`
- Criar os índices
- Criar usuários padrão automaticamente:
  - 👑 **Admin:** `admin` / `admin123`
  - 📊 **Gerencial:** `gerencial` / `gerencial123`
  - 👁️ **Usuário:** `usuario` / `usuario123`

**Se preferir inicializar manualmente**, você pode executar:
```bash
python init_database.py
```

### **2. Configuração do Frontend**

Agora, vamos configurar a interface do usuário em React.

```bash
# 1. Em um novo terminal, navegue até a pasta do frontend
cd frontend-react

# 2. Instale as dependências do Node.js
npm install
```

---

## ▶️ Executando a Aplicação

Para rodar a aplicação, você precisará de **dois terminais abertos** simultaneamente.

#### **Terminal 1: Rodar o Backend**

**Importante:** Execute o comando a partir da pasta `backend`, não da `backend/src`.

```bash
# Navegue até a pasta /backend
cd backend

# Ative o ambiente virtual (se não estiver ativo)
# venv\Scripts\activate  (Windows)
# source venv/bin/activate (macOS/Linux)

# Inicie o servidor FastAPI, apontando para o módulo dentro de 'src'
uvicorn src.main:app --reload --port 3000
```
> O backend estará disponível em `http://localhost:3000`.
> 
> **Nota:** Na primeira execução, as tabelas do banco de dados serão criadas automaticamente. Certifique-se de que o PostgreSQL está rodando e as credenciais no `config.yaml` estão corretas.

#### **Terminal 2: Rodar o Frontend**

```bash
# Navegue até a pasta /frontend-react
cd frontend-react

# Inicie o servidor de desenvolvimento do Vite
npm run dev
```
> A aplicação React estará acessível em `http://localhost:5173` (ou outra porta indicada pelo Vite).

**Abra `http://localhost:5173` no seu navegador para usar a aplicação!**

### 🔐 Credenciais de Login

O sistema cria automaticamente **3 usuários padrão** na primeira inicialização:

| Perfil | Username | Senha | Permissões |
|--------|----------|-------|------------|
| 👑 **Admin** | `admin` | `admin123` | Acesso total ao sistema |
| 📊 **Gerencial** | `gerencial` | `gerencial123` | Gerenciar tarefas e usuários (exceto admins) |
| 👁️ **Usuário** | `usuario` | `usuario123` | Visualizar e atualizar status de tarefas |

> 💡 **Nota:** Consulte `backend/CREDENCIAIS_USUARIOS.md` para detalhes completos sobre as permissões de cada perfil.

---

## 📚 Documentação Interativa da API (Swagger)

O FastAPI gera automaticamente uma documentação interativa da API usando Swagger UI.

### Acessar o Swagger

Após iniciar o backend, acesse:

- **Swagger UI**: `http://localhost:3000/docs`
- **ReDoc** (alternativa): `http://localhost:3000/redoc`

### Funcionalidades do Swagger

- ✅ Visualizar todos os endpoints da API
- ✅ Ver esquemas de dados (schemas)
- ✅ Testar endpoints diretamente no navegador
- ✅ Ver exemplos de requisições e respostas
- ✅ Autenticar e testar endpoints protegidos

### Como usar o Swagger

1. Inicie o backend: `uvicorn src.main:app --reload --port 3000`
2. Abra seu navegador em `http://localhost:3000/docs`
3. Para testar endpoints protegidos:
   - Clique no botão **"Authorize"** no topo da página
   - Faça login primeiro em `/token` para obter um token JWT
   - Cole o token no campo de autorização
   - Agora você pode testar os endpoints protegidos

---

## 🔌 Endpoints da API

A API expõe os seguintes endpoints para manipulação das tarefas:

| Método | Rota               | Descrição                              |
| :----- | :----------------- | :------------------------------------- |
| `GET`  | `/tasks/`          | Lista todas as tarefas.                |
| `POST` | `/tasks/`          | Cria uma nova tarefa.                  |
| `PUT`  | `/tasks/{id}`      | Atualiza uma tarefa existente.         |
| `DELETE`| `/tasks/{id}`      | Exclui uma tarefa.                     |
| `POST` | `/token`           | Autenticação (obter token JWT).        |
| `GET`  | `/users/`          | Lista usuários (admin/gerencial).      |
| `POST` | `/users/`          | Cria usuário (admin).                  |
| `PUT`  | `/users/{id}`      | Atualiza usuário (admin/gerencial).    |
| `DELETE`| `/users/{id}`      | Deleta usuário (admin).                |
| `GET`  | `/users/me/`       | Dados do usuário logado.               |
| `GET`  | `/docs`            | Documentação interativa (Swagger UI).  |
| `GET`  | `/redoc`           | Documentação alternativa (ReDoc).      |

> 💡 **Dica**: Para ver todos os endpoints com detalhes, exemplos e poder testá-los diretamente, acesse `http://localhost:3000/docs` após iniciar o servidor.

---

---

## 🧪 Testes

O projeto utiliza **TDD (Test-Driven Development)** com pytest.

### Executar Testes

```bash
cd backend

# Instalar dependências de teste (se ainda não instalou)
pip install -r requirements.txt

# Executar todos os testes
pytest

# Executar com cobertura de código
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_services/test_user_service.py

# Executar por categoria
pytest -m repository  # Apenas testes de repositórios
pytest -m service     # Apenas testes de serviços
pytest -m api         # Apenas testes de API
```

### Estrutura de Testes

- `tests/test_repositories/` - Testes de repositórios (acesso a dados)
- `tests/test_services/` - Testes de serviços (lógica de negócio)
- `tests/test_api/` - Testes de endpoints (integração)

Para mais detalhes, consulte [TESTING.md](backend/TESTING.md) e [tests/README.md](backend/tests/README.md).

---


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



## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.txt) para mais detalhes.
