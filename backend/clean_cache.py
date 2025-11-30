"""
Script para limpar cache do Python antes de executar testes.
"""
import os
import shutil
import sys
from pathlib import Path

def clean_python_cache():
    """Remove todos os arquivos __pycache__ e .pyc."""
    root = Path(__file__).parent
    removed = []
    
    for path in root.rglob('__pycache__'):
        if path.is_dir():
            print(f"Removendo: {path}")
            shutil.rmtree(path)
            removed.append(str(path))
    
    for path in root.rglob('*.pyc'):
        if path.is_file():
            print(f"Removendo: {path}")
            path.unlink()
            removed.append(str(path))
    
    for path in root.rglob('*.pyo'):
        if path.is_file():
            print(f"Removendo: {path}")
            path.unlink()
            removed.append(str(path))
    
    if removed:
        print(f"\nOK: {len(removed)} arquivo(s) de cache removido(s)")
    else:
        print("\nOK: Nenhum arquivo de cache encontrado")
    
    return len(removed)

if __name__ == "__main__":
    print("Limpando cache do Python...")
    print("=" * 50)
    count = clean_python_cache()
    print("=" * 50)
    sys.exit(0 if count >= 0 else 1)

