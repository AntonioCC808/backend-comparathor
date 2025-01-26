from typing import List

from pydantic import BaseModel

from app.schemas.product import ProductDTO


class ComparisonProductDTO(BaseModel):
    id: int
    comparison_id: int
    product: ProductDTO  # Include full product details

    class Config:
        from_attributes = True


class ComparisonDTO(BaseModel):
    id: int
    title: str
    description: str
    id_user: int
    date_created: str
    products: List[ComparisonProductDTO] # Include associated products with details

    class Config:
        from_attributes = True