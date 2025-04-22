from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from app.schemas.base import BaseSchema, TimestampSchema

class ClientBase(BaseSchema):
    name: str
    email: EmailStr
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class ClientInDBBase(ClientBase, TimestampSchema):
    id: int
    api_key: str

    class Config:
        from_attributes = True

class Client(ClientInDBBase):
    pass

class ClientInDB(ClientInDBBase):
    pass 