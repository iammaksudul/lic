from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.schemas.base import BaseSchema, TimestampSchema

class LicenseActivationBase(BaseSchema):
    license_id: int
    hardware_id: str
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    last_check_in: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class LicenseActivationCreate(LicenseActivationBase):
    pass

class LicenseActivationUpdate(BaseSchema):
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    last_check_in: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class LicenseActivationInDBBase(LicenseActivationBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class LicenseActivation(LicenseActivationInDBBase):
    pass

class LicenseActivationInDB(LicenseActivationInDBBase):
    pass 