# app/models/product.py

from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    version = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True)
    # Rename metadata to avoid conflict with reserved word in SQLAlchemy
    extra_metadata = Column(JSON, nullable=True)
    
    # Relationships
    licenses = relationship("LicenseActivation", back_populates="product")  # Changed relationship name
