from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Comparison(Base):
    __tablename__ = "comparisons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    id_user = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="comparisons")

class ComparisonProduct(Base):
    __tablename__ = "comparison_products"
    id = Column(Integer, primary_key=True, index=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
