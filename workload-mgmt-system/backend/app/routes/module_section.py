"""
Module Section API Routes

RESTful endpoints for module section management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.module_section import (
    ModuleSectionCreate,
    ModuleSectionUpdate,
    ModuleSectionResponse
)
from app.services.module_section_service import ModuleSectionService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/module-sections", tags=["Module Sections"])


@router.post("", response_model=ModuleSectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(
    payload: ModuleSectionCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new module section. ADMIN only."""
    return ModuleSectionService.create_section(db, payload)


@router.get("", response_model=list[ModuleSectionResponse])
def list_sections(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of module sections. All authenticated users."""
    return ModuleSectionService.get_sections(db)


@router.put("/{section_id}", response_model=ModuleSectionResponse)
def update_section(
    section_id: int,
    payload: ModuleSectionUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update module section. ADMIN only."""
    return ModuleSectionService.update_section(db, section_id, payload)


@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
def delete_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete module section. ADMIN only."""
    ModuleSectionService.delete_section(db, section_id)
    return {"message": "Module section deleted successfully"}
