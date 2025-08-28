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

# 4. Crie o arquivo requirements.txt com o seguinte conteúdo:
# fastapi
# uvicorn[standard]

# 5. Instale as dependências do Python
pip install -r requirements.txt
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

#### **Terminal 2: Rodar o Frontend**

```bash
# Navegue até a pasta /frontend-react
cd frontend-react

# Inicie o servidor de desenvolvimento do Vite
npm run dev
```
> A aplicação React estará acessível em `http://localhost:5173` (ou outra porta indicada pelo Vite).

**Abra `http://localhost:5173` no seu navegador para usar a aplicação!**

---

## 🔌 Endpoints da API

A API expõe os seguintes endpoints para manipulação das tarefas:

| Método | Rota               | Descrição                              |
| :----- | :----------------- | :------------------------------------- |
| `GET`  | `/tarefas`         | Lista todas as tarefas.                |
| `POST` | `/tarefas`         | Cria uma nova tarefa.                  |
| `PUT`  | `/tarefas/{id}`    | Atualiza uma tarefa existente.         |
| `DELETE`| `/tarefas/{id}`    | Exclui uma tarefa.                     |
| `GET`  | `/docs`            | Acessa a documentação interativa (Swagger UI). |

---

## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.txt) para mais detalhes.