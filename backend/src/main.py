"""
API Principal - FastAPI Application
Aplicação refatorada usando Design Patterns:
- Repository Pattern: abstração de acesso a dados
- Service Layer Pattern: lógica de negócio separada
- Dependency Injection: injeção de dependências via FastAPI Depends
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager

# Imports de inicialização
from src.models.init_db import init_database

# Imports de autenticação
from src.models import auth
from src.config import schemas

# Imports de serviços (Service Layer)
from src.services import UserService, TaskService, AuthService
from src.services.notification_service import NotificationService
from src.dependencies import get_user_service, get_task_service, get_auth_service, get_notification_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler - substitui @app.on_event("startup")
    Inicializa o banco de dados ao iniciar a aplicação.
    """
    # Startup
    try:
        init_database()
    except Exception as e:
        print(f"\nAVISO: Nao foi possivel inicializar o banco de dados automaticamente.")
        print(f"   Erro: {e}")
        print(f"   Certifique-se de que o PostgreSQL esta rodando e as credenciais estao corretas.")
        print(f"   Voce ainda pode executar manualmente: python -m src.models.init_db\n")
    yield
    # Shutdown (se necessário adicionar lógica de limpeza aqui)


app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="Uma API completa com autenticação JWT e controle de acesso por nível.",
    version="2.0.0",
    lifespan=lifespan
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Origens permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# ============================================================================
# ENDPOINTS DE AUTENTICAÇÃO
# ============================================================================

@app.post("/token", response_model=schemas.Token, tags=["Autenticação"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint de autenticação.
    Retorna um token JWT válido para o usuário autenticado.
    """
    return auth_service.authenticate(form_data.username, form_data.password)

# ============================================================================
# ENDPOINTS DE USUÁRIOS
# ============================================================================

@app.get("/users/", response_model=List[schemas.User], tags=["Usuários"])
def read_all_users(
    current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"])),
    user_service: UserService = Depends(get_user_service)
):
    """
    Lista todos os usuários. **Acesso restrito a administradores e gerenciais.**
    - Admin: vê todos os usuários
    - Gerencial: vê apenas usuários até o nível gerencial (não vê admin)
    """
    return user_service.get_all_users(current_user.role)

@app.post("/users/", response_model=schemas.User, tags=["Usuários"], status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: schemas.UserCreate,
    _ = Depends(auth.require_role(["admin"])),
    user_service: UserService = Depends(get_user_service)
):
    """
    Cria um novo usuário. **Acesso restrito a administradores.**
    """
    return user_service.create_user(user)

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Usuários"])
def update_existing_user(
    user_id: int,
    user: schemas.UserUpdate,
    current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"])),
    user_service: UserService = Depends(get_user_service)
):
    """
    Atualiza um usuário existente.
    - Admin: pode editar qualquer usuário
    - Gerencial: pode editar usuários (exceto admin) e não pode alterar role para admin
    """
    return user_service.update_user(user_id, user, current_user.role)

@app.delete("/users/{user_id}", tags=["Usuários"])
def delete_existing_user(
    user_id: int,
    _ = Depends(auth.require_role(["admin"])),
    user_service: UserService = Depends(get_user_service)
):
    """
    Deleta um usuário. **Acesso restrito a administradores.**
    """
    user_service.delete_user(user_id)
    return {"message": "Usuário deletado com sucesso"}

@app.get("/users/me/", response_model=schemas.User, tags=["Usuários"])
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user

# ============================================================================
# ENDPOINTS DE NOTIFICAÇÕES
# ============================================================================

@app.get("/notifications/", tags=["Notificações"])
def get_notifications(
    unread_only: bool = False,
    current_user: schemas.User = Depends(auth.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """
    Retorna notificações do usuário atual.
    - Admin e gerencial recebem notificações de tarefas em revisão
    - Todos os usuários recebem notificações quando suas tarefas são concluídas
    """
    notifications = notification_service.get_user_notifications(current_user.id, unread_only=unread_only)
    return notifications

@app.get("/notifications/unread-count", tags=["Notificações"])
def get_unread_count(
    current_user: schemas.User = Depends(auth.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """Retorna o número de notificações não lidas do usuário atual."""
    count = notification_service.get_unread_count(current_user.id)
    return {"unread_count": count}

@app.put("/notifications/{notification_id}/read", tags=["Notificações"])
def mark_notification_as_read(
    notification_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """Marca uma notificação como lida."""
    success = notification_service.mark_as_read(notification_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    return {"message": "Notificação marcada como lida"}

@app.put("/notifications/read-all", tags=["Notificações"])
def mark_all_notifications_as_read(
    current_user: schemas.User = Depends(auth.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service)
):
    """Marca todas as notificações do usuário como lidas."""
    count = notification_service.mark_all_as_read(current_user.id)
    return {"message": f"{count} notificações marcadas como lidas"}

# ============================================================================
# ENDPOINTS DE TAREFAS
# ============================================================================

@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tarefas"])
def read_all_tasks(
    _ = Depends(auth.require_role(["admin", "gerencial", "visualizacao"])),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Lista todas as tarefas. **Acesso permitido para todos os níveis.**
    """
    return task_service.get_all_tasks()

@app.post("/tasks/", response_model=schemas.Task, tags=["Tarefas"], status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: schemas.TaskCreate,
    current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"])),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Cria uma nova tarefa. **Acesso restrito a administradores e gerentes.**
    Admin e gerencial podem atribuir tarefas a outros usuários através do campo owner_id.
    """
    return task_service.create_task(task, current_user.id)

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tarefas"])
def update_existing_task(
    task_id: int,
    task: schemas.TaskCreate,
    current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial", "visualizacao"])),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Atualiza uma tarefa existente. 
    - Admin e gerencial: podem alterar título, descrição, status e responsável.
    - Visualização: pode alterar apenas o status (mas não pode mudar para "concluida").
    Notifica admin e gerencial quando status muda para "em_revisao" (Observer Pattern).
    """
    # Converter current_user para dict para passar ao Observer
    current_user_dict = {
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role
    }
    return task_service.update_task(task_id, task, current_user.role, current_user_dict)

@app.delete("/tasks/{task_id}", tags=["Tarefas"])
def delete_existing_task(
    task_id: int,
    _ = Depends(auth.require_role(["admin"])),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Deleta uma tarefa. **Acesso restrito a administradores.**
    """
    task_service.delete_task(task_id)
    return {"message": "Tarefa deletada com sucesso"}
