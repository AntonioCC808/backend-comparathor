from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    products = relationship("Product", back_populates="user")
    comparisons = relationship("Comparison", back_populates="user")
