"""
Domain Model - Top-Level Academic Organization

This model represents academic domains - the highest level of organizational hierarchy.
Domains group related academic programs together (e.g., Computing, Engineering, Business).

THINK OF IT AS: The "college" or "faculty" level - broad academic areas.
EXAMPLE: Computing Domain contains BSCS, BSSE, BSIT programs.

HIERARCHY: Domain → Program → Program Section → Task Instance
"""

from sqlalchemy import Column, Integer, String
from app.database import Base


class Domain(Base):
    """
    Domain Model - Database table for academic domains.
    
    Each row represents one academic domain that contains multiple programs.
    
    RELATIONSHIP: One Domain → Many Programs (one-to-many)
    EXAMPLE: Computing domain contains BSCS, BSSE, BSIT, MSCS programs
    """
    __tablename__ = "domains"

    # PRIMARY KEY: Unique identifier for each domain
    # SIGNIFICANCE: Used to link programs to domains
    # USECASE: Foreign key in programs table
    # EXAMPLE: Domain ID 1 = "Computing"
    domain_id = Column(Integer, primary_key=True, index=True)
    
    # NAME: Name of the academic domain
    # SIGNIFICANCE: Identifies the domain (display name)
    # USECASE: Shown in dropdowns, reports, organizational structure
    # EXAMPLES: "Computing", "Engineering", "Business", "Science"
    # UNIQUE: Each domain must have a unique name (no duplicates)
    # NOTE: Top-level organizational grouping
    name = Column(String(100), nullable=False, unique=True)
    
    # DESCRIPTION: Optional description of the domain
    # SIGNIFICANCE: Provides additional context about the domain
    # USECASE: Documentation, help text, reports
    # EXAMPLES: "Computer Science and IT related programs", "Engineering programs"
    # NOTE: Optional field for additional information
    description = Column(String(255))
