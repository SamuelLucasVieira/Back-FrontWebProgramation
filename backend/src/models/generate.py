from passlib.context import CryptContext# This context is used for creating and verifying password hashes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Creates a hash from a plain password."""
    return pwd_context.hash(password)

# Coloque a senha que você quer gerar o hash
plain_password = "admin123"

# Gera o hash usando a mesma função da sua API
correct_hash = get_password_hash(plain_password)

print("--- Hash Correto Gerado ---")
print(correct_hash)
print("----------------------------")
print("\nCopie este hash e atualize a coluna 'hashed_password' do usuário no seu banco de dados.")