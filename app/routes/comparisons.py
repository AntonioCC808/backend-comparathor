from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.comparison import Comparison, ComparisonProduct
from app.schemas.comparison import ComparisonCreate, ComparisonOut
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[ComparisonOut])
def get_comparisons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comparisons = db.query(Comparison).offset(skip).limit(limit).all()
    return comparisons

@router.post("/", response_model=ComparisonOut)
def create_comparison(comparison: ComparisonCreate, db: Session = Depends(get_db)):
    new_comparison = Comparison(**comparison.dict())
    db.add(new_comparison)
    db.commit()
    db.refresh(new_comparison)
    return new_comparison
