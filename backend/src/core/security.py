from passlib.context import CryptContext

# This context is used for creating and verifying password hashes.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Creates a hash from a plain password."""
    return pwd_context.hash(password)