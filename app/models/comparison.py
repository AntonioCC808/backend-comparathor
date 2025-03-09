from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from app.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"))
    title = Column(String(256))
    description = Column(String(500))
    date_created = Column(String(50))

    product_type_id = Column(Integer, ForeignKey("product_types.id"))

    user = relationship("User", back_populates="comparisons")
    product_type = relationship("ProductType")
    products = relationship(
        "ComparisonProduct",
        back_populates="comparison",
        cascade="all, delete-orphan"
    )


class ComparisonProduct(Base):
    __tablename__ = "comparison_products"

    id = Column(Integer, primary_key=True, index=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    comparison = relationship("Comparison", back_populates="products")
    product = relationship("Product")
