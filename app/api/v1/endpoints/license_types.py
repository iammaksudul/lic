from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.license_type import license_type
from app.models.user import User
from app.schemas.license_type import LicenseType as LicenseTypeSchema
from app.schemas.license_type import LicenseTypeCreate, LicenseTypeUpdate

router = APIRouter()

@router.get("/", response_model=List[LicenseTypeSchema])
def read_license_types(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve license types.
    """
    license_types = license_type.get_multi(db, skip=skip, limit=limit)
    return license_types

@router.post("/", response_model=LicenseTypeSchema)
def create_license_type(
    *,
    db: Session = Depends(deps.get_db),
    license_type_in: LicenseTypeCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new license type.
    """
    license_type_obj = license_type.create(db, obj_in=license_type_in)
    return license_type_obj

@router.put("/{license_type_id}", response_model=LicenseTypeSchema)
def update_license_type(
    *,
    db: Session = Depends(deps.get_db),
    license_type_id: int,
    license_type_in: LicenseTypeUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a license type.
    """
    license_type_obj = license_type.get(db, id=license_type_id)
    if not license_type_obj:
        raise HTTPException(
            status_code=404,
            detail="License type not found"
        )
    license_type_obj = license_type.update(db, db_obj=license_type_obj, obj_in=license_type_in)
    return license_type_obj

@router.get("/{license_type_id}", response_model=LicenseTypeSchema)
def read_license_type(
    *,
    db: Session = Depends(deps.get_db),
    license_type_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get license type by ID.
    """
    license_type_obj = license_type.get(db, id=license_type_id)
    if not license_type_obj:
        raise HTTPException(
            status_code=404,
            detail="License type not found"
        )
    return license_type_obj

@router.delete("/{license_type_id}", response_model=LicenseTypeSchema)
def delete_license_type(
    *,
    db: Session = Depends(deps.get_db),
    license_type_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a license type.
    """
    license_type_obj = license_type.get(db, id=license_type_id)
    if not license_type_obj:
        raise HTTPException(
            status_code=404,
            detail="License type not found"
        )
    license_type_obj = license_type.remove(db, id=license_type_id)
    return license_type_obj 