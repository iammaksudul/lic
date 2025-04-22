from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.schemas.base import BaseSchema, TimestampSchema

class LicenseBase(BaseSchema):
    key: str
    user_id: int
    product_id: int
    status: str = "active"
    expires_at: Optional[datetime] = None
    is_trial: bool = False
    max_activations: int = 1
    current_activations: int = 0
    metadata: Optional[Dict[str, Any]] = None

class LicenseCreate(LicenseBase):
    pass

class LicenseUpdate(BaseSchema):
    status: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_trial: Optional[bool] = None
    max_activations: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class LicenseInDBBase(LicenseBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class License(LicenseInDBBase):
    pass

class LicenseInDB(LicenseInDBBase):
    pass 