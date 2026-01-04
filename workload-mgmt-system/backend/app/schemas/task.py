"""
Task Schemas - Data Validation for Legacy Task API (Deprecated)

⚠️ DEPRECATED: These schemas are kept for backward compatibility during migration.
New code should use TaskTemplateSchemas and TaskInstanceSchemas instead.

These Pydantic schemas define the data structures for the legacy Task API.
The new system splits tasks into TaskTemplate (reusable definitions) and TaskInstance (specific executions).
"""

from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal


class TaskBase(BaseModel):
    """
    Base schema with common fields for legacy tasks.
    
    ⚠️ DEPRECATED: Use TaskTemplateBase and TaskInstanceBase instead.
    
    This schema was for the old monolithic task model.
    """
    # TITLE: Title/name of the task
    # WHAT: Display name shown in UI, reports
    # NOTE: Legacy field - use TaskTemplate.name and TaskInstance hierarchy instead
    title: str
    
    # CATEGORY: Broad category of work
    # WHAT: Groups tasks by type (Teaching, Research, Admin)
    # VALUES: Only these values allowed: "Teaching", "Research", "Admin"
    category: Literal["Teaching", "Research", "Admin"]
    
    # DEPARTMENT: Department this task belongs to (optional)
    # WHAT: Organizational grouping
    # NOTE: Required if category="Teaching" (validated below)
    department: Optional[str]
    
    # REQUIRED_SPECIALTY: Preferred field of expertise (optional)
    # WHAT: Preferred matching - not required, but better if matched
    # NOTE: Required if category="Teaching" (validated below)
    required_specialty: Optional[str]
    
    # REQUIRED_QUALIFICATION: Minimum qualification needed
    # WHAT: Determines which staff can be assigned (PhD > MSc > BSc)
    # VALUES: Only these values allowed: "BSc", "MSc", "PhD"
    required_qualification: Literal["BSc", "MSc", "PhD"]
    
    # TARIFF_HOURS: Number of hours for this task
    # WHAT: Workload hours
    # VALIDATION: Must be greater than 0 (positive number)
    tariff_hours: float = Field(gt=0)
    
    # REQUIRED_SKILLS: List of skills needed for this task
    # WHAT: Preferred matching - more matching skills = better assignment
    # FORMAT: List of strings
    # DEFAULT: Empty list if no skills specified
    required_skills: List[str] = Field(default_factory=list)
    
    # REQUIRED_EXPERIENCE: Minimum years of experience
    # WHAT: Preferred matching - staff with more experience preferred
    # VALIDATION: Must be >= 0 (cannot be negative)
    # DEFAULT: 0 (no experience required)
    required_experience: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_teaching_requirements(cls, model):
        """
        Custom validation: Teaching tasks require department and specialty.
        
        BUSINESS RULE: If category is "Teaching", department and required_specialty must be provided.
        This ensures teaching tasks have proper organizational and expertise context.
        """
        if model.category == "Teaching":
            if not model.department:
                raise ValueError("Teaching tasks require department")
            if not model.required_specialty:
                raise ValueError("Teaching tasks require specialty")
        return model


class TaskCreate(TaskBase):
    """
    Schema for creating a new legacy task.
    
    ⚠️ DEPRECATED: Use TaskTemplateCreate and TaskInstanceCreate instead.
    
    WHAT: Used when POST /api/tasks is called (create new task)
    INHERITS: All fields from TaskBase
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing legacy task (partial update).
    
    ⚠️ DEPRECATED: Use TaskTemplateUpdate and TaskInstanceUpdate instead.
    
    WHAT: Used when PUT /api/tasks/{id} is called (update task)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    """
    title: Optional[str]
    tariff_hours: Optional[float] = Field(gt=0)
    required_skills: Optional[List[str]]
    required_experience: Optional[int] = Field(ge=0)
    status: Optional[Literal["draft", "approved"]]  # Legacy status values


class TaskResponse(TaskBase):
    """
    Schema for legacy task API responses.
    
    ⚠️ DEPRECATED: Use TaskTemplateResponse and TaskInstanceResponse instead.
    
    WHAT: Used when GET /api/tasks returns data (read task)
    INHERITS: All fields from TaskBase
    ADDS: task_id and status fields
    """
    task_id: int  # Database-generated primary key
    status: str  # Workflow status

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
