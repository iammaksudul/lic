from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.base import BaseSchema, TimestampSchema

class UserBase(BaseSchema):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role: Optional[str] = None

class UserInDBBase(UserBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str 