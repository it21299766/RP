"""
Domain Schemas - Data Validation for Domain API

These Pydantic schemas define the data structures for Domain API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class DomainCreate(BaseModel):
    """
    Schema for creating a new domain.
    
    WHAT: Used when POST /api/domains is called (create new domain)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"name": "Computing", "description": "Computer Science and IT programs"}
    """
    # NAME: Name of the academic domain
    # WHAT: Display name shown in UI, dropdowns, reports
    # EXAMPLES: "Computing", "Engineering", "Business", "Science"
    # NOTE: Must be unique (enforced by database constraint)
    name: str
    
    # DESCRIPTION: Optional description of the domain
    # WHAT: Provides additional context about the domain
    # EXAMPLES: "Computer Science and IT related programs", "Engineering programs"
    # NOTE: Optional field - can be None if no description provided
    description: Optional[str]


class DomainResponse(DomainCreate):
    """
    Schema for domain API responses.
    
    WHAT: Used when GET /api/domains returns data (read domain)
    INHERITS: All fields from DomainCreate (name, description)
    ADDS: domain_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes domain_id (from database)
    - Includes all fields from DomainCreate
    """
    domain_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)


class DomainUpdate(BaseModel):
    """
    Schema for updating an existing domain (partial update).
    
    WHAT: Used when PUT /api/domains/{id} is called (update domain)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    VALIDATION: Only validates fields that are provided (None = field not updated)
    
    PARTIAL UPDATE:
    - If name is provided, update name
    - If name is None, don't change name
    - Allows updating just one field (e.g., just description) without providing all fields
    """
    name: Optional[str]  # Optional - update name if provided
    description: Optional[str]  # Optional - update description if provided
