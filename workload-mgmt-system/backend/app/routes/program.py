"""
Program API Routes

RESTful endpoints for program management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.program import ProgramCreate, ProgramUpdate, ProgramResponse
from app.services.program_service import ProgramService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/programs", tags=["Programs"])


@router.post("", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
def create_program(
    payload: ProgramCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new program. ADMIN only."""
    return ProgramService.create_program(db, payload)


@router.get("", response_model=list[ProgramResponse])
def list_programs(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of programs. All authenticated users."""
    return ProgramService.get_programs(db)


@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    payload: ProgramUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update program. ADMIN only."""
    return ProgramService.update_program(db, program_id, payload)


@router.delete("/{program_id}", status_code=status.HTTP_200_OK)
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete program. ADMIN only."""
    ProgramService.delete_program(db, program_id)
    return {"message": "Program deleted successfully"}
