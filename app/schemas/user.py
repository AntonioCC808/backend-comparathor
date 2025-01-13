from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserDTO(BaseModel):
    user_id: int
    email: EmailStr

    class Config:
        orm_mode = True