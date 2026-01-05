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
from app.services.report_service import ReportService
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/staff-workload")
def get_staff_workload_report(
    staff_id: Optional[int] = None,
    semester: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get staff workload summary report.
    
    WHAT THIS ENDPOINT DOES: Returns workload summary for staff members including:
    - Total assigned hours per staff
    - Overload/underload status
    - Max hours per week (from DesignationWorkloadPolicy)
    
    AUTHORIZATION:
    - ACADEMIC: Can only view own workload (staff_id must match current_user.staff_id or be omitted)
    - ADMIN/MANAGEMENT: Can view any staff workload
    
    QUERY PARAMETERS:
    - staff_id: Optional staff ID filter (ACADEMIC: ignored, uses own ID)
    - semester: Optional semester filter (e.g., "2025S1")
    - department: Optional department filter (ADMIN/MANAGEMENT only)
    
    RETRIEVES FROM DB:
    - staff table
    - assignments table
    - task_instances table
    - designation_workload_policies table
    
    USE CASE: Staff workload summary report for admin dashboard or staff profile
    
    Returns:
        Dictionary with staff workload data
    """
    # ACADEMIC can only view own workload
    if current_user.role == "ACADEMIC":
        staff_id = current_user.staff_id
        department = None  # ACADEMIC cannot filter by department
    
    # Get workload summary
    summary = ReportService.get_staff_workload_summary(db, semester, department)
    
    # If staff_id specified, filter to that staff
    if staff_id:
        summary = [s for s in summary if s['staff_id'] == staff_id]
    
    return {
        "data": summary,
        "count": len(summary),
        "semester": semester,
        "department": department
    }


@router.get("/workload-by-type")
def get_workload_by_type(
    staff_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get workload breakdown by task type (teaching, admin, research).
    
    AUTHORIZATION:
    - ACADEMIC: Can only view own workload
    - ADMIN/MANAGEMENT: Can view any staff workload
    
    QUERY PARAMETERS:
    - staff_id: Optional staff ID filter
    - semester: Optional semester filter
    """
    if current_user.role == "ACADEMIC":
        staff_id = current_user.staff_id
    
    data = ReportService.get_workload_by_task_type(db, staff_id, semester)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester
    }


@router.get("/workload-by-domain")
def get_workload_by_domain(
    staff_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get workload breakdown by domain.
    
    AUTHORIZATION:
    - ACADEMIC: Can only view own workload
    - ADMIN/MANAGEMENT: Can view any staff workload
    """
    if current_user.role == "ACADEMIC":
        staff_id = current_user.staff_id
    
    data = ReportService.get_workload_by_domain(db, staff_id, semester)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester
    }


@router.get("/department-summary")
def get_department_summary(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get department workload summary.
    
    WHAT THIS ENDPOINT DOES: Returns average workload per department.
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - semester: Optional semester filter
    
    USE CASE: Department-level workload reports for management
    """
    data = ReportService.get_department_average_workload(db, semester)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester
    }


@router.get("/program-teaching-load")
def get_program_teaching_load(
    program_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get program teaching load report.
    
    WHAT THIS ENDPOINT DOES: Returns teaching load per program including:
    - Total task instances
    - Assigned vs unassigned tasks
    - Total hours per program
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - program_id: Optional program ID filter
    - semester: Optional semester filter
    
    USE CASE: Program-level teaching load reports for HoD/Dean
    """
    data = ReportService.get_program_teaching_load(db, semester, program_id)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester,
        "program_id": program_id
    }


@router.get("/unassigned-tasks")
def get_unassigned_tasks(
    program_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get unassigned tasks report (critical for admin).
    
    WHAT THIS ENDPOINT DOES: Returns all approved task instances that are not assigned.
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - program_id: Optional program ID filter
    - semester: Optional semester filter
    
    USE CASE: Identify workload gaps, input for GA optimization
    """
    data = ReportService.get_unassigned_tasks(db, semester, program_id)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester,
        "program_id": program_id
    }


@router.get("/overload-underload")
def get_overload_underload_report(
    semester: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get overload/underload distribution report.
    
    WHAT THIS ENDPOINT DOES: Returns distribution of staff by workload status:
    - OVERLOADED: Staff with hours > max_hours
    - UNDERLOADED: Staff with hours < 50% of max_hours
    - BALANCED: Staff with hours between 50% and 100% of max_hours
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - semester: Optional semester filter
    - department: Optional department filter
    
    USE CASE: Workload distribution charts for admin dashboard
    """
    data = ReportService.get_overload_underload_distribution(db, semester, department)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester,
        "department": department
    }


@router.get("/ga-input-snapshot")
def get_ga_input_snapshot(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get GA optimization input snapshot.
    
    WHAT THIS ENDPOINT DOES: Returns unassigned approved task instances with their requirements.
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - semester: Optional semester filter
    
    USE CASE: Feed GA with clean data, debug optimization
    """
    data = ReportService.get_ga_input_snapshot(db, semester)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester
    }


@router.get("/ga-result-summary")
def get_ga_result_summary(
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get GA optimization result summary.
    
    WHAT THIS ENDPOINT DOES: Returns summary of GA optimization results including:
    - Total assigned tasks
    - Total assigned hours
    - System vs admin assignments
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - semester: Optional semester filter
    
    USE CASE: Show GA effectiveness, viva explanation
    """
    data = ReportService.get_ga_result_summary(db, semester)
    
    return {
        **data,
        "semester": semester
    }


@router.get("/change-requests")
def get_change_request_summary(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get change request summary report.
    
    WHAT THIS ENDPOINT DOES: Returns summary of change requests by status.
    
    AUTHORIZATION:
    - ACADEMIC: Can view own change requests only (filtered in service if needed)
    - ADMIN/MANAGEMENT: Can view all change requests
    
    USE CASE: Governance & transparency
    """
    data = ReportService.get_change_request_summary(db)
    
    return {
        "data": data,
        "count": len(data)
    }


@router.get("/staff/{staff_id}/detailed")
def get_staff_detailed_workload(
    staff_id: int,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed workload report for a specific staff member.
    
    WHAT THIS ENDPOINT DOES: Returns detailed breakdown of all assignments for a staff member.
    
    AUTHORIZATION:
    - ACADEMIC: Can only view own detailed workload
    - ADMIN/MANAGEMENT: Can view any staff detailed workload
    
    PATH PARAMETERS:
    - staff_id: Staff ID to get report for
    
    QUERY PARAMETERS:
    - semester: Optional semester filter
    
    USE CASE: Detailed staff workload report for PDF export
    """
    # ACADEMIC can only view own workload
    if current_user.role == "ACADEMIC" and staff_id != current_user.staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own workload"
        )
    
    data = ReportService.get_staff_detailed_workload(db, staff_id, semester)
    
    return {
        "data": data,
        "count": len(data),
        "staff_id": staff_id,
        "semester": semester
    }


@router.get("/program-section-workload")
def get_program_section_workload(
    program_id: Optional[int] = None,
    semester: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "MANAGEMENT"))
) -> Dict[str, Any]:
    """
    Get workload breakdown by program section.
    
    WHAT THIS ENDPOINT DOES: Returns workload breakdown by program section.
    
    AUTHORIZATION: MANAGEMENT and ADMIN only
    
    QUERY PARAMETERS:
    - program_id: Optional program ID filter
    - semester: Optional semester filter
    
    USE CASE: Program section-level workload reports
    """
    data = ReportService.get_program_section_workload(db, semester, program_id)
    
    return {
        "data": data,
        "count": len(data),
        "semester": semester,
        "program_id": program_id
    }
