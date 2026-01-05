"""
Assignment Schemas - Data Validation for Assignment API

⚠️ NOTE: This schema uses legacy task_id field. The new system uses task_instance_id.
This schema is kept for backward compatibility but may need updating to use task_instance_id.

These Pydantic schemas define the data structures for Assignment API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class AssignmentCreate(BaseModel):
    """
    Schema for creating a new assignment.
    
    WHAT: Used when POST /api/assignments is called (assign staff to task)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"staff_id": 1, "task_id": 5, "override": False}
    
    NOTE: Uses legacy task_id - consider updating to task_instance_id
    """
    # STAFF_ID: Which staff member is assigned
    # WHAT: Identifies the staff member being assigned to the task
    # EXAMPLE: Staff ID 1 = "Dr. John Smith"
    staff_id: int
    
    # TASK_ID: Which task is being assigned (LEGACY - consider updating to task_instance_id)
    # WHAT: Identifies the task being assigned
    # EXAMPLE: Task ID 5 = specific task instance
    # NOTE: Legacy field - new system should use task_instance_id instead
    task_id: int
    
    # OVERRIDE: Whether admin override is used
    # WHAT: Flag to indicate if assignment violates rules but is allowed by admin
    # DEFAULT: False (normal assignment following rules)
    # USE CASE: Admin manually assigns staff even if qualification/specialty doesn't match
    # NOTE: If override=True, override_reason should be provided
    override: bool = False
    
    # OVERRIDE_REASON: Explanation when override is used
    # WHAT: Documents why override was necessary (audit trail)
    # EXAMPLES: "Temporary staffing issue", "Special expertise needed"
    # NOTE: Optional, but should be provided when override=True
    override_reason: Optional[str]


class AssignmentResponse(AssignmentCreate):
    """
    Schema for assignment API responses.
    
    WHAT: Used when GET /api/assignments returns data (read assignment)
    INHERITS: All fields from AssignmentCreate (staff_id, task_id, override, override_reason)
    ADDS: assignment_id and status fields (database-generated/calculated)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes assignment_id (from database)
    - Includes status (workflow status)
    - Includes all fields from AssignmentCreate
    """
    assignment_id: int  # Database-generated primary key
    status: str  # Workflow status (e.g., "assigned", "completed")

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)


class AssignmentUpdate(BaseModel):
    """
    Schema for updating an existing assignment (partial update).
    
    WHAT: Used when PUT /api/assignments/{id} is called (update assignment)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If status is provided, update status
    - If status is None, don't change status
    - Allows updating just one field (e.g., just status) without providing all fields
    """
    status: Optional[str]  # Optional - update status if provided (e.g., "assigned", "completed")
    override: Optional[bool]  # Optional - update override flag if provided
    override_reason: Optional[str]  # Optional - update override reason if provided
