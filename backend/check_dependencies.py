"""
Script para verificar se todas as dependências estão instaladas antes de executar os testes.
"""
import sys

REQUIRED_PACKAGES = [
    ('pytest', 'pytest'),
    ('pytest_asyncio', 'pytest-asyncio'),
    ('pytest_cov', 'pytest-cov'),
    ('httpx', 'httpx'),
    ('pytest_mock', 'pytest-mock'),
    ('fastapi', 'fastapi'),
    ('pydantic', 'pydantic'),
    ('email_validator', 'email-validator'),  # Importante para schemas com EmailStr
    ('psycopg2', 'psycopg2-binary'),
    ('bcrypt', 'bcrypt'),
    ('jose', 'python-jose'),
    ('passlib', 'passlib'),
    ('yaml', 'PyYAML'),
]

missing_packages = []

for import_name, package_name in REQUIRED_PACKAGES:
    try:
        __import__(import_name)
    except ImportError:
        missing_packages.append(package_name)

if missing_packages:
    print("ERRO: Dependencias faltando:")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    print("\nPara instalar todas as dependencias, execute:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
else:
    print("OK: Todas as dependencias estao instaladas!")
    sys.exit(0)

