from typing import List, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Licensing System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT: int = 100
    RATE_LIMIT_TIME_WINDOW: int = 60

    # IP Whitelist
    IP_WHITELIST_ENABLED: bool = False
    ALLOWED_IPS: List[str] = []
    IP_WHITELIST_FILE: str = "ip_whitelist.txt"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def set_db_uri(cls, v, info):
        # Access values from info.data for Pydantic v2
        return v or info.data["DATABASE_URL"]

settings = Settings()
