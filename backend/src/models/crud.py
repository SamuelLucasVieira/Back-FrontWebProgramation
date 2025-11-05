# Imports atualizados para a nova estrutura
from src.config.database import get_db_cursor
from src.core.security import get_password_hash 
from datetime import datetime

from psycopg2.extras import DictCursor

# Função auxiliar para converter tuplas em dicionários
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Função auxiliar para serializar datetime para string ISO
def serialize_user(user_dict):
    """Converte campos datetime para string ISO format"""
    if user_dict and 'created_at' in user_dict and user_dict['created_at'] is not None:
        if isinstance(user_dict['created_at'], datetime):
            user_dict['created_at'] = user_dict['created_at'].isoformat()
    return user_dict

# --- CRUD de Usuários ---

def get_user_by_username(username: str):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, username, email, hashed_password, role FROM usuarios WHERE username = %s;", (username,))
        user = cursor.fetchone()
        if user:
            # Converte a tupla em um dicionário
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, user))
        return None

def get_all_users():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, username, email, role, created_at FROM usuarios ORDER BY id;")
        users = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        users_list = [dict(zip(columns, user)) for user in users]
        # Serializar datetime para string em cada usuário
        return [serialize_user(user) for user in users_list]

def get_users_by_max_role(max_role: str):
    """
    Retorna usuários até um nível máximo de role.
    Ordem de hierarquia: admin > gerencial > visualizacao
    """
    # Definir hierarquia de roles
    role_hierarchy = {
        'admin': 3,
        'gerencial': 2,
        'visualizacao': 1
    }
    
    max_level = role_hierarchy.get(max_role, 1)
    
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, username, email, role, created_at FROM usuarios ORDER BY id;")
        users = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        users_list = [dict(zip(columns, user)) for user in users]
        
        # Filtrar usuários baseado na hierarquia
        filtered_users = [
            serialize_user(user) for user in users_list 
            if role_hierarchy.get(user['role'], 0) <= max_level
        ]
        
        return filtered_users

def get_user_by_id(user_id: int):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, username, email, role, created_at FROM usuarios WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
        if user:
            columns = [desc[0] for desc in cursor.description]
            user_dict = dict(zip(columns, user))
            return serialize_user(user_dict)
        return None

def create_user(username: str, email: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO usuarios (username, email, hashed_password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
            (username, email, hashed_password, role)
        )
        user_id = cursor.fetchone()[0]
        return {"id": user_id, "username": username, "email": email, "role": role}

def update_user(user_id: int, username: str = None, email: str = None, role: str = None, password: str = None):
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
    query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s RETURNING id, username, email, role, created_at;"
    
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, values)
        updated = cursor.fetchone()
        if updated:
            columns = [desc[0] for desc in cursor.description]
            user_dict = dict(zip(columns, updated))
            return serialize_user(user_dict)
        return None

def delete_user(user_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s RETURNING id;", (user_id,))
        deleted_id = cursor.fetchone()
        return deleted_id is not None

# --- CRUD de Tarefas ---

def get_tasks():
    with get_db_cursor() as cursor:
        # JOIN com usuarios para trazer o username do responsável
        cursor.execute("""
            SELECT t.id, t.titulo, t.descricao, t.status, t.owner_id, u.username as owner_username
            FROM tarefas t
            LEFT JOIN usuarios u ON t.owner_id = u.id
            ORDER BY t.id;
        """)
        tasks = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, task)) for task in tasks]

def create_task(titulo: str, descricao: str, status: str, owner_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO tarefas (titulo, descricao, status, owner_id) VALUES (%s, %s, %s, %s) RETURNING id;",
            (titulo, descricao, status, owner_id)
        )
        task_id = cursor.fetchone()[0]
        # Buscar o username do owner
        cursor.execute("SELECT username FROM usuarios WHERE id = %s;", (owner_id,))
        owner_result = cursor.fetchone()
        owner_username = owner_result[0] if owner_result else None
        return {"id": task_id, "titulo": titulo, "descricao": descricao, "status": status, "owner_id": owner_id, "owner_username": owner_username}

def update_task(task_id: int, titulo: str = None, descricao: str = None, status: str = None, owner_id: int = None):
    updates = []
    values = []
    
    if titulo is not None:
        updates.append("titulo = %s")
        values.append(titulo)
    if descricao is not None:
        updates.append("descricao = %s")
        values.append(descricao)
    if status is not None:
        updates.append("status = %s")
        values.append(status)
    if owner_id is not None:
        updates.append("owner_id = %s")
        values.append(owner_id)
    
    if not updates:
        return False
    
    values.append(task_id)
    query = f"UPDATE tarefas SET {', '.join(updates)} WHERE id = %s RETURNING id;"
    
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, values)
        updated_id = cursor.fetchone()
        return updated_id is not None

def delete_task(task_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM tarefas WHERE id = %s RETURNING id;", (task_id,))
        deleted_id = cursor.fetchone()
        return deleted_id is not None