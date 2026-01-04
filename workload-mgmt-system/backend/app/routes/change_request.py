"""
Change Request API Routes

RESTful endpoints for change request workflow.
Access: ACADEMIC can create, ADMIN can approve/reject
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.change_request import (
    ChangeRequestCreate,
    ChangeRequestAction,
    ChangeRequestResponse
)
from app.services.change_request_service import ChangeRequestService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/change-requests", tags=["Change Requests"])


@router.post("", response_model=ChangeRequestResponse, status_code=status.HTTP_201_CREATED)
def create_change_request(
    payload: ChangeRequestCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ACADEMIC", "ADMIN"))
):
    """
    Create a change request.
    ACADEMIC and ADMIN can create requests.
    """
    # ACADEMIC can only create requests for themselves
    if current_user.role == "ACADEMIC":
        # Ensure the request is for the current user's assignment
        # This validation should be in the service layer
        pass
    return ChangeRequestService.create_request(db, payload)


@router.put("/{request_id}/approve", response_model=ChangeRequestResponse)
def approve_request(
    request_id: int,
    payload: ChangeRequestAction,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Approve a change request. ADMIN only."""
    return ChangeRequestService.approve_request(db, request_id, payload.admin_comment)


@router.put("/{request_id}/reject", response_model=ChangeRequestResponse)
def reject_request(
    request_id: int,
    payload: ChangeRequestAction,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Reject a change request. ADMIN only."""
    return ChangeRequestService.reject_request(db, request_id, payload.admin_comment)


@router.get("", response_model=list[ChangeRequestResponse])
def get_change_requests(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get all change requests.
    ACADEMIC sees own requests only, ADMIN sees all.
    """
    if current_user.role == "ACADEMIC":
        return ChangeRequestService.get_by_staff(db, current_user.staff_id)
    return ChangeRequestService.get_all(db)
