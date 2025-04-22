from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.license_activation import license_activation
from app.models.user import User
from app.schemas.license_activation import LicenseActivation as LicenseActivationSchema
from app.schemas.license_activation import LicenseActivationCreate, LicenseActivationUpdate

router = APIRouter()

@router.get("/", response_model=List[LicenseActivationSchema])
def read_license_activations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve license activations.
    """
    license_activations = license_activation.get_multi(db, skip=skip, limit=limit)
    return license_activations

@router.post("/", response_model=LicenseActivationSchema)
def create_license_activation(
    *,
    db: Session = Depends(deps.get_db),
    license_activation_in: LicenseActivationCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new license activation.
    """
    license_activation_obj = license_activation.create(db, obj_in=license_activation_in)
    return license_activation_obj

@router.put("/{license_activation_id}", response_model=LicenseActivationSchema)
def update_license_activation(
    *,
    db: Session = Depends(deps.get_db),
    license_activation_id: int,
    license_activation_in: LicenseActivationUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a license activation.
    """
    license_activation_obj = license_activation.get(db, id=license_activation_id)
    if not license_activation_obj:
        raise HTTPException(
            status_code=404,
            detail="License activation not found"
        )
    license_activation_obj = license_activation.update(db, db_obj=license_activation_obj, obj_in=license_activation_in)
    return license_activation_obj

@router.get("/{license_activation_id}", response_model=LicenseActivationSchema)
def read_license_activation(
    *,
    db: Session = Depends(deps.get_db),
    license_activation_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get license activation by ID.
    """
    license_activation_obj = license_activation.get(db, id=license_activation_id)
    if not license_activation_obj:
        raise HTTPException(
            status_code=404,
            detail="License activation not found"
        )
    return license_activation_obj

@router.delete("/{license_activation_id}", response_model=LicenseActivationSchema)
def delete_license_activation(
    *,
    db: Session = Depends(deps.get_db),
    license_activation_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a license activation.
    """
    license_activation_obj = license_activation.get(db, id=license_activation_id)
    if not license_activation_obj:
        raise HTTPException(
            status_code=404,
            detail="License activation not found"
        )
    license_activation_obj = license_activation.remove(db, id=license_activation_id)
    return license_activation_obj 