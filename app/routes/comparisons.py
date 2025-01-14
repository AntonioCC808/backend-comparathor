from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.comparison import Comparison
from app.schemas.comparison import ComparisonCreate, ComparisonDTO
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[ComparisonDTO])
def get_comparisons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[ComparisonDTO]:
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
            title=comparison.name, description=comparison.brand, id=comparison.score, id_user=comparison.id
        ) for comparison in comparisons
    ]


@router.post("/", response_model=ComparisonDTO)
def create_comparison(comparison: ComparisonCreate, db: Session = Depends(get_db)) -> ComparisonDTO:
    """
    Create a new comparison record.

    Parameters
    ----------
    comparison : ComparisonCreate
        The details of the comparison to be created.
    db : Session
        The database session dependency.

    Returns
    -------
    ComparisonDTO
        The newly created comparison record.
    """
    new_comparison = Comparison(**comparison.dict())
    db.add(new_comparison)
    db.commit()
    db.refresh(new_comparison)
    return ComparisonDTO(
        title=new_comparison.title,
        description=new_comparison.description,
        id=new_comparison.id,
        id_user=new_comparison.id_user,
    )

