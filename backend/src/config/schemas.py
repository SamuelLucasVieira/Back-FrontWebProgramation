from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# --- Esquemas de Tarefa ---
class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: str = "pendente"

class TaskCreate(TaskBase):
    owner_id: Optional[int] = None  # Opcional: admin/gerencial pode atribuir a outros usuários

class Task(TaskBase):
    id: int
    owner_id: int
    owner_username: Optional[str] = None  # Nome do usuário responsável
    status: str
    created_at: Optional[str] = None  # Data de criação da tarefa

    model_config = ConfigDict(from_attributes=True)

# --- Esquemas de Usuário ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "visualizacao" # Papel padrão ao criar

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    role: str
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- Esquemas de Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None