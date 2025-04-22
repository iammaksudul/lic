from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.licenses import license_type  # Updated to match the file name 'licenses.py'
from app.crud.client import client  # This import should now work if the file exists

from app.models.user import User
from app.schemas.license import License as LicenseSchema
from app.schemas.license import LicenseCreate, LicenseUpdate

router = APIRouter()

@router.get("/", response_model=List[LicenseSchema])
def read_licenses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve licenses.
    """
    licenses = license.get_multi(db, skip=skip, limit=limit)
    return licenses

@router.post("/", response_model=LicenseSchema)
def create_license(
    *,
    db: Session = Depends(deps.get_db),
    license_in: LicenseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new license.
    """
    license_obj = license.create(db, obj_in=license_in)
    return license_obj

@router.put("/{license_id}", response_model=LicenseSchema)
def update_license(
    *,
    db: Session = Depends(deps.get_db),
    license_id: int,
    license_in: LicenseUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a license.
    """
    license_obj = license.get(db, id=license_id)
    if not license_obj:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )
    license_obj = license.update(db, db_obj=license_obj, obj_in=license_in)
    return license_obj

@router.get("/{license_id}", response_model=LicenseSchema)
def read_license(
    *,
    db: Session = Depends(deps.get_db),
    license_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get license by ID.
    """
    license_obj = license.get(db, id=license_id)
    if not license_obj:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )
    return license_obj

@router.delete("/{license_id}", response_model=LicenseSchema)
def delete_license(
    *,
    db: Session = Depends(deps.get_db),
    license_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a license.
    """
    license_obj = license.get(db, id=license_id)
    if not license_obj:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )
    license_obj = license.remove(db, id=license_id)
    return license_obj

@router.post("/{license_id}/activate")
def activate_license(
    *,
    db: Session = Depends(deps.get_db),
    license_id: int,
    hardware_id: str
) -> Any:
    """
    Activate license on a specific hardware.
    """
    license_obj = license.get(db, id=license_id)
    if not license_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    if not license_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="License is not active"
        )
    if license_obj.current_activations >= license_obj.max_activations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum activations reached"
        )
    
    result = license.activate_license(
        db=db, license_id=license_id, hardware_id=hardware_id
    )
    return {"status": "success", "message": "License activated successfully"}
