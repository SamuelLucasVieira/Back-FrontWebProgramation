# 📋 Instruções - Novas Funcionalidades

## ✅ Funcionalidades Implementadas

### 1. 🎯 Sistema Kanban para Tarefas

O sistema de tarefas agora utiliza um board kanban com 4 colunas:

- **Pendente** (cinza) - Tarefas ainda não iniciadas
- **Em Andamento** (azul) - Tarefas que estão sendo trabalhadas
- **Em Revisão** (amarelo) - Tarefas que precisam ser revisadas
- **Concluída** (verde) - Tarefas finalizadas

#### Funcionalidades do Kanban:
- ✅ Arrastar e soltar tarefas entre colunas (drag and drop)
- ✅ Alterar status através de um dropdown no card da tarefa
- ✅ Editar tarefas diretamente no card
- ✅ Visualização por colunas com contador de tarefas

### 2. 👥 Gerenciador de Usuários

Interface completa para gerenciamento de usuários com controle de acesso por perfil.

#### Funcionalidades:
- ✅ Listar todos os usuários (apenas admin)
- ✅ Criar novos usuários
- ✅ Editar usuários existentes (username, email, senha, perfil)
- ✅ Deletar usuários
- ✅ Visualização de perfis com cores diferenciadas

#### Perfis de Acesso:
- **Administrador** (admin) - Acesso completo ao sistema
- **Gerencial** (gerencial) - Pode criar e editar tarefas
- **Visualização** (visualizacao) - Apenas visualiza tarefas

### 3. 🔐 Sistema de Autenticação

- ✅ Tela de login
- ✅ Autenticação via JWT
- ✅ Proteção de rotas baseada em perfil
- ✅ Logout
- ✅ Persistência de sessão (localStorage)

## 🚀 Como Usar

### Passo 1: Atualizar o Banco de Dados

Se você já tem um banco de dados existente, execute o script de migração:

```sql
-- Execute o arquivo: backend/src/models/migrate_kanban.sql
```

Ou se for criar um novo banco do zero, execute:

```sql
-- Execute o arquivo: backend/src/models/scripts.sql
```

### Passo 2: Iniciar o Backend

```bash
cd backend
# Ative seu ambiente virtual se estiver usando
python -m uvicorn src.main:app --reload --port 3000
```

### Passo 3: Iniciar o Frontend

```bash
cd frontend-react
npm install  # Se ainda não instalou as dependências
npm run dev
```

### Passo 4: Acessar o Sistema

1. Acesse `http://localhost:5173` (ou a porta que o Vite indicar)
2. Faça login com:
   - **Username:** admin
   - **Senha:** admin123
3. Explore as funcionalidades!

## 📝 Endpoints da API

### Autenticação
- `POST /token` - Login (obter token JWT)

### Usuários (requer autenticação admin)
- `GET /users/` - Listar todos os usuários
- `POST /users/` - Criar novo usuário
- `PUT /users/{user_id}` - Atualizar usuário
- `DELETE /users/{user_id}` - Deletar usuário
- `GET /users/me/` - Obter dados do usuário logado

### Tarefas
- `GET /tasks/` - Listar todas as tarefas (todos os perfis)
- `POST /tasks/` - Criar tarefa (admin e gerencial)
- `PUT /tasks/{task_id}` - Atualizar tarefa (admin e gerencial)
- `DELETE /tasks/{task_id}` - Deletar tarefa (apenas admin)

## 🎨 Interface

### Tela de Login
- Formulário simples com username e senha
- Mensagens de erro quando credenciais estão incorretas

### Board Kanban
- Layout responsivo (4 colunas em desktop, empilhadas em mobile)
- Cards arrastáveis
- Contador de tarefas por coluna
- Ações rápidas em cada card

### Gerenciador de Usuários
- Tabela com todos os usuários
- Formulário para criar/editar
- Badges coloridos para identificar perfis
- Botões de ação rápida

## 🔧 Tecnologias Utilizadas

### Backend
- FastAPI
- PostgreSQL
- JWT para autenticação
- bcrypt para hash de senhas

### Frontend
- React 18
- Tailwind CSS
- HTML5 Drag and Drop API
- Fetch API para requisições HTTP

## 📌 Notas Importantes

1. **Autenticação**: Todas as rotas (exceto `/token`) requerem autenticação via token JWT
2. **Permissões**: O sistema verifica o perfil do usuário antes de permitir ações
3. **Status das Tarefas**: Os valores aceitos são: `pendente`, `em_andamento`, `em_revisao`, `concluida`
4. **Senhas**: Ao editar um usuário, a senha só será alterada se for preenchida no formulário

## 🐛 Solução de Problemas

### Erro ao fazer login
- Verifique se o backend está rodando
- Confirme se o usuário existe no banco de dados
- Verifique as credenciais

### Tarefas não aparecem no kanban
- Verifique se está autenticado
- Confirme se o status das tarefas está usando os valores corretos
- Execute o script de migração se necessário

### Erro 401 (Não autorizado)
- Faça login novamente
- Verifique se o token ainda é válido
- Confirme se tem permissão para a ação (perfil correto)

## 📚 Próximos Passos (Melhorias Futuras)

- [ ] Filtros e busca de tarefas
- [ ] Atribuição de tarefas a usuários
- [ ] Comentários em tarefas
- [ ] Histórico de alterações
- [ ] Notificações
- [ ] Exportação de relatórios
