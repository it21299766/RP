"""
Program Model - Academic Degree Programs

This model represents academic programs (degree programs) that belong to a domain.
Programs are the second level in the hierarchy (Domain → Program).

THINK OF IT AS: Specific degree programs like "Bachelor of Science in Computer Science"
or "Master of Science in Software Engineering".

HIERARCHY: Domain → Program → Program Section → Task Instance
EXAMPLE: Computing Domain → BSCS Program → Section A → DBMS Lecture
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Program(Base):
    """
    Program Model - Database table for academic programs.
    
    Each row represents one degree program that belongs to a domain.
    
    RELATIONSHIPS:
    - Many Programs → One Domain (many-to-one)
    - One Program → Many Program Sections (one-to-many)
    - One Program → Many Task Instances (one-to-many)
    """
    __tablename__ = "programs"

    # PRIMARY KEY: Unique identifier for each program
    # SIGNIFICANCE: Used to link program sections and task instances to programs
    # USECASE: Foreign key in program_sections and task_instances tables
    # EXAMPLE: Program ID 1 = "Bachelor of Science in Computer Science"
    program_id = Column(Integer, primary_key=True, index=True)
    
    # NAME: Full name of the academic program
    # SIGNIFICANCE: Human-readable program name
    # USECASE: Displayed in UI, reports, official documentation
    # EXAMPLES: "Bachelor of Science in Computer Science", "Master of Science in CS"
    # NOTE: Descriptive full name (not abbreviation)
    name = Column(String(150), nullable=False)
    
    # CODE: Short code/abbreviation for the program
    # SIGNIFICANCE: Short identifier used in references and URLs
    # USECASE: 
    #   - Used in API endpoints, file naming
    #   - Shown in compact views (tables, lists)
    #   - Referenced in reports
    # EXAMPLES: "BSCS", "BSSE", "BSIT", "MSCS", "BBA"
    # UNIQUE: Each program must have a unique code (no duplicates)
    # NOTE: Typically uppercase abbreviation
    code = Column(String(20), nullable=False, unique=True)

    # DOMAIN_ID: Which domain this program belongs to
    # SIGNIFICANCE: Links program to its parent domain
    # USECASE: 
    #   - Filter programs by domain
    #   - Generate domain-level reports
    #   - Maintain organizational hierarchy
    # RELATIONSHIP: Many Programs → One Domain (many-to-one)
    # EXAMPLE: BSCS program belongs to Computing domain (domain_id=1)
    domain_id = Column(Integer, ForeignKey("domains.domain_id"), nullable=False)
