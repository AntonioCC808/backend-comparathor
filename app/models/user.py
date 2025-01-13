from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailStr, unique=True, index=True)
    password = Column(String)
    role = Column(Enum("admin", "user", name="user_roles"), default="user")