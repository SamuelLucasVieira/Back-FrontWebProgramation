# 🔐 Credenciais de Usuários Padrão

Este documento lista as credenciais dos usuários padrão criados automaticamente pelo sistema.

## 👥 Usuários Padrão

O sistema cria automaticamente **3 usuários padrão** quando o banco de dados é inicializado:

### 1. 👑 Administrador (Admin)

- **Username:** `admin`
- **Senha:** `admin123`
- **Email:** `admin@example.com`
- **Role:** `admin`
- **Permissões:**
  - ✅ Acesso total ao sistema
  - ✅ Criar/editar/deletar usuários
  - ✅ Criar/editar/deletar tarefas
  - ✅ Atribuir tarefas a qualquer usuário

### 2. 📊 Gerencial (Gestão)

- **Username:** `gerencial`
- **Senha:** `gerencial123`
- **Email:** `gerencial@example.com`
- **Role:** `gerencial`
- **Permissões:**
  - ✅ Criar/editar tarefas
  - ✅ Ver usuários (exceto admins)
  - ✅ Editar usuários (exceto admins)
  - ❌ Não pode deletar usuários
  - ❌ Não pode deletar tarefas
  - ❌ Não pode criar usuários

### 3. 👁️ Usuário (Visualização)

- **Username:** `usuario`
- **Senha:** `usuario123`
- **Email:** `usuario@example.com`
- **Role:** `visualizacao`
- **Permissões:**
  - ✅ Visualizar tarefas
  - ✅ Alterar status de tarefas (exceto para "concluida")
  - ❌ Não pode criar tarefas
  - ❌ Não pode editar título/descrição
  - ❌ Não pode deletar tarefas
  - ❌ Não pode acessar gerenciamento de usuários

## 🚀 Como Usar

### Login no Sistema

1. Acesse `http://localhost:5173` (frontend)
2. Use uma das credenciais acima
3. O sistema redirecionará para a interface apropriada baseada no perfil

### Testando no Swagger

1. Acesse `http://localhost:3000/docs`
2. Clique em **"Authorize"**
3. Faça login primeiro em `/token` com as credenciais
4. Cole o token JWT retornado no campo de autorização
5. Agora você pode testar os endpoints protegidos

## ⚠️ Importante

- **Em produção**, altere essas senhas padrão imediatamente!
- Essas credenciais são apenas para desenvolvimento/teste
- Use senhas fortes em ambiente de produção

## 📝 Criar Novos Usuários

Você pode criar novos usuários através da interface do sistema (se for admin) ou usando a API:

```bash
POST /users/
Authorization: Bearer <token_admin>
{
  "username": "novo_usuario",
  "email": "novo@example.com",
  "password": "senha_segura",
  "role": "visualizacao"
}
```

