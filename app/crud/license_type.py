from sqlalchemy.orm import Session
from app.models.license_type import LicenseType
from app.schemas.license_type import LicenseTypeCreate, LicenseTypeUpdate
from typing import Optional, List

class CRUDLicenseType:
    def get(self, db: Session, id: int) -> Optional[LicenseType]:
        return db.query(LicenseType).filter(LicenseType.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[LicenseType]:
        return db.query(LicenseType).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: LicenseTypeCreate) -> LicenseType:
        db_obj = LicenseType(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: LicenseType, obj_in: LicenseTypeUpdate) -> LicenseType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[LicenseType]:
        obj = db.query(LicenseType).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

license_type = CRUDLicenseType()
