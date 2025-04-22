from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.license_type import LicenseType
from app.schemas.license_type import LicenseTypeCreate, LicenseTypeUpdate

class CRUDLicenseType(CRUDBase[LicenseType, LicenseTypeCreate, LicenseTypeUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[LicenseType]:
        return db.query(LicenseType).filter(LicenseType.name == name).first()

license_type = CRUDLicenseType(LicenseType) 