"""
ModuleSection Schemas - Data Validation for Module Section API

⚠️ NOTE: ModuleSection is NOT currently used in workload assignment or GA algorithm.
The current system uses ProgramSection instead. ModuleSection exists in the codebase
but is not referenced by TaskInstance, Assignment, or GA optimization.

PURPOSE (when/if implemented):
ModuleSection represents sections within a course/module (e.g., Unit 1, Unit 2, or Section 1, Section 2).
This allows different professors with different specializations to teach different parts of a course.

These Pydantic schemas define the data structures for ModuleSection API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional


class ModuleSectionCreate(BaseModel):
    """
    Schema for creating a new module section.
    
    WHAT: Used when POST /api/module-sections is called (create new module section)
    NOTE: Currently not used in workload assignment system
    
    PURPOSE (when implemented):
    - Represents sections within a course/module (e.g., Unit 1, Unit 2)
    - Allows different professors to teach different parts of a course
    - Each section can have different student counts and instructors
    """
    # MODULE_ID: Which module this section belongs to
    # WHAT: Links section to its parent module/course
    # EXAMPLE: Module ID 5 = "Database Management Systems" course
    module_id: int
    
    # SECTION_CODE: Letter/identifier for the section
    # WHAT: Identifies the section within the module (e.g., "A", "B", "Unit 1")
    # EXAMPLES: "A", "B", "C", "Unit 1", "Unit 2"
    # NOTE: Typically single letter or descriptive name
    section_code: str
    
    # STUDENT_COUNT: Number of students in this module section
    # WHAT: Used for workload calculations and resource planning
    # EXAMPLES: 50, 45, 48 students
    # NOTE: Can vary between sections of the same module
    student_count: int


class ModuleSectionUpdate(BaseModel):
    """
    Schema for updating an existing module section (partial update).
    
    WHAT: Used when PUT /api/module-sections/{id} is called (update module section)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    
    NOTE: Currently only student_count can be updated (section_code and module_id typically don't change)
    """
    # STUDENT_COUNT: Number of students (can be updated if enrollment changes)
    # WHAT: Update student count if enrollment changes during semester
    # NOTE: Only field that makes sense to update (module_id and section_code shouldn't change)
    student_count: Optional[int]


class ModuleSectionResponse(ModuleSectionCreate):
    """
    Schema for module section API responses.
    
    WHAT: Used when GET /api/module-sections returns data (read module section)
    INHERITS: All fields from ModuleSectionCreate (module_id, section_code, student_count)
    ADDS: section_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes section_id (from database)
    - Includes all fields from ModuleSectionCreate
    """
    section_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
