from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List

# ... other imports like fastapi, timedelta, etc.

from src.models import crud
from src.config import schemas
from src.core.security import verify_password  # <== IMPORT a função do novo local

# REMOVA as linhas de código de 'pwd_context', 'get_password_hash', 
# e 'verify_password' deste arquivo.

# ... o resto do seu código em auth.py permanece o mesmo
# Exemplo de uso:
# --- Configurações de Segurança ---
SECRET_KEY = "c8a3a08d2a6a6e3a5f9b4b0e6e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Funções de Senha e Token ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependências de Autenticação e Autorização ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
        
    # Retorna o usuário com seu papel (role)
    user_with_role = schemas.User(
        id=user['id'], 
        username=user['username'], 
        email=user['email'], 
        role=user['role']
    )
    return user_with_role

def require_role(required_roles: List[str]):
    """
    Função de dependência que verifica se o usuário atual tem um dos papéis necessários.
    """
    async def role_checker(current_user: schemas.User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer um dos seguintes papéis: {', '.join(required_roles)}",
            )
        return current_user
    return role_checker