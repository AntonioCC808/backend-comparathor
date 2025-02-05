from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str
    user_id: str

class UserRegister(UserBase):
    role: Optional[str] = "user"  # Default role is 'user'


class UserDTO(BaseModel):
    user_id: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
