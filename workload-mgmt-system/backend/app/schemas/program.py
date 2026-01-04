"""
Program Schemas - Data Validation for Program API

These Pydantic schemas define the data structures for Program API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class ProgramCreate(BaseModel):
    """
    Schema for creating a new program.
    
    WHAT: Used when POST /api/programs is called (create new program)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"name": "Bachelor of Science in Computer Science", "code": "BSCS", "domain_id": 1}
    """
    # NAME: Full name of the academic program
    # WHAT: Human-readable program name shown in UI, reports
    # EXAMPLES: "Bachelor of Science in Computer Science", "Master of Science in CS"
    # NOTE: Descriptive full name (not abbreviation)
    name: str
    
    # CODE: Short code/abbreviation for the program
    # WHAT: Short identifier used in references, URLs, compact views
    # EXAMPLES: "BSCS", "BSSE", "BSIT", "MSCS", "BBA"
    # NOTE: Must be unique (enforced by database constraint), typically uppercase
    code: str
    
    # DOMAIN_ID: Which domain this program belongs to
    # WHAT: Links program to its parent domain
    # EXAMPLE: Domain ID 1 = "Computing" domain
    # NOTE: Program must belong to a valid domain (foreign key constraint)
    domain_id: int


class ProgramUpdate(BaseModel):
    """
    Schema for updating an existing program (partial update).
    
    WHAT: Used when PUT /api/programs/{id} is called (update program)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If name is provided, update name
    - If name is None, don't change name
    - Allows updating just one field (e.g., just name) without providing all fields
    
    NOTE: domain_id typically doesn't change (programs don't move between domains)
    """
    name: Optional[str]  # Optional - update name if provided
    code: Optional[str]  # Optional - update code if provided


class ProgramResponse(ProgramCreate):
    """
    Schema for program API responses.
    
    WHAT: Used when GET /api/programs returns data (read program)
    INHERITS: All fields from ProgramCreate (name, code, domain_id)
    ADDS: program_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes program_id (from database)
    - Includes all fields from ProgramCreate
    """
    program_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
