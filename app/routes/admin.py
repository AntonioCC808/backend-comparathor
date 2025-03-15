from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models.product import ProductType, Product
from app.models.user import User
from app.schemas.product import ProductTypeCreateDTO, ProductTypeDTO
from app.schemas.user import UserDTO, UserRoleUpdate
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


@router.put("/roles", response_model=List[UserDTO])
def update_users_roles(
    user_roles_update: List[UserRoleUpdate],
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """
    Update multiple users' roles (only accessible by admins).

    Parameters
    ----------
    user_roles_update : List[UserRoleUpdate]
        List of users and their new roles.
    db : Session
        Database session.
    admin_user : User
        The currently authenticated admin user.

    Returns
    -------
    List[UserDTO]
        The updated user data.

    Raises
    ------
    HTTPException
        If any user is not found or a role is invalid.
    """
    updated_users = []
    for user_data in user_roles_update:
        user = db.query(User).filter(User.user_id == user_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_data.user_id} not found.")

        if user_data.role not in ["user", "admin"]:
            raise HTTPException(status_code=400, detail=f"Invalid role for {user_data.user_id}.")

        user.role = user_data.role
        updated_users.append(user)

    db.commit()
    for user in updated_users:
        db.refresh(user)

    return [UserDTO.model_validate(user) for user in updated_users]


@router.get("/users", response_model=List[UserDTO])
def get_all_users(db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    """
    Fetch all users (only accessible by admins).

    Parameters
    ----------
    db : Session
        Database session.
    admin_user : User
        The currently authenticated admin user.

    Returns
    -------
    List[UserDTO]
        A list of all users in the system.
    """
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return users