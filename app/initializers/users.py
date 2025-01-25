from typing import List
import yaml
from pkg_resources import resource_filename
from app.database import SessionLocal
from app.models.user import User
from app.utils import get_logger, hash_password

logger = get_logger("USERS-INITIALIZER")


def _init_users(users: List[dict]):
    """
    Initialize users in the database.

    Parameters
    ----------
    users : List[dict]
        A list of user data to initialize in the database.

    Returns
    -------
    None
        This function does not return a value.
    """
    logger.info("Initializing users...")

    with SessionLocal() as session:
        # Convert to database models
        init_users = [
            User(
                user_id=user["user_id"],
                email=user["email"],
                password=hash_password(user["password"]),  # Hash the password before storing
                role=user.get("role", "user"),  # Default role is "user"
            )
            for user in users
        ]

        # Add to database
        for user in init_users:
            if session.query(User).filter(User.email == user.email).first():
                logger.debug(f"Skipping user {user.email} as it already exists")
                continue
            session.add(user)

        # Commit
        session.commit()
        logger.info("Users initialized")


def load():
    """
    Load users from a YAML file.

    Returns
    -------
    None
        This function does not return a value.
    """
    # Open and read the users YAML file
    with open(resource_filename("app", "resources/users.yml")) as f:
        data = yaml.safe_load(f)

    # Convert the loaded data to initialize users
    _init_users(data["users"])
