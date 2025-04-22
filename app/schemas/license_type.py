from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.schemas.base import BaseSchema, TimestampSchema

# Shared properties
class LicenseTypeBase(BaseSchema):
    name: str
    description: Optional[str] = None
    duration_days: Optional[int] = None
    max_activations: int = 1
    is_trial: bool = False
    price: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

# Properties to receive on license type creation
class LicenseTypeCreate(LicenseTypeBase):
    pass

# Properties to receive on license type update
class LicenseTypeUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    max_activations: Optional[int] = None
    is_trial: Optional[bool] = None
    price: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

# Properties shared by models stored in DB
class LicenseTypeInDBBase(LicenseTypeBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

# Properties to return to client
class LicenseType(LicenseTypeInDBBase):
    pass

class LicenseTypeInDB(LicenseTypeInDBBase):
    pass 