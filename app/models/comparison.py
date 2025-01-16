from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from app.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    id_user: Mapped[int] = Column(Integer, ForeignKey("users.user_id"))
    title: Mapped[str] = Column(String(256))
    description: Mapped[str] = Column(String)
    date_created: Mapped[str] = Column(String)
    user = relationship("User", back_populates="comparisons")
    products = relationship("ComparisonProduct", back_populates="comparison")


class ComparisonProduct(Base):
    __tablename__ = "comparison_products"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    comparison_id: Mapped[int] = Column(Integer, ForeignKey("comparisons.id"))
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"))
    comparison = relationship("Comparison", back_populates="products")
