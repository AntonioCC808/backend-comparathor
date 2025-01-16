from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserDTO(BaseModel):
    user_id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
