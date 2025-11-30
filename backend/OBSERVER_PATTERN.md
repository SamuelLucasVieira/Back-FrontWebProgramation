# 🔔 Padrão Observer - Sistema de Notificações

## 📋 Visão Geral

O sistema implementa o **Padrão Observer** para notificar automaticamente:
- **Admin e Gerencial**: quando uma tarefa é movida para o status **"em_revisao"**
- **Responsável pela Tarefa**: quando uma tarefa é movida para o status **"concluida"**

## 🎯 Objetivo

O sistema detecta mudanças de status e notifica automaticamente:

### Quando status muda para "em_revisao":
- Detecta a mudança de status
- Notifica todos os usuários com perfil **admin** ou **gerencial**
- Cria notificações que podem ser visualizadas no frontend

### Quando status muda para "concluida":
- Detecta a mudança de status
- Notifica o **responsável pela tarefa** (owner_id)
- Cria notificação que pode ser visualizada no frontend

## 🏗️ Estrutura do Padrão Observer

### 1. **Subject (Assunto Observado)**
- **Classe:** `TaskSubject` (`backend/src/patterns/observer.py`)
- **Responsabilidade:** Representa uma tarefa que pode ser observada
- **Métodos:**
  - `attach(observer)`: Adiciona um observador
  - `detach(observer)`: Remove um observador
  - `notify(event_data)`: Notifica todos os observadores
  - `update_task()`: Atualiza a tarefa e dispara notificações

### 2. **Observer (Observador)**
- **Interface:** `Observer` (abstrata)
- **Implementação:** `TaskNotificationObserver`
- **Responsabilidade:** Observa mudanças na tarefa e cria notificações quando necessário
  - Quando status muda para "em_revisao": notifica admin e gerencial
  - Quando status muda para "concluida": notifica o responsável pela tarefa
- **Método:**
  - `update(subject, event_data)`: Chamado quando o subject notifica

### 3. **NotificationService**
- **Classe:** `NotificationService` (`backend/src/services/notification_service.py`)
- **Responsabilidade:** Gerencia o armazenamento e recuperação de notificações
- **Funcionalidades:**
  - `create_review_notification()`: Cria notificações para admin e gerencial quando tarefa vai para revisão
  - `create_completion_notification()`: Cria notificação para o responsável quando tarefa é concluída
  - Armazena notificações em memória (singleton)
  - Fornece métodos para buscar e marcar notificações como lidas

## 🔄 Fluxo de Funcionamento

### Fluxo para "em_revisao":
```
1. Usuário atualiza tarefa para status "em_revisao"
   ↓
2. TaskService.update_task() detecta mudança
   ↓
3. TaskService._notify_if_review() é chamado
   ↓
4. TaskSubject é criado com a tarefa
   ↓
5. TaskNotificationObserver é anexado ao Subject
   ↓
6. Subject.notify() dispara notificação
   ↓
7. Observer.update() detecta mudança para "em_revisao"
   ↓
8. NotificationService.create_review_notification() cria notificações
   ↓
9. Notificações são criadas para todos admin e gerencial
   ↓
10. Notificações ficam disponíveis via API
   ↓
11. Frontend busca e exibe notificações
```

### Fluxo para "concluida":
```
1. Usuário atualiza tarefa para status "concluida"
   ↓
2. TaskService.update_task() detecta mudança
   ↓
3. TaskService._notify_if_review() é chamado
   ↓
4. TaskSubject é criado com a tarefa
   ↓
5. TaskNotificationObserver é anexado ao Subject
   ↓
6. Subject.notify() dispara notificação
   ↓
7. Observer.update() detecta mudança para "concluida"
   ↓
8. NotificationService.create_completion_notification() cria notificação
   ↓
9. Notificação é criada para o responsável pela tarefa (owner_id)
   ↓
10. Notificação fica disponível via API
   ↓
11. Frontend busca e exibe notificação
```

## 📁 Arquivos Envolvidos

### Backend
- `backend/src/patterns/observer.py` - Implementação do padrão Observer
- `backend/src/services/notification_service.py` - Serviço de notificações
- `backend/src/services/task_service.py` - Integração do Observer
- `backend/src/main.py` - Endpoints de notificações

### Frontend
- `frontend-react/src/components/NotificationBell.jsx` - Componente de notificações
- `frontend-react/src/App.jsx` - Integração do componente

## 🔌 Endpoints da API

### GET `/notifications/`
- **Descrição:** Lista notificações do usuário atual
- **Acesso:** Todos os usuários autenticados
- **Parâmetros:**
  - `unread_only` (query, opcional): Se `true`, retorna apenas não lidas
- **Notas:**
  - Admin e Gerencial recebem notificações de tarefas em revisão
  - Todos os usuários recebem notificações quando suas tarefas são concluídas

### GET `/notifications/unread-count`
- **Descrição:** Retorna o número de notificações não lidas
- **Acesso:** Todos os usuários autenticados

### PUT `/notifications/{notification_id}/read`
- **Descrição:** Marca uma notificação como lida
- **Acesso:** Todos os usuários autenticados

### PUT `/notifications/read-all`
- **Descrição:** Marca todas as notificações como lidas
- **Acesso:** Todos os usuários autenticados

## 💡 Exemplo de Uso

### Backend (Automático)
Quando uma tarefa é atualizada:

```python
# No TaskService.update_task()
if new_status == 'em_revisao' and old_status != 'em_revisao':
    # Criar Subject
    task_subject = TaskSubject(task)
    
    # Anexar Observer
    task_subject.attach(notification_observer)
    
    # Notificar (dispara criação de notificações)
    task_subject.update_task(task, old_status, current_user)
```

### Frontend
O componente `NotificationBell` automaticamente:
- Busca notificações a cada 30 segundos
- Exibe contador de não lidas
- Permite marcar como lidas
- Mostra lista de notificações ao clicar

## 🎨 Interface do Usuário

- **Ícone de sino** no header (apenas para admin/gerencial)
- **Badge vermelho** com contador de não lidas
- **Painel dropdown** com lista de notificações
- **Notificações não lidas** destacadas em azul claro
- **Botão "Marcar todas como lidas"**

## 🔒 Segurança

- **Notificações de revisão**: Apenas usuários com perfil **admin** ou **gerencial** recebem
- **Notificações de conclusão**: Apenas o responsável pela tarefa (owner_id) recebe
- Apenas usuários autenticados podem acessar endpoints de notificações
- Cada usuário só vê suas próprias notificações

## 🚀 Melhorias Futuras

1. **Persistência:** Migrar notificações de memória para banco de dados
2. **Notificações em tempo real:** Usar WebSockets para notificações instantâneas
3. **Tipos de notificação:** Expandir para outros eventos (tarefa criada, concluída, etc.)
4. **Preferências:** Permitir usuários configurarem quais notificações receber
5. **Email/SMS:** Enviar notificações por email ou SMS

## 📚 Referências

- **Padrão Observer:** Design Pattern para notificações de mudanças
- **Separation of Concerns:** Observer separado da lógica de negócio
- **Dependency Injection:** Observer injetado no TaskService

