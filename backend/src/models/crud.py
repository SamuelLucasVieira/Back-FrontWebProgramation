# Imports atualizados para a nova estrutura
from src.config.database import get_db_cursor
from src.models.auth import get_password_hash

from psycopg2.extras import DictCursor

# Função auxiliar para converter tuplas em dicionários
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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

def create_user(username: str, email: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO usuarios (username, email, hashed_password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
            (username, email, hashed_password, role)
        )
        user_id = cursor.fetchone()[0]
        return {"id": user_id, "username": username, "email": email, "role": role}

def delete_user(user_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s RETURNING id;", (user_id,))
        deleted_id = cursor.fetchone()
        return deleted_id is not None

# --- CRUD de Tarefas ---

def get_tasks():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, titulo, descricao, status, owner_id FROM tarefas;")
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
        return {"id": task_id, "titulo": titulo, "descricao": descricao, "status": status, "owner_id": owner_id}

def update_task(task_id: int, titulo: str, descricao: str, status: str):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "UPDATE tarefas SET titulo = %s, descricao = %s, status = %s WHERE id = %s RETURNING id;",
            (titulo, descricao, status, task_id)
        )
        updated_id = cursor.fetchone()
        return updated_id is not None

def delete_task(task_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM tarefas WHERE id = %s RETURNING id;", (task_id,))
        deleted_id = cursor.fetchone()
        return deleted_id is not None