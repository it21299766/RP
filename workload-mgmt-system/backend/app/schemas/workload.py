"""
Workload Schemas - Data Validation for My Workload API

These Pydantic schemas define the data structures for workload/assignment display.
They include task details along with assignment information.
"""

from pydantic import BaseModel
from typing import Optional


class WorkloadAssignmentResponse(BaseModel):
    """
    Schema for a single assignment with task details.
    
    WHAT: Used when GET /api/workload/my-assignments returns data
    CONTAINS: Assignment info + Task details (hours, task name, program, semester, etc.)
    """
    # Assignment fields
    assignment_id: int
    status: str  # "assigned", "completed"
    
    # Task instance fields
    task_instance_id: int
    task_name: Optional[str] = None  # From task template
    task_type: Optional[str] = None  # From task template (lecture, lab, etc.)
    hours: float  # effective_hours from task instance
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    program_name: Optional[str] = None  # From program
    section: Optional[str] = None  # From program section
    
    class Config:
        from_attributes = True

