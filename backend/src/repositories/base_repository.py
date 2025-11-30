"""
Classe base abstrata para repositórios.
Define a interface comum que todos os repositórios devem seguir.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Callable
from src.config.database import get_db_cursor


class BaseRepository(ABC):
    """
    Classe base abstrata para repositórios.
    Fornece métodos utilitários comuns e define a interface básica.
    """
    
    @staticmethod
    def _row_to_dict(cursor, row) -> Optional[Dict[str, Any]]:
        """Converte uma tupla de resultado em um dicionário."""
        if not row:
            return None
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    
    @staticmethod
    def _rows_to_dicts(cursor, rows) -> List[Dict[str, Any]]:
        """Converte múltiplas tuplas de resultado em uma lista de dicionários."""
        if not rows:
            return []
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    @staticmethod
    def _execute_query(query: str, params: tuple = None, commit: bool = False) -> Any:
        """
        Executa uma query e retorna o cursor para processamento.
        ATENÇÃO: Este método mantém o cursor aberto dentro do context manager.
        Use _execute_with_cursor para operações que precisam processar resultados.
        """
        with get_db_cursor(commit=commit) as cursor:
            cursor.execute(query, params or ())
            return cursor
    
    @staticmethod
    def _execute_with_cursor(query: str, params: tuple = None, commit: bool = False) -> Callable:
        """
        Executa uma query e retorna uma função que processa o resultado dentro do context manager.
        Isso garante que o cursor permaneça aberto durante o processamento.
        
        Uso:
            result = _execute_with_cursor(query, params, commit)(lambda cursor: cursor.fetchone())
        """
        def process_result(processor: Callable) -> Any:
            with get_db_cursor(commit=commit) as cursor:
                cursor.execute(query, params or ())
                return processor(cursor)
        return process_result

