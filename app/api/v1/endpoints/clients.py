from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.client import client
from app.models.user import User
from app.schemas.client import Client as ClientSchema
from app.schemas.client import ClientCreate, ClientUpdate

router = APIRouter()

@router.get("/", response_model=List[ClientSchema])
def read_clients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve clients.
    """
    clients = client.get_multi(db, skip=skip, limit=limit)
    return clients

@router.post("/", response_model=ClientSchema)
def create_client(
    *,
    db: Session = Depends(deps.get_db),
    client_in: ClientCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new client.
    """
    client_obj = client.create(db, obj_in=client_in)
    return client_obj

@router.put("/{client_id}", response_model=ClientSchema)
def update_client(
    *,
    db: Session = Depends(deps.get_db),
    client_id: int,
    client_in: ClientUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a client.
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    client_obj = client.update(db, db_obj=client_obj, obj_in=client_in)
    return client_obj

@router.get("/{client_id}", response_model=ClientSchema)
def read_client(
    *,
    db: Session = Depends(deps.get_db),
    client_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get client by ID.
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    return client_obj

@router.delete("/{client_id}", response_model=ClientSchema)
def delete_client(
    *,
    db: Session = Depends(deps.get_db),
    client_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a client.
    """
    client_obj = client.get(db, id=client_id)
    if not client_obj:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )
    client_obj = client.remove(db, id=client_id)
    return client_obj 