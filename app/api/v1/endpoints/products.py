from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_products():
    return {"message": "List of products"}
