"""
Assignment API Routes

RESTful endpoints for task assignments.
Access: ADMIN for write, all authenticated for read (ACADEMIC sees own only)
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.assignment import AssignmentCreate, AssignmentResponse, AssignmentUpdate
from app.services.assignment_service import AssignmentService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new assignment. ADMIN only."""
    return AssignmentService.create_assignment(db, payload)


@router.get("", response_model=list[AssignmentResponse])
def list_assignments(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get list of assignments.
    ACADEMIC sees own assignments only, ADMIN/MANAGEMENT see all.
    """
    if current_user.role == "ACADEMIC":
        # Filter to show only own assignments
        all_assignments = AssignmentService.get_all(db)
        return [a for a in all_assignments if a.staff_id == current_user.staff_id]
    return AssignmentService.get_all(db)


@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update assignment. ADMIN only."""
    return AssignmentService.update_assignment(db, assignment_id, payload)


@router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete assignment. ADMIN only."""
    AssignmentService.delete_assignment(db, assignment_id)
    return {"message": "Assignment deleted successfully"}
