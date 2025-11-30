"""
Serviço de Autenticação - Service Layer Pattern
Contém a lógica de negócio relacionada a autenticação e autorização.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from datetime import timedelta
from src.repositories.user_repository import UserRepository
from src.models import auth


class AuthService:
    """Serviço para autenticação e autorização."""
    
    def __init__(self, repository: Optional[UserRepository] = None):
        """Inicializa o serviço com um repositório (Dependency Injection)."""
        self.repository = repository or UserRepository()
    
    def authenticate(self, username: str, password: str) -> Dict[str, str]:
        """
        Autentica um usuário e retorna um token JWT.
        Lança exceção se as credenciais forem inválidas.
        """
        # Buscar usuário pelo username
        user = self.repository.find_by_username(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar senha
        if not auth.verify_password(password, user['hashed_password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Criar token JWT
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user['username'], "role": user['role']},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

