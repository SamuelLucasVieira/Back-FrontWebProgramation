"""
Script auxiliar para migrar o ENUM task_status.
Execute este script se o ENUM foi criado sem os valores 'em_andamento' e 'em_revisao'.
"""
from src.models.migrate_task_status_enum import migrate_task_status_enum

if __name__ == "__main__":
    migrate_task_status_enum()

