"""
TaskInstance Schemas - Data Validation for Task Instance API

These Pydantic schemas define the data structures for TaskInstance API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaskInstanceBase(BaseModel):
    """
    Base schema with common fields for task instances.
    
    This is the foundation that Create and Response schemas inherit from.
    Contains all the core fields that define a task instance.
    """
    # TASK_TEMPLATE_ID: Links to the template this instance is based on
    # WHAT: References the reusable template definition (which template to use)
    # EXAMPLE: Template ID 5 = "DBMS Lecture" template
    # NOTE: Multiple instances can use the same template (different semesters)
    task_template_id: int
    
    # DOMAIN_ID: Academic domain this task belongs to
    # WHAT: Top-level organizational grouping (which domain)
    # EXAMPLE: Domain ID 1 = "Computing" domain
    domain_id: int
    
    # PROGRAM_ID: Academic program this task belongs to
    # WHAT: Specific degree program (which program)
    # EXAMPLE: Program ID 1 = "Bachelor of Science in Computer Science"
    program_id: int
    
    # PROGRAM_SECTION_ID: Specific section of the program (optional)
    # WHAT: Section within a program (Section A, B, C, etc.)
    # EXAMPLE: Section ID 5 = "BSCS Section A"
    # NOTE: Can be None if task applies to entire program (not section-specific)
    # CURRENTLY USED: Yes - TaskInstance uses program_section_id for assignment
    program_section_id: Optional[int] = None
    
    # SEMESTER: Which semester this task occurs in
    # WHAT: Temporal identifier for when task happens
    # FORMAT: "YYYYSN" where S = S1 (Spring) or S2 (Fall), N = semester number
    # VALIDATION: Must be 1-20 characters long
    # EXAMPLES: "2025S1" (Spring 2025), "2025S2" (Fall 2025)
    semester: str = Field(..., min_length=1, max_length=20)
    
    # ACADEMIC_YEAR: Which academic year this task belongs to
    # WHAT: Year grouping (academic years span two calendar years)
    # FORMAT: "YYYY-YYYY" (e.g., "2024-2025")
    # VALIDATION: Must be 1-10 characters long
    # EXAMPLES: "2024-2025", "2025-2026"
    academic_year: str = Field(..., min_length=1, max_length=10)
    
    # WEEK_NUMBER: Optional - which week of the semester (for weekly tasks)
    # WHAT: For tasks that happen in specific weeks
    # VALIDATION: Must be between 1 and 52 (valid week numbers)
    # EXAMPLES: 1, 2, 3, ..., 16 (if 16-week semester)
    # NOTE: None for tasks that span entire semester (like regular lectures)
    week_number: Optional[int] = Field(None, ge=1, le=52)
    
    # MONTH: Optional - which month (for monthly tasks)
    # WHAT: For tasks that happen in specific months
    # VALIDATION: Must be between 1 and 12 (January to December)
    # EXAMPLES: 1 (January), 6 (June), 12 (December)
    # NOTE: None for semester-long tasks
    month: Optional[int] = Field(None, ge=1, le=12)
    
    # EFFECTIVE_HOURS: Actual hours for this specific instance
    # WHAT: Overrides template default_hours if different
    # VALIDATION: Must be greater than 0 (positive number)
    # EXAMPLES: 2.0 hours, 3.0 hours, 8.0 hours
    # NOTE: If not specified, uses template's default_hours
    effective_hours: float = Field(..., gt=0)
    
    # STATUS: Workflow status of this task instance
    # WHAT: Tracks where task is in the approval/execution process
    # VALUES: Only these values allowed: "draft", "approved", "completed"
    # DEFAULT: "draft" (new instances start as draft)
    # WORKFLOW: draft → approved → completed
    # NOTE: Only "approved" tasks should be assigned to staff
    status: Literal["draft", "approved", "completed"] = "draft"


class TaskInstanceCreate(TaskInstanceBase):
    """
    Schema for creating a new task instance.
    
    WHAT: Used when POST /api/task-instances is called (create new instance)
    INHERITS: All fields from TaskInstanceBase
    VALIDATION: All required fields must be provided, validated by Pydantic
    """
    pass


class TaskInstanceUpdate(BaseModel):
    """
    Schema for updating an existing task instance (partial update).
    
    WHAT: Used when PUT /api/task-instances/{id} is called (update instance)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If effective_hours is provided, update hours
    - If effective_hours is None, don't change hours
    - Allows updating just one field (e.g., just status) without providing all fields
    """
    # All fields are optional for partial update
    task_template_id: Optional[int] = None
    domain_id: Optional[int] = None
    program_id: Optional[int] = None
    program_section_id: Optional[int] = None
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=10)
    week_number: Optional[int] = Field(None, ge=1, le=52)
    month: Optional[int] = Field(None, ge=1, le=12)
    effective_hours: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["draft", "approved", "completed"]] = None


class TaskInstanceResponse(TaskInstanceBase):
    """
    Schema for task instance API responses.
    
    WHAT: Used when GET /api/task-instances returns data (read instance)
    INHERITS: All fields from TaskInstanceBase
    ADDS: id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes id (from database)
    - Includes all fields from TaskInstanceBase
    """
    id: int  # Database-generated primary key

    class Config:
        from_attributes = True  # Pydantic v2 (replaces orm_mode) - enables SQLAlchemy model conversion
