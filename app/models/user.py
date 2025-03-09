from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, unique=True)  # Por ejemplo, si usas UUID, usa 36
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50), default="user")

    products = relationship("Product", back_populates="user")
    comparisons = relationship("Comparison", back_populates="user")

