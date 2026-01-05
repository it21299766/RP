"""
Module Model - Course Modules/Subjects

This model represents course modules (subjects/courses) within a program.
Modules are the actual courses that students take (e.g., "Database Management Systems",
"Operating Systems", "Software Engineering").

THINK OF IT AS: Individual courses/subjects that make up a program.
EXAMPLE: BSCS Program contains modules like "DBMS", "OS", "SE", "Networks".

RELATIONSHIP: Program → Module → Module Section
NOTE: Modules are separate from Task Instances (modules are course definitions,
task instances are workload assignments)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Module(Base):
    """
    Module Model - Database table for course modules.
    
    Each row represents one course module/subject within a program.
    
    RELATIONSHIPS:
    - Many Modules → One Program (many-to-one)
    - One Module → Many Module Sections (one-to-many)
    
    EXAMPLE: BSCS Program contains Module "Database Management Systems" (Module ID 5)
    """
    __tablename__ = "modules"

    # PRIMARY KEY: Unique identifier for each module
    # SIGNIFICANCE: Used to link module sections to modules
    # USECASE: Foreign key in module_sections table
    # EXAMPLE: Module ID 5 = "Database Management Systems"
    module_id = Column(Integer, primary_key=True, index=True)
    
    # NAME: Full name of the course module
    # SIGNIFICANCE: Human-readable module name
    # USECASE: Displayed in UI, course catalogs, reports
    # EXAMPLES: "Database Management Systems", "Operating Systems", "Software Engineering"
    # NOTE: Descriptive full name
    name = Column(String(100), nullable=False)
    
    # CODE: Course code/identifier
    # SIGNIFICANCE: Short code used for referencing the module
    # USECASE: 
    #   - Used in timetables, transcripts
    #   - Shown in compact views
    #   - Referenced in documentation
    # EXAMPLES: "CS301", "SE401", "DBMS301"
    # UNIQUE: Each module must have a unique code across all programs
    # NOTE: Typically alphanumeric course code
    code = Column(String(20), unique=True, nullable=False)

    # PROGRAM_ID: Which program this module belongs to
    # SIGNIFICANCE: Links module to its parent program
    # USECASE: 
    #   - Filter modules by program
    #   - Generate program curriculum
    #   - Maintain program structure
    # RELATIONSHIP: Many Modules → One Program (many-to-one)
    # EXAMPLE: "DBMS" module belongs to BSCS program (program_id=1)
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=False)

    # SEMESTER: Which semester this module is offered in
    # SIGNIFICANCE: Defines when students take this module
    # VALUES: Typically 1-8 (for 4-year programs) or 1-4 (for 2-year programs)
    # USECASE: 
    #   - Plan curriculum progression
    #   - Filter modules by semester
    #   - Generate semester schedules
    # EXAMPLES: 1 (first semester), 3 (third semester), 6 (sixth semester)
    # NOTE: Sequential numbering (1, 2, 3, ...)
    semester = Column(Integer, nullable=False)
    
    # CREDITS: Credit hours/points for this module
    # SIGNIFICANCE: Academic weight of the module
    # USECASE: 
    #   - Calculate student workload
    #   - Degree requirements tracking
    #   - Academic planning
    # EXAMPLES: 3 credits, 4 credits
    # NOTE: Typically 1-6 credits per module
    credits = Column(Integer, nullable=False)
