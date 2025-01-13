from pydantic import BaseModel
from typing import List

class ComparisonBase(BaseModel):
    title: str
    description: str
    id_user: int

class ComparisonCreate(ComparisonBase):
    pass

class ComparisonDTO(ComparisonBase):
    id: int

    class Config:
        orm_mode = True
