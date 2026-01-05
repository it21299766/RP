"""
ModuleSection Model - Sections Within Modules

⚠️ NOTE: This model is NOT currently used in workload assignment or GA algorithm.
The current system uses ProgramSection instead. ModuleSection exists in the database
and has CRUD operations, but TaskInstance, Assignment, and GA optimization do NOT
reference module_section_id.

PURPOSE (when/if implemented):
This model represents sections within a course/module (e.g., Unit 1, Unit 2, or Section 1, Section 2).
This allows different professors with different specializations to teach different parts of a course.

EXAMPLE CONCEPT:
- "Database Management Systems" module has "Unit 1: SQL Fundamentals" (taught by Prof A)
- "Database Management Systems" module has "Unit 2: Database Design" (taught by Prof B)

RELATIONSHIP: Module → Module Section
CURRENT STATUS: Model exists but is not used in workload assignment system
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ModuleSection(Base):
    """
    ModuleSection Model - Database table for module sections.
    
    Each row represents one section of a module/course.
    
    RELATIONSHIP: Many Module Sections → One Module (many-to-one)
    
    EXAMPLE: "DBMS" module (Module ID 5) has Module Section A (Section ID 10)
    """
    __tablename__ = "module_sections"

    # PRIMARY KEY: Unique identifier for each module section
    # SIGNIFICANCE: Used to identify specific sections of modules
    # USECASE: Reference in task assignments, scheduling, reporting
    # EXAMPLE: Section ID 10 = "DBMS Section A"
    section_id = Column(Integer, primary_key=True, index=True)

    # MODULE_ID: Which module this section belongs to
    # SIGNIFICANCE: Links section to its parent module
    # USECASE: 
    #   - Filter sections by module
    #   - Generate module-level reports
    #   - Maintain module structure
    # RELATIONSHIP: Many Module Sections → One Module (many-to-one)
    # EXAMPLE: Section A belongs to "DBMS" module (module_id=5)
    module_id = Column(Integer, ForeignKey("modules.module_id"), nullable=False)

    # SECTION_CODE: Letter/identifier for the section
    # SIGNIFICANCE: Identifies the section within the module
    # USECASE: 
    #   - Display section name (e.g., "Section A")
    #   - Distinguish between parallel sections
    #   - Reference in schedules
    # EXAMPLES: "A", "B", "C", "D"
    # NOTE: Typically single letter, but can be alphanumeric
    section_code = Column(String(10), nullable=False)
    
    # STUDENT_COUNT: Number of students in this module section
    # SIGNIFICANCE: Used for workload calculations and resource planning
    # USECASE: 
    #   - Calculate teaching hours (more students = more hours)
    #   - Resource allocation (classroom size, lab capacity)
    #   - Reporting and analytics
    # EXAMPLES: 50, 45, 48 students
    # NOTE: Can vary between sections of the same module
    student_count = Column(Integer, nullable=False)
