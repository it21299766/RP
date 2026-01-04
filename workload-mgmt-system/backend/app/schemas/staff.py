"""
Staff Schemas - Data Validation and Serialization

This file defines Pydantic schemas for staff data validation and API serialization.
Schemas ensure data is valid before it reaches the database or API responses.

THINK OF IT AS: "Data contracts" that define what data looks like for:
- Creating staff (StaffCreate) - what fields are required/optional
- Updating staff (StaffUpdate) - what fields can be changed
- API responses (StaffResponse) - what data is returned to client

WHY SCHEMAS?
- Validation: Ensures data is correct before processing
- Documentation: Auto-generates API documentation
- Type safety: Catches errors at request time, not database time
- Serialization: Converts database models to JSON for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class StaffBase(BaseModel):
    """
    Base schema with common staff fields.
    
    This is the foundation - fields shared by create, update, and response schemas.
    Contains all the core staff information fields.
    """
    # NAME: Full name of staff member
    # REQUIRED: Yes (everyone has a name)
    # VALIDATION: String, max length handled by database
    name: str
    
    # DESIGNATION: Academic rank/position
    # REQUIRED: Yes (needed for workload policy lookup)
    # EXAMPLES: "Professor", "Senior Lecturer I", "Lecturer"
    # SIGNIFICANCE: Determines workload limits from DesignationWorkloadPolicy
    designation: str
    
    # QUALIFICATION: Highest academic degree
    # REQUIRED: Yes (hard constraint for task assignment)
    # VALUES: Only "BSc", "MSc", or "PhD" allowed (Literal type)
    # SIGNIFICANCE: Determines which tasks staff can be assigned (PhD > MSc > BSc)
    qualification: Literal["BSc", "MSc", "PhD"]
    
    # SPECIALIZATION: Field of expertise
    # REQUIRED: Yes (used for task matching)
    # EXAMPLES: "Computer Science", "Physics", "Mathematics"
    # SIGNIFICANCE: Soft constraint - preferred matching in GA algorithm
    specialization: str
    
    # DEPARTMENT: Academic department
    # REQUIRED: Yes (organizational grouping)
    # EXAMPLES: "Computer Science", "Mathematics"
    # SIGNIFICANCE: Used for filtering, reports, organizational structure
    department: str
    
    # ROLE: System access level
    # REQUIRED: Yes (needed for authentication and authorization)
    # VALUES: Only "ACADEMIC", "ADMIN", or "MANAGEMENT" allowed
    # SIGNIFICANCE: Determines permissions (ACADEMIC=own data, ADMIN=all data)
    role: Literal["ACADEMIC", "ADMIN", "MANAGEMENT"]
    
    # EXPERIENCE_YEARS: Years of professional experience
    # REQUIRED: No (defaults to 0)
    # VALIDATION: Must be >= 0 (ge=0 means "greater than or equal to 0")
    # SIGNIFICANCE: Soft constraint - used in task matching (more experience = better)
    experience_years: int = Field(ge=0, default=0)
    
    # SKILLS: List of technical/professional skills
    # REQUIRED: No (defaults to empty list)
    # FORMAT: List of strings
    # EXAMPLES: ["Python", "Java", "Machine Learning"]
    # SIGNIFICANCE: Soft constraint - GA algorithm matches with task required skills
    skills: Optional[List[str]] = []
    
    # AVAILABLE: Whether staff is currently available
    # REQUIRED: No (defaults to True)
    # SIGNIFICANCE: Prevents assigning tasks to unavailable staff
    # NOTE: Set to False for staff on leave, sabbatical, etc.
    available: bool = True
    
    # MAX_HOURS: Maximum teaching hours (DEPRECATED)
    # REQUIRED: No (optional, deprecated field)
    # VALIDATION: If provided, must be > 0
    # STATUS: Deprecated - use DesignationWorkloadPolicy instead
    # NOTE: Kept for backward compatibility during migration
    max_hours: Optional[float] = Field(None, gt=0)
    
    # USERNAME: Login identifier
    # REQUIRED: No (auto-generated if not provided)
    # FORMAT: "sf" + staff_id for academic, "adm" + staff_id for admin
    # SIGNIFICANCE: Used for login authentication
    # NOTE: Auto-generated during staff creation if not provided
    username: Optional[str] = None


class StaffCreate(StaffBase):
    """
    Schema for creating a new staff member.
    
    WHAT THIS IS FOR: Defines what data is needed when creating staff via API.
    
    INHERITS FROM StaffBase: Gets all base fields (name, designation, etc.)
    ADDS: Optional password field (for initial password setting)
    
    VALIDATION: All StaffBase fields validated, password is optional
    DEFAULT BEHAVIOR: If password not provided, defaults to username
    """
    # PASSWORD: Initial password for the staff member
    # REQUIRED: No (optional - defaults to username if not provided)
    # SECURITY: Will be hashed before storing (never stored as plain text)
    # DEFAULT: If not provided, password = username (e.g., sf7/sf7)
    # USE CASE: Allow admin to set custom password, or use default
    password: Optional[str] = None


class StaffUpdate(BaseModel):
    """
    Schema for updating an existing staff member.
    
    WHAT THIS IS FOR: Defines what fields can be updated (partial update).
    
    DIFFERENCES FROM StaffCreate:
    - All fields are Optional (only update what's provided)
    - No password field (password updates handled separately)
    - Allows partial updates (update just one field)
    
    VALIDATION: Only validates fields that are provided
    USE CASE: Update staff information without providing all fields
    """
    # All fields are Optional - only update what's provided
    # This allows partial updates (e.g., just update designation)
    
    name: Optional[str] = None  # Update name if provided
    designation: Optional[str] = None  # Update designation if provided
    qualification: Optional[Literal["BSc", "MSc", "PhD"]] = None  # Update qualification if provided
    specialization: Optional[str] = None  # Update specialization if provided
    department: Optional[str] = None  # Update department if provided
    role: Optional[Literal["ACADEMIC", "ADMIN", "MANAGEMENT"]] = None  # Update role if provided
    experience_years: Optional[int] = Field(None, ge=0)  # Update experience if provided (must be >= 0)
    skills: Optional[List[str]] = None  # Update skills if provided
    available: Optional[bool] = None  # Update availability if provided
    max_hours: Optional[float] = Field(None, gt=0)  # Deprecated but kept for compatibility


class StaffResponse(StaffBase):
    """
    Schema for API responses (what data is sent back to client).
    
    WHAT THIS IS FOR: Defines what data is returned when getting staff information.
    
    INHERITS FROM StaffBase: Gets all base fields
    ADDS: staff_id, username, and profile_picture_path (database-generated/stored fields)
    
    EXCLUDES: password_hash (security - never return password hash!)
    
    SERIALIZATION: Converts Staff database model to JSON using this schema
    """
    # STAFF_ID: Primary key (database-generated)
    # REQUIRED: Yes (always present in responses)
    # SIGNIFICANCE: Used to identify staff in API calls
    staff_id: int
    
    # USERNAME: Login identifier (may be auto-generated)
    # REQUIRED: No (may be None if not yet generated)
    # SIGNIFICANCE: Used for login, shown in responses
    username: Optional[str] = None
    
    # PROFILE_PICTURE_PATH: Path to profile picture
    # REQUIRED: No (may be None if no picture uploaded)
    # SIGNIFICANCE: Used by frontend to display profile picture
    # FORMAT: Relative path or URL
    profile_picture_path: Optional[str] = None

    class Config:
        # Pydantic v2 configuration
        # from_attributes=True allows creating schema from SQLAlchemy models
        # This is the new way (replaces orm_mode=True in Pydantic v1)
        # Enables: StaffResponse.from_orm(staff_model)
        from_attributes = True


class PasswordUpdate(BaseModel):
    """
    Schema for updating staff password.
    
    WHAT THIS IS FOR: Defines the data needed to change a staff member's password.
    
    FIELDS:
    - current_password: Current password (for verification)
    - new_password: New password (must be provided)
    
    VALIDATION: Both fields are required
    USE CASE: Allow staff to change their password securely
    
    SECURITY: Password will be hashed before storing (never stored as plain text)
    """
    # CURRENT_PASSWORD: Current password for verification
    # REQUIRED: Yes (must provide current password to change it)
    # SIGNIFICANCE: Security measure - prevents unauthorized password changes
    # VALIDATION: Must match existing password_hash in database
    current_password: str
    
    # NEW_PASSWORD: New password to set
    # REQUIRED: Yes (must provide new password)
    # SIGNIFICANCE: The new password that will replace the current one
    # SECURITY: Will be hashed before storing (never stored as plain text)
    # VALIDATION: Should meet password policy (length, complexity) if enforced
    new_password: str
