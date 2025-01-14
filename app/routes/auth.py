from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserDTO
from app.models.user import User
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserDTO)
def register(user: UserCreate, db: Session = Depends(get_db)) -> UserDTO:
    """
    Register a new user.

    Parameters
    ----------
    user : UserCreate
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
    new_user = User(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserDTO(user_id=new_user.user_id, email=new_user.email)

@router.post("/login")
def login(email: str = Form(...),  password: str = Form(...), db: Session = Depends(get_db)) -> dict:
    """
    Authenticate a user and generate a JWT token.

    Parameters
    ----------
    email : str
        The email of the user.
    password : str
        The plaintext password of the user.
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
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}