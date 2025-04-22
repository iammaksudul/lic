# Importing Base from base_class.py to make sure models are registered with SQLAlchemy
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.license import License  # noqa
from app.models.license_type import LicenseType  # noqa
from app.models.product import Product  # noqa
from app.models.client import Client  # noqa
from app.models.license_activation import LicenseActivation  # noqa
