from fastapi import APIRouter
from app.api.v1.endpoints import licenses, users, products, auth

api_router = APIRouter()
 
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(licenses.router, prefix="/licenses", tags=["licenses"])
api_router.include_router(products.router, prefix="/products", tags=["products"]) 