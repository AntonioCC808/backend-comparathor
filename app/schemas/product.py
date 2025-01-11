from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: str
    score: float
    id_user: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
