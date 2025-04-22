from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from app.core.security import get_current_user
from app.models.user import User, UserRole

router = APIRouter()

# Get the absolute path to the templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Render the home page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Render the login page.
    """
    return templates.TemplateResponse("client/login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Render the registration page.
    """
    return templates.TemplateResponse("client/register.html", {"request": request})

@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """
    Render the admin login page.
    """
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    """
    Render the admin dashboard.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin dashboard"
        )
    return templates.TemplateResponse("admin/index.html", {"request": request, "user": current_user})

@router.get("/client", response_class=HTMLResponse)
async def client_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    """
    Render the client dashboard.
    """
    return templates.TemplateResponse("client/index.html", {"request": request, "user": current_user})

@router.get("/logout", response_class=RedirectResponse)
async def logout():
    """
    Logout the user and redirect to the home page.
    """
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/license-types", response_class=HTMLResponse)
async def license_types_page(request: Request):
    """
    Render the license types page.
    """
    return templates.TemplateResponse("license_types.html", {"request": request})

@router.get("/license-activation", response_class=HTMLResponse)
async def license_activation_page(request: Request):
    """
    Render the license activation page.
    """
    return templates.TemplateResponse("license_activation.html", {"request": request}) 