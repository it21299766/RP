"""
Workload API Routes

RESTful endpoints for viewing workload and assignments.
Access: All authenticated users (see own assignments)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth_guard import get_current_user
from app.models.staff import Staff
from app.models.assignment import Assignment
from app.models.task_instance import TaskInstance
from app.models.task_template import TaskTemplate
from app.models.program import Program
from app.models.program_section import ProgramSection
from app.schemas.workload import WorkloadAssignmentResponse
from typing import List

router = APIRouter(prefix="/api/workload", tags=["Workload"])


@router.get("/my-assignments", response_model=List[WorkloadAssignmentResponse])
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get all assignments for the current logged-in user with task details.
    
    WHAT THIS DOES: Returns all assignments for the logged-in user (staff or admin)
    with complete task details including:
    - Task name (from task template)
    - Task type (lecture, lab, tutorial, etc.)
    - Hours assigned
    - Semester and academic year
    - Program and section information
    
    RETRIEVES FROM DB:
    - Assignment table (filtered by staff_id = current_user.staff_id)
    - TaskInstance table (joined to get task details)
    - TaskTemplate table (joined to get task name and type)
    - Program table (joined to get program name)
    - ProgramSection table (joined to get section name)
    
    ROLE-BASED:
    - ACADEMIC: Only own assignments
    - ADMIN/MANAGEMENT: Only own assignments (if they have any)
    
    Args:
        db: Database session
        current_user: Currently authenticated user
    
    Returns:
        List of WorkloadAssignmentResponse with assignment and task details
    """
    # Get all assignments for current user
    assignments = db.query(Assignment).filter(
        Assignment.staff_id == current_user.staff_id
    ).all()
    
    # Build response with task details
    result = []
    for assignment in assignments:
        if not assignment.task_instance_id:
            continue  # Skip if no task_instance_id (shouldn't happen)
        
        # Get task instance
        task_instance = db.query(TaskInstance).filter(
            TaskInstance.id == assignment.task_instance_id
        ).first()
        
        if not task_instance:
            continue  # Skip if task instance not found
        
        # Get task template for task name and type
        task_template = db.query(TaskTemplate).filter(
            TaskTemplate.id == task_instance.task_template_id
        ).first()
        
        # Get program name
        program_name = None
        section = None
        if task_instance.program_id:
            program = db.query(Program).filter(
                Program.program_id == task_instance.program_id
            ).first()
            if program:
                program_name = program.name
                
                # Get section name if program_section_id exists
                if task_instance.program_section_id:
                    program_section = db.query(ProgramSection).filter(
                        ProgramSection.section_id == task_instance.program_section_id
                    ).first()
                    if program_section:
                        section = program_section.section_code  # Use section_code (e.g., "A", "B", "C")
        
        result.append(WorkloadAssignmentResponse(
            assignment_id=assignment.assignment_id,  # Include assignment_id for change requests
            status=assignment.status,
            task_instance_id=task_instance.id,
            task_name=task_template.name if task_template else None,
            task_type=task_template.task_type if task_template else None,
            hours=task_instance.effective_hours,
            semester=task_instance.semester,
            academic_year=task_instance.academic_year,
            program_name=program_name,
            section=section
        ))
    
    return result

