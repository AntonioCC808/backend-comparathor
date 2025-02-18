from typing import List
from pydantic import BaseModel

class ProductMetadataDTO(BaseModel):
    attribute: str
    value: str
    score: float

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    brand: str
    score: float
    price: float
    product_type_id: int
    image_base64: str  #  Added field for Base64 encoded image
    product_metadata: List[ProductMetadataDTO]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str
    brand: str
    score: float
    image_base64: str
    product_metadata: List[ProductMetadataDTO]


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



class ProductTypeCreateDTO(BaseModel):
    name: str
    description: str
    metadata_schema: dict

