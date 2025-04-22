from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData, Column, Integer

# Default metadata for the SQLAlchemy models
metadata = MetaData()

@as_declarative(metadata=metadata)
class Base:
    id: Any
    __name__: str

    # Automatically generate the table name based on the model class name (lowercased)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Optional: add a default primary key column for consistency
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)

# Lazy loading imports inside functions to avoid circular imports
def import_models():
    from app.models.user import User  # noqa
    from app.models.license import License  # noqa
    from app.models.license_type import LicenseType  # noqa
    from app.models.product import Product  # noqa
    from app.models.client import Client  # noqa
    from app.models.license_activation import LicenseActivation  # noqa
