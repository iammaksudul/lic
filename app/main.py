from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.security_middleware import RateLimitMiddleware, IPWhitelistMiddleware, RoleBasedAccessMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Set up role-based access middleware
app.add_middleware(RoleBasedAccessMiddleware)

# Set up rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    rate_limit=settings.RATE_LIMIT,
    time_window=settings.RATE_LIMIT_TIME_WINDOW
)

# Set up IP whitelist middleware if enabled
if settings.IP_WHITELIST_ENABLED:
    app.add_middleware(
        IPWhitelistMiddleware,
        allowed_ips=settings.ALLOWED_IPS,
        whitelist_file=settings.IP_WHITELIST_FILE
    )

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Import and include routers
from app.web import router as web_router

# Include web router (for HTML pages)
app.include_router(web_router)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR) 