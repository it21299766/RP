"""
Module API Routes

RESTful endpoints for module management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse
from app.services.module_service import ModuleService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/modules", tags=["Modules"])


@router.post("", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(
    payload: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new module. ADMIN only."""
    return ModuleService.create_module(db, payload)


@router.get("", response_model=list[ModuleResponse])
def get_modules(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of modules. All authenticated users."""
    return ModuleService.get_modules(db)


@router.put("/{module_id}", response_model=ModuleResponse)
def update_module(
    module_id: int,
    payload: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update module. ADMIN only."""
    return ModuleService.update_module(db, module_id, payload)


@router.delete("/{module_id}", status_code=status.HTTP_200_OK)
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete module. ADMIN only."""
    ModuleService.delete_module(db, module_id)
    return {"message": "Module deleted successfully"}
