from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.comparison import Comparison, ComparisonProduct
from app.schemas.comparison import ComparisonDTO, ComparisonBase
from app.database import get_db

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
    comparison: ComparisonBase, db: Session = Depends(get_db)
) -> ComparisonDTO:
    """
    Create a new comparison record.
    """
    # ✅ Exclude `products` from direct mapping to avoid AttributeError
    new_comparison = Comparison(
        title=comparison.title,
        description=comparison.description,
        id_user=comparison.id_user,
        date_created=comparison.date_created,
        product_type_id=comparison.product_type_id
    )
    db.add(new_comparison)
    db.flush()  # Ensure new_comparison.id is available before adding products

    # ✅ Ensure `ComparisonProduct` objects are created correctly
    comparison_products = [
        ComparisonProduct(comparison_id=new_comparison.id, product_id=product_id)
        for product_id in comparison.products  # This was previously a list of integers
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
    comparison_id: int, db: Session = Depends(get_db)
) -> dict:
    """
    Delete a comparison by ID.

    Parameters
    ----------
    comparison_id : int
        The ID of the comparison to delete.
    db : Session
        The database session dependency.

    Returns
    -------
    dict
        A confirmation message.
    """
    comparison = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    db.delete(comparison)
    db.commit()
    return {"message": "Comparison deleted successfully"}
