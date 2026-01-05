"""
Module Schemas - Data Validation for Module API

These Pydantic schemas define the data structures for Module API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class ModuleCreate(BaseModel):
    """
    Schema for creating a new module.
    
    WHAT: Used when POST /api/modules is called (create new module)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"name": "Database Management Systems", "code": "CS301", "program_id": 1, "semester": 3, "credits": 3}
    """
    # NAME: Full name of the course module
    # WHAT: Human-readable module name shown in UI, course catalogs, reports
    # EXAMPLES: "Database Management Systems", "Operating Systems", "Software Engineering"
    # NOTE: Descriptive full name
    name: str
    
    # CODE: Course code/identifier
    # WHAT: Short code used for referencing the module
    # EXAMPLES: "CS301", "SE401", "DBMS301"
    # NOTE: Must be unique (enforced by database constraint), typically alphanumeric
    code: str
    
    # PROGRAM_ID: Which program this module belongs to
    # WHAT: Links module to its parent program
    # EXAMPLE: Program ID 1 = "Bachelor of Science in Computer Science"
    # NOTE: Module must belong to a valid program (foreign key constraint)
    program_id: int
    
    # SEMESTER: Which semester this module is offered in
    # WHAT: Defines when students take this module
    # VALUES: Typically 1-8 (for 4-year programs) or 1-4 (for 2-year programs)
    # EXAMPLES: 1 (first semester), 3 (third semester), 6 (sixth semester)
    # NOTE: Sequential numbering (1, 2, 3, ...)
    semester: int
    
    # CREDITS: Credit hours/points for this module
    # WHAT: Academic weight of the module
    # EXAMPLES: 3 credits, 4 credits
    # NOTE: Typically 1-6 credits per module
    credits: int


class ModuleUpdate(BaseModel):
    """
    Schema for updating an existing module (partial update).
    
    WHAT: Used when PUT /api/modules/{id} is called (update module)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If name is provided, update name
    - If name is None, don't change name
    - Allows updating just one field (e.g., just credits) without providing all fields
    
    NOTE: program_id and code typically don't change (modules don't move between programs, codes are stable)
    """
    name: Optional[str]  # Optional - update name if provided
    semester: Optional[int]  # Optional - update semester if provided
    credits: Optional[int]  # Optional - update credits if provided


class ModuleResponse(ModuleCreate):
    """
    Schema for module API responses.
    
    WHAT: Used when GET /api/modules returns data (read module)
    INHERITS: All fields from ModuleCreate (name, code, program_id, semester, credits)
    ADDS: module_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes module_id (from database)
    - Includes all fields from ModuleCreate
    """
    module_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
