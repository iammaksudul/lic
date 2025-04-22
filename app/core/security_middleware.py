from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
import os
from typing import Dict, List, Optional
import ipaddress
import jwt
from jose import JWTError

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User, UserRole

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 100, time_window: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.requests: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        # Clean up old requests
        current_time = time.time()
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < self.time_window]
        else:
            self.requests[client_ip] = []
        
        # Check if rate limit is exceeded
        if len(self.requests[client_ip]) >= self.rate_limit:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Process the request
        response = await call_next(request)
        return response

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_ips: List[str] = None, whitelist_file: str = None):
        super().__init__(app)
        self.allowed_ips = allowed_ips or []
        self.whitelist_file = whitelist_file
        self.ip_ranges = self._parse_ip_ranges()
    
    def _parse_ip_ranges(self) -> List[ipaddress.IPv4Network]:
        ip_ranges = []
        
        # Add IPs from the list
        for ip in self.allowed_ips:
            try:
                if '/' in ip:  # CIDR notation
                    ip_ranges.append(ipaddress.IPv4Network(ip))
                else:  # Single IP
                    ip_ranges.append(ipaddress.IPv4Network(f"{ip}/32"))
            except ValueError:
                # Skip invalid IPs
                continue
        
        # Add IPs from the file if it exists
        if self.whitelist_file and os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                for line in f:
                    ip = line.strip()
                    if not ip or ip.startswith('#'):
                        continue
                    try:
                        if '/' in ip:  # CIDR notation
                            ip_ranges.append(ipaddress.IPv4Network(ip))
                        else:  # Single IP
                            ip_ranges.append(ipaddress.IPv4Network(f"{ip}/32"))
                    except ValueError:
                        # Skip invalid IPs
                        continue
        
        return ip_ranges
    
    def _is_ip_allowed(self, ip: str) -> bool:
        try:
            ip_obj = ipaddress.IPv4Address(ip)
            return any(ip_obj in ip_range for ip_range in self.ip_ranges)
        except ValueError:
            return False
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        # Check if IP is allowed
        if not self._is_ip_allowed(client_ip):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Access denied. Your IP is not in the whitelist."}
            )
        
        # Process the request
        response = await call_next(request)
        return response 

class RoleBasedAccessMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = {
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh",
            "/docs",
            "/redoc",
            "/openapi.json"
        }
        self.admin_paths = {
            "/api/v1/admin",
            "/api/v1/users",
            "/api/v1/licenses"
        }
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Allow public paths without authentication
        if path in self.public_paths:
            return await call_next(request)
        
        # Get the authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"}
            )
        
        token = auth_header.split(" ")[1]
        try:
            # Verify the token and get user role
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            # Get user from database
            db = next(get_db())
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            
            # Check admin paths
            if path in self.admin_paths and user.role != UserRole.ADMIN:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Not authorized to access this resource"}
                )
            
            # Add user to request state for use in route handlers
            request.state.user = user
            
            return await call_next(request)
            
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": str(e)}
            ) 