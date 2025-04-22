from typing import List, Optional
from datetime import datetime
import secrets
from sqlalchemy.orm import Session
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate

def generate_license_key() -> str:
    """Generate a unique license key"""
    return secrets.token_urlsafe(32)

def get(db: Session, id: int) -> Optional[License]:
    return db.query(License).filter(License.id == id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[License]:
    return db.query(License).offset(skip).limit(limit).all()

def get_multi_by_user(
    db: Session, *, user_id: int, skip: int = 0, limit: int = 100
) -> List[License]:
    return (
        db.query(License)
        .filter(License.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_license(db: Session, *, obj_in: LicenseCreate) -> License:
    db_obj = License(
        license_key=generate_license_key(),
        type=obj_in.type,
        user_id=obj_in.user_id,
        product_id=obj_in.product_id,
        max_activations=obj_in.max_activations,
        expires_at=obj_in.expires_at,
        created_at=datetime.utcnow(),
        is_active=True,
        current_activations=0
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: License, obj_in: LicenseUpdate
) -> License:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def activate_license(
    db: Session, *, license_id: int, hardware_id: str
) -> License:
    license = get(db=db, id=license_id)
    if not license:
        return None
    
    license.hardware_id = hardware_id
    license.current_activations += 1
    db.add(license)
    db.commit()
    db.refresh(license)
    return license 