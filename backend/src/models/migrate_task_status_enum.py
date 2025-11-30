"""
Script de migração para atualizar o ENUM task_status.
Adiciona os valores 'em_andamento' e 'em_revisao' se não existirem.
"""
from src.config.database import get_db_cursor


def enum_value_exists(cursor, enum_type: str, enum_value: str) -> bool:
    """Verifica se um valor existe em um tipo ENUM."""
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 
            FROM pg_enum 
            WHERE enumlabel = %s 
            AND enumtypid = (
                SELECT oid 
                FROM pg_type 
                WHERE typname = %s
            )
        );
    """, (enum_value, enum_type))
    return cursor.fetchone()[0]


def migrate_task_status_enum():
    """
    Adiciona os valores 'em_andamento' e 'em_revisao' ao ENUM task_status
    se eles não existirem.
    """
    print("\n" + "="*60)
    print("Migrando ENUM task_status...")
    print("="*60)
    
    try:
        with get_db_cursor(commit=True) as cursor:
            # Verificar se o tipo ENUM existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM pg_type 
                    WHERE typname = 'task_status'
                );
            """)
            enum_exists = cursor.fetchone()[0]
            
            if not enum_exists:
                print("\n[ERRO] O tipo ENUM 'task_status' não existe!")
                print("Execute o script de inicialização primeiro: python -m src.models.init_db")
                return False
            
            print("\n[1/2] Verificando valor 'em_andamento'...")
            if not enum_value_exists(cursor, 'task_status', 'em_andamento'):
                print("   → Adicionando valor 'em_andamento'...")
                cursor.execute("ALTER TYPE task_status ADD VALUE 'em_andamento';")
                print("   ✓ Valor 'em_andamento' adicionado com sucesso!")
            else:
                print("   ✓ Valor 'em_andamento' já existe.")
            
            print("\n[2/2] Verificando valor 'em_revisao'...")
            if not enum_value_exists(cursor, 'task_status', 'em_revisao'):
                print("   → Adicionando valor 'em_revisao'...")
                cursor.execute("ALTER TYPE task_status ADD VALUE 'em_revisao';")
                print("   ✓ Valor 'em_revisao' adicionado com sucesso!")
            else:
                print("   ✓ Valor 'em_revisao' já existe.")
            
            print("\n" + "="*60)
            print("✓ Migração do ENUM task_status concluída com sucesso!")
            print("="*60 + "\n")
            return True
            
    except Exception as e:
        print(f"\n❌ ERRO ao migrar ENUM task_status: {e}")
        print("Verifique se o banco de dados está rodando e se as credenciais estão corretas.")
        raise


if __name__ == "__main__":
    migrate_task_status_enum()

