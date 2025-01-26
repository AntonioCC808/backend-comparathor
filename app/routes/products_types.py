from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import ProductType
from app.schemas.product import ProductTypeDTO

router = APIRouter()


@router.get("/", response_model=List[ProductTypeDTO])
def get_product_types(db: Session = Depends(get_db)) -> List[ProductTypeDTO]:
    """
    Retrieve a list of all product types.

    Parameters
    ----------
    db : Session
        The database session dependency.

    Returns
    -------
    list[ProductTypeDTO]
        A list of all product types.
    """
    product_types = db.query(ProductType).all()
    return [ProductTypeDTO.model_validate(product_type) for product_type in product_types]