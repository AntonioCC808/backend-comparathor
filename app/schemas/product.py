from typing import List
from pydantic import BaseModel

class ProductMetadataDTO(BaseModel):
    id: int
    attribute: str
    value: str
    score: float

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    brand: str
    score: float
    id_user: int
    id_product_type: int
    image_base64: str  # ✅ Added field for Base64 encoded image
    product_metadata: List[ProductMetadataDTO]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str
    brand: str
    score: float
    id_user: int
    id: int = None
    product_type_id: int = None
    image_base64: str = None  # ✅ Make it optional in case of updates
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
