from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models.product import ProductType
from app.schemas.product import ProductTypeCreateDTO, ProductTypeDTO
from app.utils import get_current_admin_user

router = APIRouter()

@router.post("/product-types", response_model=ProductTypeDTO, status_code=status.HTTP_201_CREATED)
def create_product_type(
    product_type_data: ProductTypeCreateDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """
    Create a new product type. Only accessible to administrators.

    Parameters
    ----------
    product_type_data : ProductTypeCreateDTO
        The new product type data.

    db : Session
        The database session dependency.

    current_user : dict
        The current authenticated admin user.

    Returns
    -------
    ProductTypeDTO
        The created product type.
    """
    new_product_type = ProductType(**product_type_data.model_dump())
    db.add(new_product_type)
    db.commit()
    db.refresh(new_product_type)
    return ProductTypeDTO.model_validate(new_product_type)