"""
Script auxiliar para inicializar o banco de dados manualmente.
Execute este script se precisar criar as tabelas sem iniciar o servidor FastAPI.

Uso:
    python init_database.py
"""
import sys
from pathlib import Path

# Adiciona o diretório src ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent))

from src.models.init_db import init_database

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Inicialização Manual do Banco de Dados")
    print("="*60)
    print("\nEste script criará:")
    print("  - Tipos ENUM (user_role, task_status)")
    print("  - Tabelas (usuarios, tarefas)")
    print("  - Índices")
    print("  - Usuário admin padrão (se não existir)")
    print("\n" + "="*60 + "\n")
    
    try:
        init_database()
        print("\n✅ Inicialização concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante a inicialização: {e}")
        sys.exit(1)

