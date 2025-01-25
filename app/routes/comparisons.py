from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.comparison import Comparison
from app.schemas.comparison import ComparisonDTO, ComparisonBase
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=list[ComparisonDTO])
def get_comparisons(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[ComparisonDTO]:
    """
    Retrieve a list of comparisons.

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
    comparisons = db.query(Comparison).offset(skip).limit(limit).all()
    return [
        ComparisonDTO(
            title=comparison.title,
            description=comparison.description,
            date_created=comparison.date_created,
            id_user=comparison.id_user,
            id=comparison.id,
        )
        for comparison in comparisons
    ]


@router.post("/", response_model=ComparisonDTO)
def create_comparison(
    comparison: ComparisonBase, db: Session = Depends(get_db)
) -> ComparisonDTO:
    """
    Create a new comparison record.

    Parameters
    ----------
    comparison : ComparisonBase
        The details of the comparison to be created.
    db : Session
        The database session dependency.

    Returns
    -------
    ComparisonDTO
        The newly created comparison record.
    """
    new_comparison = Comparison(**comparison.model_dump())
    db.add(new_comparison)
    db.commit()
    db.refresh(new_comparison)
    return ComparisonDTO(
        title=new_comparison.title,
        description=new_comparison.description,
        id=new_comparison.id,
        id_user=new_comparison.id_user,
        date_created=new_comparison.date_created,
    )


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
    return ComparisonDTO(
        title=comparison.title,
        description=comparison.description,
        date_created=comparison.date_created,
        id_user=comparison.id_user,
        id=comparison.id,
    )


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
