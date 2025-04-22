from typing import Optional
from pydantic import BaseModel
from app.schemas.base import BaseSchema

class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenPayload(BaseSchema):
    sub: Optional[int] = None 