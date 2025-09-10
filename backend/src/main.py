from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# --- Configurações de Segurança ---
# Em um ambiente de produção, use segredos mais fortes e gerencie-os adequadamente.
SECRET_KEY = "c8a3a08d2a6a6e3a5f9b4b0e6e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90" # Troque por uma chave forte e aleatória
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Caminho do arquivo de persistência
DB_FILE = "tasks.json"

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para obter o token via header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------
# Modelo de dados (Pydantic)
# -------------------------

class Task(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = ""
    status: str = Field(default="pendente", pattern="^(pendente|concluída)$")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

# -------------------------
# Simulação de Banco de Dados de Usuários
# -------------------------

# Em um cenário real, isso viria de um banco de dados professor.
# Senha para "admin" é "senha123"
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("senha123"),
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# -------------------------
# Funções de Autenticação
# -------------------------

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# -------------------------
# Funções utilitárias JSON (Tarefas)
# -------------------------

def load_tasks() -> List[Task]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [Task(**item) for item in data]
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: List[Task]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([t.dict() for t in tasks], f, ensure_ascii=False, indent=2)

# -------------------------
# Inicialização do FastAPI
# -------------------------

app = FastAPI(
    title="API de Tarefas Segura",
    description="CRUD de tarefas com autenticação baseada em token JWT.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Rotas
# -------------------------

@app.post("/token", response_model=Token, summary="Autenticar e obter token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", summary="Home")
def home():
    return {"message": "API de Tarefas Online"}

# Todas as rotas abaixo agora exigem autenticação
@app.get("/tarefas", response_model=List[Task], summary="Listar tarefas (protegido)")
def listar_tarefas(current_user: User = Depends(get_current_user)):
    return load_tasks()

@app.post("/tarefas", response_model=Task, summary="Criar tarefa (protegido)")
def criar_tarefa(tarefa: Task, current_user: User = Depends(get_current_user)):
    tarefas = load_tasks()
    if any(t.id == tarefa.id for t in tarefas):
        raise HTTPException(status_code=400, detail="ID já existe.")
    tarefas.append(tarefa)
    save_tasks(tarefas)
    return tarefa

@app.put("/tarefas/{id}", response_model=Task, summary="Atualizar tarefa (protegido)")
def atualizar_tarefa(id: int, tarefa: Task, current_user: User = Depends(get_current_user)):
    tarefas = load_tasks()
    for idx, t in enumerate(tarefas):
        if t.id == id:
            tarefas[idx] = tarefa
            save_tasks(tarefas)
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete("/tarefas/{id}", summary="Excluir tarefa (protegido)")
def excluir_tarefa(id: int, current_user: User = Depends(get_current_user)):
    tarefas = load_tasks()
    tarefas_novas = [t for t in tarefas if t.id != id]
    if len(tarefas_novas) == len(tarefas):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    save_tasks(tarefas_novas)
    return {"detail": "Tarefa excluída com sucesso."}

# -------------------------
# Execução (modo script)
# -------------------------

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 3000))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=reload) # Supondo que o arquivo se chame main.py