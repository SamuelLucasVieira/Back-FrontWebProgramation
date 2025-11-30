"""
Repositório de Tarefas - Repository Pattern
Responsável por todas as operações de acesso a dados relacionadas a tarefas.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """Repositório para operações CRUD de tarefas."""
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas com informações do responsável."""
        query = """
            SELECT t.id, t.titulo, t.descricao, t.status, t.owner_id, t.created_at,
                   u.username as owner_username
            FROM tarefas t
            LEFT JOIN usuarios u ON t.owner_id = u.id
            ORDER BY t.id;
        """
        def process_result(cursor):
            rows = cursor.fetchall()
            tasks = self._rows_to_dicts(cursor, rows)
            return [self._serialize_task(task) for task in tasks]
        return self._execute_with_cursor(query)(process_result)
    
    def find_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Busca uma tarefa pelo ID."""
        query = """
            SELECT t.id, t.titulo, t.descricao, t.status, t.owner_id, t.created_at,
                   u.username as owner_username
            FROM tarefas t
            LEFT JOIN usuarios u ON t.owner_id = u.id
            WHERE t.id = %s;
        """
        def process_result(cursor):
            row = cursor.fetchone()
            if row:
                task = self._row_to_dict(cursor, row)
                return self._serialize_task(task)
            return None
        return self._execute_with_cursor(query, (task_id,))(process_result)
    
    def find_by_owner(self, owner_id: int) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas de um usuário específico."""
        query = """
            SELECT t.id, t.titulo, t.descricao, t.status, t.owner_id, t.created_at,
                   u.username as owner_username
            FROM tarefas t
            LEFT JOIN usuarios u ON t.owner_id = u.id
            WHERE t.owner_id = %s
            ORDER BY t.id;
        """
        def process_result(cursor):
            rows = cursor.fetchall()
            tasks = self._rows_to_dicts(cursor, rows)
            return [self._serialize_task(task) for task in tasks]
        return self._execute_with_cursor(query, (owner_id,))(process_result)
    
    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas com um status específico."""
        query = """
            SELECT t.id, t.titulo, t.descricao, t.status, t.owner_id, t.created_at,
                   u.username as owner_username
            FROM tarefas t
            LEFT JOIN usuarios u ON t.owner_id = u.id
            WHERE t.status = %s
            ORDER BY t.id;
        """
        def process_result(cursor):
            rows = cursor.fetchall()
            tasks = self._rows_to_dicts(cursor, rows)
            return [self._serialize_task(task) for task in tasks]
        return self._execute_with_cursor(query, (status,))(process_result)
    
    def create(
        self, 
        titulo: str, 
        descricao: Optional[str], 
        status: str, 
        owner_id: int
    ) -> Dict[str, Any]:
        """Cria uma nova tarefa."""
        # Validar que o status é um valor válido
        valid_statuses = ['pendente', 'em_andamento', 'em_revisao', 'concluida']
        if status not in valid_statuses:
            raise ValueError(f"Status inválido: {status}. Valores válidos: {valid_statuses}")
        
        query = f"""
            INSERT INTO tarefas (titulo, descricao, status, owner_id) 
            VALUES (%s, %s, '{status}'::task_status, %s) 
            RETURNING id;
        """
        def process_result(cursor):
            task_id = cursor.fetchone()[0]
            
            # Buscar o username do owner em uma nova query
            owner_query = "SELECT username FROM usuarios WHERE id = %s;"
            def process_owner(cursor_owner):
                owner_result = cursor_owner.fetchone()
                return owner_result[0] if owner_result else None
            owner_username = self._execute_with_cursor(owner_query, (owner_id,))(process_owner)
            
            return {
                "id": task_id,
                "titulo": titulo,
                "descricao": descricao,
                "status": status,
                "owner_id": owner_id,
                "owner_username": owner_username
            }
        return self._execute_with_cursor(query, (titulo, descricao, owner_id), commit=True)(process_result)
    
    def update(
        self,
        task_id: int,
        titulo: Optional[str] = None,
        descricao: Optional[str] = None,
        status: Optional[str] = None,
        owner_id: Optional[int] = None
    ) -> bool:
        """Atualiza uma tarefa existente."""
        updates = []
        values = []
        
        if titulo is not None:
            updates.append("titulo = %s")
            values.append(titulo)
        if descricao is not None:
            updates.append("descricao = %s")
            values.append(descricao)
        if status is not None:
            # Validar que o status é um valor válido
            valid_statuses = ['pendente', 'em_andamento', 'em_revisao', 'concluida']
            if status not in valid_statuses:
                raise ValueError(f"Status inválido: {status}. Valores válidos: {valid_statuses}")
            # Usar função SQL para fazer o cast corretamente
            # O psycopg2 escapa strings, então precisamos usar uma função SQL
            updates.append(f"status = '{status}'::task_status")
            # Não adicionar status aos values, pois já está na query
        if owner_id is not None:
            updates.append("owner_id = %s")
            values.append(owner_id)
        
        if not updates:
            return False
        
        values.append(task_id)
        # Construir a query com os placeholders corretos
        query = f"""
            UPDATE tarefas 
            SET {', '.join(updates)} 
            WHERE id = %s 
            RETURNING id;
        """
        
        def process_result(cursor):
            updated_id = cursor.fetchone()
            return updated_id is not None
        return self._execute_with_cursor(query, tuple(values), commit=True)(process_result)
    
    def delete(self, task_id: int) -> bool:
        """Deleta uma tarefa."""
        query = "DELETE FROM tarefas WHERE id = %s RETURNING id;"
        def process_result(cursor):
            deleted_id = cursor.fetchone()
            return deleted_id is not None
        return self._execute_with_cursor(query, (task_id,), commit=True)(process_result)
    
    def exists(self, task_id: int) -> bool:
        """Verifica se uma tarefa existe."""
        return self.find_by_id(task_id) is not None
    
    @staticmethod
    def _serialize_task(task: Dict[str, Any]) -> Dict[str, Any]:
        """Converte campos datetime para string ISO format."""
        if task and 'created_at' in task and task['created_at'] is not None:
            if isinstance(task['created_at'], datetime):
                task['created_at'] = task['created_at'].isoformat()
        return task

