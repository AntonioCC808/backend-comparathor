from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    score = Column(Float)
    id_user = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="products")
