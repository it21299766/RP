"""
ProgramSection Schemas - Data Validation for Program Section API

These Pydantic schemas define the data structures for ProgramSection API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.

NOTE: ProgramSection is currently used in workload assignment system.
TaskInstance references program_section_id for section-specific task assignments.
"""

from pydantic import BaseModel
from typing import Optional


class ProgramSectionCreate(BaseModel):
    """
    Schema for creating a new program section.
    
    WHAT: Used when POST /api/program-sections is called (create new program section)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"program_id": 1, "section_code": "A", "student_count": 50, "academic_year": "2024-2025"}
    
    CURRENTLY USED: Yes - ProgramSection is used in TaskInstance for section-specific assignments
    """
    # PROGRAM_ID: Which program this section belongs to
    # WHAT: Links section to its parent program
    # EXAMPLE: Program ID 1 = "Bachelor of Science in Computer Science"
    program_id: int
    
    # SECTION_CODE: Letter/identifier for the section
    # WHAT: Identifies the section within the program (e.g., "A", "B", "C")
    # EXAMPLES: "A", "B", "C", "D"
    # NOTE: Typically single letter, but can be alphanumeric
    section_code: str
    
    # STUDENT_COUNT: Number of students in this section
    # WHAT: Used for workload calculations and resource planning
    # EXAMPLES: 50, 45, 48 students
    # NOTE: Can vary between sections of the same program
    student_count: int
    
    # ACADEMIC_YEAR: Which academic year this section is for
    # WHAT: Sections are year-specific (same program can have sections in different years)
    # FORMAT: "YYYY-YYYY" (e.g., "2024-2025")
    # EXAMPLES: "2024-2025", "2025-2026"
    # NOTE: Academic year typically runs from Fall to Spring
    academic_year: str


class ProgramSectionUpdate(BaseModel):
    """
    Schema for updating an existing program section (partial update).
    
    WHAT: Used when PUT /api/program-sections/{id} is called (update program section)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    
    NOTE: Currently only student_count can be updated (program_id, section_code, academic_year typically don't change)
    """
    # STUDENT_COUNT: Number of students (can be updated if enrollment changes)
    # WHAT: Update student count if enrollment changes during semester
    # NOTE: Only field that makes sense to update (program_id, section_code, academic_year shouldn't change)
    student_count: Optional[int]


class ProgramSectionResponse(ProgramSectionCreate):
    """
    Schema for program section API responses.
    
    WHAT: Used when GET /api/program-sections returns data (read program section)
    INHERITS: All fields from ProgramSectionCreate (program_id, section_code, student_count, academic_year)
    ADDS: section_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes section_id (from database)
    - Includes all fields from ProgramSectionCreate
    """
    section_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
