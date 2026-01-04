"""
Reports API Routes

RESTful endpoints for workload reports.
Access: MANAGEMENT and ADMIN can view all reports, ACADEMIC can view own reports
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff
from typing import Optional

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/staff-workload")
def get_staff_workload_report(
    staff_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get staff workload report.
    MANAGEMENT/ADMIN: Can view any staff
    ACADEMIC: Can only view own workload
    """
    # ACADEMIC can only view own workload
    if current_user.role == "ACADEMIC":
        if staff_id and staff_id != current_user.staff_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own workload"
            )
        staff_id = current_user.staff_id
    
    # TODO: Implement actual report generation
    return {
        "message": "Report endpoint - implementation pending",
        "staff_id": staff_id,
        "semester": semester
    }


@router.get("/department-summary")
def get_department_summary(
    department: Optional[str] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
):
    """
    Get department workload summary.
    MANAGEMENT and ADMIN only.
    """
    # TODO: Implement actual report generation
    return {
        "message": "Department summary report - implementation pending",
        "department": department,
        "semester": semester
    }


@router.get("/overload-underload")
def get_overload_underload_report(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
):
    """
    Get overload/underload report.
    MANAGEMENT and ADMIN only.
    """
    # TODO: Implement actual report generation
    return {
        "message": "Overload/underload report - implementation pending",
        "semester": semester
    }

