"""
TaskTemplate Schemas - Data Validation for Task Template API

These Pydantic schemas define the data structures for TaskTemplate API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class TaskTemplateBase(BaseModel):
    """
    Base schema with common fields for task templates.
    
    This is the foundation that Create and Response schemas inherit from.
    Contains all the core fields that define a task template.
    """
    # NAME: Human-readable name of the task template
    # WHAT: Display name shown in UI, dropdowns, reports
    # EXAMPLES: "Database Management Systems Lecture", "Operating Systems Lab"
    # VALIDATION: Must be 1-200 characters long (not empty, not too long)
    name: str = Field(..., min_length=1, max_length=200)
    
    # TASK_TYPE: Category of the task
    # WHAT: Used for grouping, reporting, tariff calculations
    # VALUES: Only these values allowed: "lecture", "lab", "tutorial", "exam", "admin", "research"
    # EXAMPLES: "lecture" for classroom teaching, "lab" for practical sessions
    task_type: Literal["lecture", "lab", "tutorial", "exam", "admin", "research"]
    
    # DEFAULT_HOURS: Standard number of hours for this task type
    # WHAT: Base hours that can be overridden in TaskInstance
    # VALIDATION: Must be greater than 0 (positive number)
    # EXAMPLES: 2.0 hours for lecture, 2.0 hours for lab, 8.0 hours for exam
    # NOTE: TaskInstance can override this with effective_hours
    default_hours: float = Field(..., gt=0)
    
    # REQUIRED_QUALIFICATION_LEVEL: Minimum qualification needed (HARD CONSTRAINT)
    # WHAT: Determines which staff can be assigned (PhD > MSc > BSc)
    # VALUES: Only these values allowed: "BSc", "MSc", "PhD"
    # EXAMPLE: "PhD" requirement means only PhD staff can be assigned
    # NOTE: This is a MUST-HAVE requirement (hard constraint in GA algorithm)
    required_qualification_level: Literal["BSc", "MSc", "PhD"]
    
    # REQUIRED_SPECIALIZATION: Preferred field of expertise (SOFT CONSTRAINT)
    # WHAT: Preferred matching - not required, but better if matched
    # EXAMPLES: "Computer Science", "Physics", "Mathematics"
    # NOTE: Can be None if any specialization is acceptable (soft constraint)
    required_specialization: Optional[str] = None
    
    # REQUIRED_SKILLS: List of skills needed for this task (SOFT CONSTRAINT)
    # WHAT: Preferred matching - more matching skills = better assignment
    # FORMAT: List of strings (e.g., ["Python", "SQL", "Database Design"])
    # DEFAULT: Empty list if no skills specified
    # EXAMPLES: ["Python", "SQL"], ["Java", "OOP"], []
    # NOTE: Empty list means no specific skills required (soft constraint)
    required_skills: List[str] = Field(default_factory=list)
    
    # REQUIRED_EXPERIENCE_YEARS: Minimum years of experience (SOFT CONSTRAINT)
    # WHAT: Preferred matching - staff with more experience preferred
    # VALIDATION: Must be >= 0 (cannot be negative)
    # DEFAULT: 0 (no experience required)
    # EXAMPLES: 5 years, 10 years, 0 (no requirement)
    # NOTE: This is a preference, not a hard requirement (soft constraint)
    required_experience_years: int = Field(default=0, ge=0)
    
    # IS_ACTIVE: Whether this template is currently usable
    # WHAT: Soft deletion flag - keeps historical data, hides from active use
    # DEFAULT: True (template is active by default)
    # USE CASE: Set to False for obsolete templates (old course no longer taught)
    # NOTE: Inactive templates don't appear in dropdowns for new instances
    is_active: bool = True


class TaskTemplateCreate(TaskTemplateBase):
    """
    Schema for creating a new task template.
    
    WHAT: Used when POST /api/task-templates is called (create new template)
    INHERITS: All fields from TaskTemplateBase (name, task_type, default_hours, etc.)
    VALIDATION: All required fields must be provided, validated by Pydantic
    """
    pass


class TaskTemplateUpdate(BaseModel):
    """
    Schema for updating an existing task template (partial update).
    
    WHAT: Used when PUT /api/task-templates/{id} is called (update template)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If name is provided, update name
    - If name is None, don't change name
    - Allows updating just one field (e.g., just is_active) without providing all fields
    """
    # All fields are optional for partial update
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    task_type: Optional[Literal["lecture", "lab", "tutorial", "exam", "admin", "research"]] = None
    default_hours: Optional[float] = Field(None, gt=0)
    required_qualification_level: Optional[Literal["BSc", "MSc", "PhD"]] = None
    required_specialization: Optional[str] = None
    required_skills: Optional[List[str]] = None
    required_experience_years: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class TaskTemplateResponse(TaskTemplateBase):
    """
    Schema for task template API responses.
    
    WHAT: Used when GET /api/task-templates returns data (read template)
    INHERITS: All fields from TaskTemplateBase
    ADDS: id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes id (from database)
    - Includes all fields from TaskTemplateBase
    """
    id: int  # Database-generated primary key

    class Config:
        from_attributes = True  # Pydantic v2 (replaces orm_mode) - enables SQLAlchemy model conversion
