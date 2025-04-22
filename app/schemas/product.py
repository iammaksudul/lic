from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.schemas.base import BaseSchema, TimestampSchema

class ProductBase(BaseSchema):
    name: str
    description: Optional[str] = None
    version: str
    is_active: bool = True
    metadata: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class ProductInDBBase(ProductBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    pass

class ProductInDB(ProductInDBBase):
    pass 