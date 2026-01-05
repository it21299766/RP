"""
ProgramSection Model - Sections Within Programs

This model represents sections within a program (e.g., Section A, B, C).
Sections allow the same program to have multiple parallel classes/cohorts.

THINK OF IT AS: Different class sections of the same program running in parallel.
EXAMPLE: BSCS Program has Section A (50 students), Section B (45 students), Section C (48 students).

HIERARCHY: Domain → Program → Program Section → Task Instance
WHY SECTIONS?
- Same program, multiple parallel classes
- Different student counts per section
- Tasks can be section-specific (e.g., "DBMS Lecture for Section A")
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ProgramSection(Base):
    """
    ProgramSection Model - Database table for program sections.
    
    Each row represents one section of a program (e.g., Section A of BSCS).
    
    RELATIONSHIPS:
    - Many Program Sections → One Program (many-to-one)
    - One Program Section → Many Task Instances (one-to-many)
    
    UNIQUENESS: Combination of (program_id, section_code, academic_year) should be unique
    (same program can have Section A in different academic years)
    """
    __tablename__ = "program_sections"

    # PRIMARY KEY: Unique identifier for each section
    # SIGNIFICANCE: Used to link task instances to sections
    # USECASE: Foreign key in task_instances table
    # EXAMPLE: Section ID 5 = "BSCS Section A for 2024-2025"
    section_id = Column(Integer, primary_key=True, index=True)

    # PROGRAM_ID: Which program this section belongs to
    # SIGNIFICANCE: Links section to its parent program
    # USECASE: 
    #   - Filter sections by program
    #   - Generate program-level reports
    #   - Maintain hierarchy
    # RELATIONSHIP: Many Program Sections → One Program (many-to-one)
    # EXAMPLE: Section A belongs to BSCS program (program_id=1)
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=False)

    # SECTION_CODE: Letter/identifier for the section
    # SIGNIFICANCE: Identifies the section within the program
    # USECASE: 
    #   - Display section name (e.g., "Section A")
    #   - Distinguish between parallel sections
    #   - Reference in task assignments
    # EXAMPLES: "A", "B", "C", "D"
    # NOTE: Typically single letter, but can be alphanumeric
    section_code = Column(String(10), nullable=False)
    
    # STUDENT_COUNT: Number of students in this section
    # SIGNIFICANCE: Used for workload calculations and resource planning
    # USECASE: 
    #   - Calculate teaching hours (more students = more hours)
    #   - Resource allocation (classroom size, lab capacity)
    #   - Reporting and analytics
    # EXAMPLES: 50, 45, 48 students
    # NOTE: Can vary between sections of the same program
    student_count = Column(Integer, nullable=False)
    
    # ACADEMIC_YEAR: Which academic year this section is for
    # SIGNIFICANCE: Sections are year-specific (same program can have sections in different years)
    # FORMAT: "YYYY-YYYY" (e.g., "2024-2025")
    # USECASE: 
    #   - Filter sections by academic year
    #   - Generate yearly reports
    #   - Plan workload per academic year
    # EXAMPLES: "2024-2025", "2025-2026"
    # NOTE: Academic year typically runs from Fall to Spring
    academic_year = Column(String(15), nullable=False)
