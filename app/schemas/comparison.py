from typing import List, Optional
from pydantic import BaseModel

from app.schemas.product import ProductDTO

class ComparisonProductDTO(BaseModel):
    id: Optional[int] = None  # Not required for unregistered users
    comparison_id: Optional[int] = None  # Not required for unregistered users
    product: ProductDTO  # ProductDTO contains full product details

    class Config:
        from_attributes = True


class ComparisonBase(BaseModel):
    title: str
    description: str
    date_created: str
    product_type_id: int
    products: List[int]

    class Config:
        from_attributes = True


class ComparisonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ComparisonDTO(ComparisonBase):
    id: int
    products: List[ComparisonProductDTO]

    class Config:
        from_attributes = True