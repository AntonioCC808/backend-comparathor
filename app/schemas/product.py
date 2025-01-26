from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    brand: str
    score: float
    id_user: int
    id_product_type: int


class ProductCreate(ProductBase):
    pass


class ProductDTO(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductTypeDTO(BaseModel):
    id: int
    name: str
    description: str
    metadata_schema: dict

    class Config:
        from_attributes = True