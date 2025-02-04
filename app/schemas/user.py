from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserBase):
    role: Optional[str] = "user"  # Default role is 'user'


class UserDTO(BaseModel):
    user_id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
