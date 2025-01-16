from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.

    Parameters
    ----------
    password : str
        The plaintext password to hash.

    Returns
    -------
    str
        The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plaintext password matches its hashed version.

    Parameters
    ----------
    plain_password : str
        The plaintext password to verify.
    hashed_password : str
        The hashed password to compare against.

    Returns
    -------
    bool
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Create a JWT token for authentication.

    Parameters
    ----------
    data : dict
        The data to encode in the token.

    Returns
    -------
    str
        The encoded JWT token.
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
