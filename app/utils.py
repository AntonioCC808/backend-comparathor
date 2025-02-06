import logging
import os
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve the currently authenticated user from a JWT token.

    This function decodes the provided JWT token, verifies its validity,
    extracts the user's email, and retrieves the corresponding user from
    the database. If authentication fails at any step, an HTTP 401
    Unauthorized exception is raised.

    Parameters
    ----------
    token : str
        The JWT token provided by the client for authentication.
    db : Session
        SQLAlchemy database session dependency.

    Returns
    -------
    User
        The authenticated user object retrieved from the database.

    Raises
    ------
    HTTPException
        If the authentication credentials are invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token and extract user email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query database for user
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise credentials_exception

    return user



def get_logger(
    name: str, save_log: bool = False, dir_to_save: Path = None
) -> logging.Logger:
    """
    Return commons logger with an INFO level.


    Parameters
    ----------
    name : str
        Name of the logger.
    save_log : bool, optional
        Setting `True`, commons directory to save the logs will be created.
        The default is `False`.
    dir_to_save : str, optional
        Path to create the loggers directory. The default is `None`.

    Returns
    -------
    logging.Logger instance
        A logger instance with commons handler and commons formatter already set.
    """
    formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    )
    logger = logging.getLogger(name)
    logger.setLevel("INFO")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if save_log:
        if not isinstance(dir_to_save, Path):
            raise TypeError(
                "If you wish to save the loggers "
                "you must provide commons path directory"
            )
        if not isinstance(save_log, bool):
            raise TypeError(
                "Save log parameter must be commons boolean value: True or False"
            )
        out_dir = f"{dir_to_save}/loggers"
        out_file = f"{out_dir}/{name}_logs.log"
        if Path(out_file).exists():
            os.remove(out_file)
        os.makedirs(out_dir, exist_ok=True)
        file_handler = logging.FileHandler(out_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
