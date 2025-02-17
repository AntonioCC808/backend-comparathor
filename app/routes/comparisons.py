from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.comparison import Comparison, ComparisonProduct
from app.models.user import User
from app.schemas.comparison import ComparisonDTO, ComparisonBase, ComparisonProductDTO
from app.database import get_db
from app.schemas.product import ProductDTO
from app.utils import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ComparisonDTO])
def get_comparisons(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[ComparisonDTO]:
    """
    Retrieve a list of comparisons, optionally filtered by product type.

    Parameters
    ----------
    skip : int, optional
        The number of records to skip (default is 0).
    limit : int, optional
        The maximum number of records to return (default is 10).
    db : Session
        The database session dependency.

    Returns
    -------
    list[ComparisonDTO]
        A list of comparison records.
    """
    query = db.query(Comparison)

    comparisons = query.offset(skip).limit(limit).all()
    return [ComparisonDTO.model_validate(comparison) for comparison in comparisons]


@router.post("/", response_model=ComparisonDTO)
def create_comparison(
        comparison: ComparisonBase,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> ComparisonDTO:
    """
    Create a new comparison record.

    - If the user is registered, save the comparison in the database.
    - If the user is not registered, return the data **without saving it**.
    """

    # ✅ If the user is not registered, return the DTO without saving
    if current_user is None:
        return ComparisonDTO(
            id=0,  # Temporary ID for frontend use
            title=comparison.title,
            description=comparison.description,
            date_created=comparison.date_created,
            product_type_id=comparison.product_type_id,
            products=[
                ComparisonProductDTO(
                    product=ProductDTO.model_validate({"id": pid})
                ) for pid in comparison.products
            ],
        )

    # Create new comparison in the database for registered users
    new_comparison = Comparison(
        title=comparison.title,
        description=comparison.description,
        user_id=current_user.user_id,  # Ensure the user ID is set
        date_created=comparison.date_created,
        product_type_id=comparison.product_type_id
    )

    db.add(new_comparison)
    db.flush()  # Ensure new_comparison.id is available before adding products

    # ✅ Add linked products
    comparison_products = [
        ComparisonProduct(comparison_id=new_comparison.id, product_id=product_id)
        for product_id in comparison.products
    ]
    db.add_all(comparison_products)

    db.commit()
    db.refresh(new_comparison)

    return ComparisonDTO.model_validate(new_comparison)


@router.get("/{comparison_id}", response_model=ComparisonDTO)
def get_comparison(
    comparison_id: int, db: Session = Depends(get_db)
) -> ComparisonDTO:
    """
    Retrieve a specific comparison by ID.

    Parameters
    ----------
    comparison_id : int
        The ID of the comparison to retrieve.
    db : Session
        The database session dependency.

    Returns
    -------
    ComparisonDTO
        The comparison record.
    """
    comparison = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return ComparisonDTO.model_validate(comparison)



@router.delete("/{comparison_id}", response_model=dict)
def delete_comparison(
    comparison_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ✅ Require authentication
) -> dict:
    """
    Delete a comparison by ID. Only the owner or an admin can delete it.

    Parameters
    ----------
    comparison_id : int
        The ID of the comparison to delete.
    db : Session
        The database session dependency.
    current_user : User
        The currently authenticated user.

    Returns
    -------
    dict
        A confirmation message.
    """
    comparison = db.query(Comparison).filter(Comparison.id == comparison_id).first()

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    # ✅ Ensure only the owner or an admin can delete it
    if comparison.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this comparison")

    db.delete(comparison)
    db.commit()
    return {"message": "Comparison deleted successfully"}
