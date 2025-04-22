from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.client import Client  # Adjust according to your actual model's path
from app.schemas.client import ClientCreate, ClientUpdate  # Adjust according to your schema's path

class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    pass

client = CRUDClient(Client)
