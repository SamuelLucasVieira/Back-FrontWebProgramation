from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- Esquemas de Tarefa ---
class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: str = "pendente"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# --- Esquemas de Usuário ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "visualizacao" # Papel padrão ao criar

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

# --- Esquemas de Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None