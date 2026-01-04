"""
Program Section API Routes

RESTful endpoints for program section management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.program_section import (
    ProgramSectionCreate,
    ProgramSectionUpdate,
    ProgramSectionResponse
)
from app.services.program_section_service import ProgramSectionService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/program-sections", tags=["Program Sections"])


@router.post("", response_model=ProgramSectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(
    payload: ProgramSectionCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new program section. ADMIN only."""
    return ProgramSectionService.create_section(db, payload)


@router.get("", response_model=list[ProgramSectionResponse])
def list_sections(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of program sections. All authenticated users."""
    return ProgramSectionService.get_sections(db)


@router.put("/{section_id}", response_model=ProgramSectionResponse)
def update_section(
    section_id: int,
    payload: ProgramSectionUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update program section. ADMIN only."""
    return ProgramSectionService.update_section(db, section_id, payload)


@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
def delete_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete program section. ADMIN only."""
    ProgramSectionService.delete_section(db, section_id)
    return {"message": "Program section deleted successfully"}
