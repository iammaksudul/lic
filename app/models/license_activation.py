# app/models/license_activation.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base  # Correct the path to Base

class LicenseActivation(Base):
    __tablename__ = 'license_activations'

    id = Column(Integer, primary_key=True, index=True)
    activation_code = Column(String(255), unique=True, nullable=False)  # Assuming activation code is unique
    client_id = Column(Integer, nullable=False)  # Assuming the client_id is required
    activated_at = Column(DateTime)  # DateTime to store when it was activated
    expiration_date = Column(DateTime)  # DateTime for when the license expires
    
    # Foreign key for the product
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)  # Added the foreign key

    # Relationship to Product
    product = relationship("Product", back_populates="licenses")  # Back reference to Product model
