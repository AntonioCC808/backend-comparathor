from pydantic import BaseModel


class ComparisonBase(BaseModel):
    title: str
    description: str
    id_user: int
    date_created: str


class ComparisonDTO(ComparisonBase):
    id: int

    class Config:
        from_attributes = True
