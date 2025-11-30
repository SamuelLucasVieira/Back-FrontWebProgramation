"""
Serviço de Usuários - Service Layer Pattern
Contém a lógica de negócio relacionada a usuários.
"""
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from src.repositories.user_repository import UserRepository
from src.config import schemas


class UserService:
    """Serviço para gerenciamento de usuários."""
    
    def __init__(self, repository: Optional[UserRepository] = None):
        """Inicializa o serviço com um repositório (Dependency Injection)."""
        self.repository = repository or UserRepository()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário pelo username."""
        return self.repository.find_by_username(username)
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Busca um usuário pelo ID. Lança exceção se não encontrado."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    
    def get_all_users(self, current_user_role: str) -> List[Dict[str, Any]]:
        """
        Retorna todos os usuários com base no perfil do usuário atual.
        - Admin: vê todos os usuários
        - Gerencial: vê apenas usuários até o nível gerencial
        """
        if current_user_role == "admin":
            return self.repository.find_all()
        else:
            return self.repository.find_by_max_role("gerencial")
    
    def create_user(self, user_data: schemas.UserCreate) -> Dict[str, Any]:
        """
        Cria um novo usuário.
        Valida se o username já existe antes de criar.
        """
        # Validar se username já existe
        if self.repository.exists_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já registrado"
            )
        
        return self.repository.create(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role
        )
    
    def update_user(
        self,
        user_id: int,
        user_data: schemas.UserUpdate,
        current_user_role: str
    ) -> Dict[str, Any]:
        """
        Atualiza um usuário existente.
        Aplica regras de negócio baseadas no perfil do usuário atual.
        """
        # Verificar se o usuário existe
        db_user = self.repository.find_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Regras de negócio: Gerencial não pode editar admin
        if current_user_role == "gerencial" and db_user['role'] == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gerenciais não podem editar administradores"
            )
        
        # Regras de negócio: Gerencial não pode alterar role para admin
        if current_user_role == "gerencial" and user_data.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Gerenciais não podem alterar role para admin"
            )
        
        # Validar se username está sendo alterado e se já está em uso
        if user_data.username and user_data.username != db_user['username']:
            if self.repository.exists_by_username(user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username já está em uso"
                )
        
        # Atualizar usuário
        updated_user = self.repository.update(
            user_id=user_id,
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            password=user_data.password
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo foi atualizado"
            )
        
        return updated_user
    
    def delete_user(self, user_id: int) -> bool:
        """Deleta um usuário."""
        success = self.repository.delete(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return success

