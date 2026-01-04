"""
ChangeRequest Schemas - Data Validation for Change Request API

These Pydantic schemas define the data structures for ChangeRequest API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class ChangeRequestCreate(BaseModel):
    """
    Schema for creating a new change request.
    
    WHAT: Used when POST /api/change-requests is called (staff requests assignment change)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"assignment_id": 5, "requested_by_staff_id": 1, "reason": "Schedule conflict"}
    
    WORKFLOW: Request starts with status="PENDING"
    """
    # ASSIGNMENT_ID: Which assignment the request is about
    # WHAT: Links request to the specific assignment to be changed
    # EXAMPLE: Assignment ID 5 = specific staff-task assignment
    assignment_id: int
    
    # REQUESTED_BY_STAFF_ID: Which staff member made this request
    # WHAT: Identifies who is requesting the change
    # EXAMPLE: Staff ID 1 = "Dr. John Smith"
    # NOTE: Staff requesting change may or may not be the assigned staff
    requested_by_staff_id: int
    
    # REASON: Explanation for why the change is requested
    # WHAT: Documents the rationale for the request (required field)
    # EXAMPLES: "Schedule conflict", "Overloaded", "Prefer different course", "Personal reason"
    # NOTE: Staff must provide a reason when creating request
    reason: str


class ChangeRequestAction(BaseModel):
    """
    Schema for admin actions on change requests (approve/reject).
    
    WHAT: Used when POST /api/change-requests/{id}/approve or /reject is called
    VALIDATION: Admin comment is optional but recommended
    
    USE CASE: Admin reviews request and provides feedback/explanation
    """
    # ADMIN_COMMENT: Optional comment from admin when reviewing request
    # WHAT: Allows admin to provide feedback or explanation
    # EXAMPLES: "Approved - workload balanced", "Rejected - no suitable replacement"
    # NOTE: Optional field - only filled when admin reviews request
    admin_comment: Optional[str]


class ChangeRequestResponse(ChangeRequestCreate):
    """
    Schema for change request API responses.
    
    WHAT: Used when GET /api/change-requests returns data (read change request)
    INHERITS: All fields from ChangeRequestCreate (assignment_id, requested_by_staff_id, reason)
    ADDS: request_id, status, and admin_comment fields (database-generated/calculated)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes request_id (from database)
    - Includes status (workflow status: "PENDING", "APPROVED", "REJECTED")
    - Includes admin_comment (if admin has reviewed)
    - Includes all fields from ChangeRequestCreate
    """
    request_id: int  # Database-generated primary key
    status: str  # Workflow status ("PENDING", "APPROVED", "REJECTED")
    admin_comment: Optional[str]  # Admin's comment (if reviewed)

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
