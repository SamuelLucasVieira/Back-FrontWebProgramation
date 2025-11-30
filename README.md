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

## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.txt) para mais detalhes.