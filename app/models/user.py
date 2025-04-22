from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from app.db.base_class import Base
from sqlalchemy.orm import relationship

# Define the UserRole enum
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    licenses = relationship("License", back_populates="user")
