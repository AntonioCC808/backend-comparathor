from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models.product import ProductType, Product
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


@router.delete("/product-types/{product_type_id}", status_code=200)
def delete_product_type(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user),
):
    """
    Delete a product type if no products are associated with it.

    Parameters
    ----------
    product_type_id : int
        The ID of the product type to delete.

    db : Session
        The database session dependency.

    current_user : dict
        The current authenticated admin user.

    Returns
    -------
    dict
        A success message.
    """
    # Check if the product type exists
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")

    # Check if there are products associated with this type
    product_count = db.query(Product).filter(Product.product_type_id == product_type_id).count()
    if product_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete product type with associated products")

    # Delete the product type
    db.delete(product_type)
    db.commit()
    return {"message": "Product type deleted successfully"}