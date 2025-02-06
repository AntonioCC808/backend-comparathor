from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str
    user_id: Optional[str] = None

class UserRegister(UserBase):
    role: str


class UserDTO(BaseModel):
    user_id: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """
    Schema for updating user settings.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None