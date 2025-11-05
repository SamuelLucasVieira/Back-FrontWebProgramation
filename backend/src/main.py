from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
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

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Origens permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# --- Endpoint de Autenticação ---

@app.post("/token", response_model=schemas.Token, tags=["Autenticação"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user['username'], "role": user['role']},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoints do  crud de Usuários (Protegidos por Nível de Acesso) ---

@app.get("/users/", response_model=List[schemas.User], tags=["Usuários"])
def read_all_users(current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"]))):
    """
    Lista todos os usuários. **Acesso restrito a administradores e gerenciais.**
    - Admin: vê todos os usuários
    - Gerencial: vê apenas usuários até o nível gerencial (não vê admin)
    """
    if current_user.role == "admin":
        return crud.get_all_users()
    else:
        # Gerencial: filtrar para não mostrar admins
        return crud.get_users_by_max_role("gerencial")

@app.post("/users/", response_model=schemas.User, tags=["Usuários"], status_code=status.HTTP_201_CREATED)
def create_new_user(user: schemas.UserCreate, _ = Depends(auth.require_role(["admin"]))):
    """
    Cria um novo usuário. **Acesso restrito a administradores.**
    """
    db_user = crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username já registrado")
    return crud.create_user(username=user.username, email=user.email, password=user.password, role=user.role)

@app.put("/users/{user_id}", response_model=schemas.User, tags=["Usuários"])
def update_existing_user(user_id: int, user: schemas.UserUpdate, current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"]))):
    """
    Atualiza um usuário existente.
    - Admin: pode editar qualquer usuário
    - Gerencial: pode editar usuários (exceto admin) e não pode alterar role para admin
    """
    db_user = crud.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Gerencial não pode editar admin
    if current_user.role == "gerencial" and db_user['role'] == "admin":
        raise HTTPException(status_code=403, detail="Gerenciais não podem editar administradores")
    
    # Gerencial não pode alterar role para admin
    if current_user.role == "gerencial" and user.role == "admin":
        raise HTTPException(status_code=403, detail="Gerenciais não podem alterar role para admin")
    
    # Se username está sendo alterado, verificar se não está em uso
    if user.username and user.username != db_user['username']:
        existing_user = crud.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username já está em uso")
    
    updated_user = crud.update_user(
        user_id=user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        password=user.password
    )
    
    if not updated_user:
        raise HTTPException(status_code=400, detail="Nenhum campo foi atualizado")
    
    return updated_user

@app.delete("/users/{user_id}", tags=["Usuários"])
def delete_existing_user(user_id: int, _ = Depends(auth.require_role(["admin"]))):
    """
    Deleta um usuário. **Acesso restrito a administradores.**
    """
    success = crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}


# --- Endpoints do  crud de Tarefas (Protegidos por Nível de Acesso) ---

@app.get("/tasks/", response_model=List[schemas.Task], tags=["Tarefas"])
def read_all_tasks(_ = Depends(auth.require_role(["admin", "gerencial", "visualizacao"]))):
    """
    Lista todas as tarefas. **Acesso permitido para todos os níveis.**
    """
    return crud.get_tasks()

@app.post("/tasks/", response_model=schemas.Task, tags=["Tarefas"], status_code=status.HTTP_201_CREATED)
def create_new_task(task: schemas.TaskCreate, current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial"]))):
    """
    Cria uma nova tarefa. **Acesso restrito a administradores e gerentes.**
    Admin e gerencial podem atribuir tarefas a outros usuários através do campo owner_id.
    """
    # Se owner_id foi fornecido, usar ele; senão, usar o id do usuário atual
    owner_id = task.owner_id if task.owner_id is not None else current_user.id
    
    # Verificar se o usuário destino existe (se foi fornecido um owner_id)
    if task.owner_id is not None and task.owner_id != current_user.id:
        target_user = crud.get_user_by_id(task.owner_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="Usuário destino não encontrado")
    
    return crud.create_task(titulo=task.titulo, descricao=task.descricao, status=task.status, owner_id=owner_id)

@app.put("/tasks/{task_id}", response_model=schemas.Task, tags=["Tarefas"])
def update_existing_task(task_id: int, task: schemas.TaskCreate, current_user: schemas.User = Depends(auth.require_role(["admin", "gerencial", "visualizacao"]))):
    """
    Atualiza uma tarefa existente. 
    - Admin e gerencial: podem alterar título, descrição, status e responsável.
    - Visualização: pode alterar apenas o status (mas não pode mudar para "concluida").
    """
    # Verificar se a tarefa existe
    tasks = crud.get_tasks()
    current_task = next((t for t in tasks if t['id'] == task_id), None)
    if not current_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Restrições para usuário com role "visualizacao"
    if current_user.role == "visualizacao":
        # Visualização não pode alterar título, descrição ou owner_id
        if task.status and task.status == "concluida":
            raise HTTPException(status_code=403, detail="Usuários com perfil visualização não podem concluir tarefas")
        # Apenas atualizar status, ignorar outros campos
        success = crud.update_task(task_id, None, None, task.status, None)
        if not success:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        # Admin e gerencial podem alterar tudo
        # Se owner_id foi fornecido, verificar se o usuário destino existe
        owner_id = None
        if task.owner_id is not None:
            target_user = crud.get_user_by_id(task.owner_id)
            if not target_user:
                raise HTTPException(status_code=404, detail="Usuário destino não encontrado")
            owner_id = task.owner_id
        
        success = crud.update_task(task_id, task.titulo, task.descricao, task.status, owner_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Retornar a tarefa atualizada
    updated_tasks = crud.get_tasks()
    updated_task = next((t for t in updated_tasks if t['id'] == task_id), None)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Erro ao buscar tarefa atualizada")
    
    return updated_task

@app.delete("/tasks/{task_id}", tags=["Tarefas"])
def delete_existing_task(task_id: int, _ = Depends(auth.require_role(["admin"]))):
    """
    Deleta uma tarefa. **Acesso restrito a administradores.**
    """
    success = crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}

# Rota para verificar o usuário logado
@app.get("/users/me/", response_model=schemas.User, tags=["Usuários"])
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user