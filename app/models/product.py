from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship, Mapped
from app.database import Base


class ProductType(Base):
    __tablename__ = "product_types"
    id = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String)
    metadata_schema = Column(JSON)
    products = relationship("Product", back_populates="product_type")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    id_product_type = Column(Integer, ForeignKey("product_types.id"))
    id_user = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String)
    image = Column(String)
    brand = Column(String)
    score = Column(Float)
    user = relationship("User", back_populates="products")
    product_type = relationship("ProductType", back_populates="products")
    product_metadata = relationship("ProductMetadata", back_populates="product")


class ProductMetadata(Base):
    __tablename__ = "product_metadata"
    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    attribute = Column(String)
    value = Column(String)
    score = Column(Float)
    product = relationship("Product", back_populates="product_metadata")
