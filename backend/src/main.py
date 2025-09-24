from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

# Imports atualizados para a nova estrutura
from src.models import auth, crud
from src.config import schemas

app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description="Uma API completa com autenticação JWT e controle de acesso por nível.",
    version="1.0.0"
)

# --- Endpoint de Autenticação ---

@app.post("/token", response_model=schemas.Token, tags=["Autenticação"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user =  crud.get_user_by_username(form_data.username)
    if not user or not  auth.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes= auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  auth.create_access_token(
        data={"sub": user['username'], "role": user['role']},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoints do  crud de Usuários (Protegidos por Nível de Acesso) ---

@app.post("/users/", response_model= schemas.User, tags=["Usuários"], status_code=status.HTTP_201_CREATED)
def create_new_user(user:  schemas.UserCreate, _ = Depends( auth.require_role(["admin"]))):
    """
    Cria um novo usuário. **Acesso restrito a administradores.**
    """
    db_user =  crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username já registrado")
    return  crud.create_user(username=user.username, email=user.email, password=user.password, role=user.role)

@app.delete("/users/{user_id}", tags=["Usuários"])
def delete_existing_user(user_id: int, _ = Depends( auth.require_role(["admin"]))):
    """
    Deleta um usuário. **Acesso restrito a administradores.**
    """
    success =  crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}


# --- Endpoints do  crud de Tarefas (Protegidos por Nível de Acesso) ---

@app.get("/tasks/", response_model=List[ schemas.Task], tags=["Tarefas"])
def read_all_tasks(_ = Depends( auth.require_role(["admin", "gerencial", "visualizacao"]))):
    """
    Lista todas as tarefas. **Acesso permitido para todos os níveis.**
    """
    return  crud.get_tasks()

@app.post("/tasks/", response_model= schemas.Task, tags=["Tarefas"], status_code=status.HTTP_201_CREATED)
def create_new_task(task:  schemas.TaskCreate, current_user:  schemas.User = Depends( auth.require_role(["admin", "gerencial"]))):
    """
    Cria uma nova tarefa. **Acesso restrito a administradores e gerentes.**
    """
    return  crud.create_task(titulo=task.titulo, descricao=task.descricao, status=task.status, owner_id=current_user.id)

@app.put("/tasks/{task_id}", tags=["Tarefas"])
def update_existing_task(task_id: int, task:  schemas.TaskCreate, _ = Depends( auth.require_role(["admin", "gerencial"]))):
    """
    Atualiza uma tarefa existente. **Acesso restrito a administradores e gerentes.**
    """
    success =  crud.update_task(task_id, task.titulo, task.descricao, task.status)
    if not success:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa atualizada com sucesso"}

@app.delete("/tasks/{task_id}", tags=["Tarefas"])
def delete_existing_task(task_id: int, _ = Depends( auth.require_role(["admin"]))):
    """
    Deleta uma tarefa. **Acesso restrito a administradores.**
    """
    success =  crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}

# Rota para verificar o usuário logado
@app.get("/users/me/", response_model= schemas.User, tags=["Usuários"])
async def read_users_me(current_user:  schemas.User = Depends( auth.get_current_user)):
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user