"""
Repositório de Usuários - Repository Pattern
Responsável por todas as operações de acesso a dados relacionadas a usuários.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.repositories.base_repository import BaseRepository
from src.core.security import get_password_hash


class UserRepository(BaseRepository):
    """Repositório para operações CRUD de usuários."""
    
    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário pelo username."""
        query = """
            SELECT id, username, email, hashed_password, role, created_at 
            FROM usuarios 
            WHERE username = %s;
        """
        def process_result(cursor):
            row = cursor.fetchone()
            if row:
                user = self._row_to_dict(cursor, row)
                return self._serialize_user(user)
            return None
        return self._execute_with_cursor(query, (username,))(process_result)
    
    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca um usuário pelo ID."""
        query = """
            SELECT id, username, email, role, created_at 
            FROM usuarios 
            WHERE id = %s;
        """
        def process_result(cursor):
            row = cursor.fetchone()
            if row:
                user = self._row_to_dict(cursor, row)
                return self._serialize_user(user)
            return None
        return self._execute_with_cursor(query, (user_id,))(process_result)
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Retorna todos os usuários."""
        query = """
            SELECT id, username, email, role, created_at 
            FROM usuarios 
            ORDER BY id;
        """
        def process_result(cursor):
            rows = cursor.fetchall()
            users = self._rows_to_dicts(cursor, rows)
            return [self._serialize_user(user) for user in users]
        return self._execute_with_cursor(query)(process_result)
    
    def find_by_max_role(self, max_role: str) -> List[Dict[str, Any]]:
        """
        Retorna usuários até um nível máximo de role.
        Ordem de hierarquia: admin > gerencial > visualizacao
        """
        role_hierarchy = {
            'admin': 3,
            'gerencial': 2,
            'visualizacao': 1
        }
        
        max_level = role_hierarchy.get(max_role, 1)
        all_users = self.find_all()
        
        # Filtrar usuários baseado na hierarquia
        filtered_users = [
            user for user in all_users 
            if role_hierarchy.get(user['role'], 0) <= max_level
        ]
        
        return filtered_users
    
    def create(self, username: str, email: str, password: str, role: str) -> Dict[str, Any]:
        """Cria um novo usuário."""
        hashed_password = get_password_hash(password)
        query = """
            INSERT INTO usuarios (username, email, hashed_password, role) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id;
        """
        def process_result(cursor):
            user_id = cursor.fetchone()[0]
            return {
                "id": user_id,
                "username": username,
                "email": email,
                "role": role
            }
        return self._execute_with_cursor(query, (username, email, hashed_password, role), commit=True)(process_result)
    
    def update(
        self, 
        user_id: int, 
        username: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        password: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Atualiza um usuário existente."""
        updates = []
        values = []
        
        if username is not None:
            updates.append("username = %s")
            values.append(username)
        if email is not None:
            updates.append("email = %s")
            values.append(email)
        if role is not None:
            updates.append("role = %s")
            values.append(role)
        if password is not None:
            hashed_password = get_password_hash(password)
            updates.append("hashed_password = %s")
            values.append(hashed_password)
        
        if not updates:
            return None
        
        values.append(user_id)
        query = f"""
            UPDATE usuarios 
            SET {', '.join(updates)} 
            WHERE id = %s 
            RETURNING id, username, email, role, created_at;
        """
        
        def process_result(cursor):
            row = cursor.fetchone()
            if row:
                user = self._row_to_dict(cursor, row)
                return self._serialize_user(user)
            return None
        return self._execute_with_cursor(query, tuple(values), commit=True)(process_result)
    
    def delete(self, user_id: int) -> bool:
        """Deleta um usuário."""
        query = "DELETE FROM usuarios WHERE id = %s RETURNING id;"
        def process_result(cursor):
            deleted_id = cursor.fetchone()
            return deleted_id is not None
        return self._execute_with_cursor(query, (user_id,), commit=True)(process_result)
    
    def exists_by_username(self, username: str) -> bool:
        """Verifica se um username já existe."""
        return self.find_by_username(username) is not None
    
    @staticmethod
    def _serialize_user(user: Dict[str, Any]) -> Dict[str, Any]:
        """Converte campos datetime para string ISO format."""
        if user and 'created_at' in user and user['created_at'] is not None:
            if isinstance(user['created_at'], datetime):
                user['created_at'] = user['created_at'].isoformat()
        return user

