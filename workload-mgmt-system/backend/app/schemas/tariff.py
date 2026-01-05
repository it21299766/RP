"""
Tariff Schemas - Data Validation for Tariff API

These Pydantic schemas define the data structures for Tariff API requests and responses.
They validate incoming data and serialize database models for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected.
"""

from pydantic import BaseModel
from typing import Optional


class TariffCreate(BaseModel):
    """
    Schema for creating a new tariff rule.
    
    WHAT: Used when POST /api/tariffs is called (create new tariff rule)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"task_type": "lecture", "category": "teaching", "hours": 2, "per_unit": "PER_SECTION"}
    
    PURPOSE: Defines workload calculation rules (how many hours different task types take)
    """
    # TASK_TYPE: Type of task this tariff applies to
    # WHAT: Categorizes the type of work
    # EXAMPLES: "LECTURE", "LAB", "TUTORIAL", "MARKING", "EXAM", "ADMIN", "RESEARCH"
    # NOTE: Must match task_type values in TaskTemplate
    task_type: str
    
    # CATEGORY: Broad category of work
    # WHAT: Groups related task types for reporting and policy
    # EXAMPLES: "TEACHING", "ADMIN", "RESEARCH"
    # NOTE: Helps organize different types of academic work
    category: str
    
    # HOURS: Number of hours for this tariff rule
    # WHAT: The base hours value used in workload calculation
    # EXAMPLES: 2 hours, 4 hours, 0.1 hours
    # NOTE: 
    #   - If per_unit="FIXED": This is the total hours
    #   - If per_unit="PER_SECTION": This is hours per section
    #   - If per_unit="PER_STUDENT": This is hours per student
    hours: int
    
    # PER_UNIT: What unit this tariff is calculated per
    # WHAT: Determines how hours are calculated (per section, per student, or fixed)
    # VALUES: "PER_SECTION", "PER_STUDENT", "FIXED"
    # EXAMPLES:
    #   - "PER_SECTION": 2 hours × 1 section = 2 hours
    #   - "PER_STUDENT": 0.1 hours × 50 students = 5 hours
    #   - "FIXED": 5 hours (regardless of section/student count)
    per_unit: str


class TariffUpdate(BaseModel):
    """
    Schema for updating an existing tariff rule (partial update).
    
    WHAT: Used when PUT /api/tariffs/{id} is called (update tariff)
    ALL FIELDS OPTIONAL: Only provided fields are updated (partial update)
    
    NOTE: Currently only hours can be updated (task_type, category, per_unit typically don't change)
    """
    # HOURS: Number of hours (can be updated if policy changes)
    # WHAT: Update hours if workload policy changes
    # NOTE: Only field that makes sense to update (task_type, category, per_unit shouldn't change)
    hours: Optional[int]


class TariffResponse(TariffCreate):
    """
    Schema for tariff API responses.
    
    WHAT: Used when GET /api/tariffs returns data (read tariff)
    INHERITS: All fields from TariffCreate (task_type, category, hours, per_unit)
    ADDS: tariff_id field (database-generated primary key)
    
    SERIALIZATION:
    - Converts SQLAlchemy model to JSON
    - Includes tariff_id (from database)
    - Includes all fields from TariffCreate
    """
    tariff_id: int  # Database-generated primary key

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion (Pydantic v1 syntax)
