from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class LicenseType(str, enum.Enum):
    TRIAL = "trial"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    type = Column(Enum(LicenseType))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    status = Column(String, default="active")  # active, expired, revoked
    expires_at = Column(DateTime, nullable=True)
    is_trial = Column(Boolean, default=False)
    max_activations = Column(Integer, default=1)
    current_activations = Column(Integer, default=0)
    hardware_id = Column(String, nullable=True)
    license_metadata = Column(JSON, nullable=True)  # Renamed metadata to license_metadata
    
    # Relationships
    user = relationship("User", back_populates="licenses")
    product = relationship("Product", back_populates="licenses")
    activations = relationship("LicenseActivation", back_populates="license")
