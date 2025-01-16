from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserDTO
from app.models.user import User
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=UserDTO)
def register(user: UserBase, db: Session = Depends(get_db)) -> UserDTO:
    """
    Register a new user.

    Parameters
    ----------
    user : UserBase
        The user details including email and password.
    db : Session
        The database session dependency.

    Returns
    -------
    UserDTO
        The newly created user.

    Raises
    ------
    HTTPException
        If the email is already registered.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email, password=hash_password(user.password), role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserDTO(user_id=new_user.user_id, email=new_user.email, role=new_user.role)


@router.post("/login")
def login(user_data: UserBase, db: Session = Depends(get_db)) -> dict:
    """
    Authenticate a user and generate a JWT token.

    Parameters
    ----------
    user_data: UserBase
    db : Session
        The database session dependency.

    Returns
    -------
    dict
        A dictionary containing the JWT access token and token type.

    Raises
    ------
    HTTPException
        If the credentials are invalid.
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
