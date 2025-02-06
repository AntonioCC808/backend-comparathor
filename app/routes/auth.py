from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserDTO, UserRegister
from app.models.user import User
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=UserDTO)
def register(user: UserRegister, db: Session = Depends(get_db)) -> UserDTO:
    """
    Register a new user.

    Parameters
    ----------
    user : UserRegister
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
    # Check if user_id already exists
    if db.query(User).filter(User.user_id == user.user_id).first():
        raise HTTPException(status_code=400, detail="User ID already exists. Please choose another.")

    # Check if email is already registered
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        user_id=user.user_id,  # Ensure user_id is included
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserDTO.model_validate(new_user)


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
    token = create_access_token({"sub": user.email, "user_id": user.user_id, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}


@router.get("/me", response_model=UserDTO)
def get_current_user_route(user: User = Depends(get_current_user)):
    """
    Retrieve the currently authenticated user's details.
    """
    return user
