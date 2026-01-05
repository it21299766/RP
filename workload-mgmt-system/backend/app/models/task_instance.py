"""
TaskInstance Model - Specific Task Executions in Time

This model represents a specific execution of a TaskTemplate in a particular
semester, program, and section. Think of TaskTemplate as the "recipe" and
TaskInstance as the "meal" made from that recipe.

THINK OF IT AS: A specific assignment of work for a specific semester/program.
EXAMPLE: "DBMS Lecture for BSCS Section A, Fall 2024"

RELATIONSHIP: TaskTemplate (recipe) → TaskInstance (specific execution)
EXAMPLE: "DBMS Lecture" template → "DBMS Lecture for BSCS-A Fall 2024" instance
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class TaskInstance(Base):
    """
    TaskInstance Model - Database table for specific task executions.
    
    Each row represents one instance of a task template assigned to a specific
    program/section in a specific semester. This is what actually gets assigned
    to staff members.
    
    HIERARCHY: Domain → Program → Program Section → Task Instance
    EXAMPLE: Computing Domain → BSCS Program → Section A → DBMS Lecture Instance
    """
    __tablename__ = "task_instances"

    # PRIMARY KEY: Unique identifier for each task instance
    # SIGNIFICANCE: Used to link instances to assignments
    # USECASE: Foreign key in assignments table (who is assigned to this instance)
    id = Column(Integer, primary_key=True, index=True)
    
    # TASK_TEMPLATE_ID: Links to the template this instance is based on
    # SIGNIFICANCE: References the reusable template definition
    # USECASE: Gets template requirements (qualification, skills, default hours)
    # EXAMPLE: Links to "DBMS Lecture" template to get requirements
    # RELATIONSHIP: Many TaskInstances → One TaskTemplate (many-to-one)
    # NOTE: Multiple instances can use the same template (different semesters)
    task_template_id = Column(Integer, ForeignKey("task_templates.id"), nullable=False)
    
    # DOMAIN_ID: Academic domain this task belongs to
    # SIGNIFICANCE: Top-level organizational grouping
    # USECASE: Filter tasks by domain, generate domain-level reports
    # EXAMPLES: "Computing", "Engineering", "Business", "Science"
    # HIERARCHY: Domain contains multiple Programs
    # EXAMPLE: Computing domain contains BSCS, BSSE, BSIT programs
    domain_id = Column(Integer, ForeignKey("domains.domain_id"), nullable=False)
    
    # PROGRAM_ID: Academic program this task belongs to
    # SIGNIFICANCE: Specific degree program (e.g., BSCS, BSSE)
    # USECASE: Filter tasks by program, assign tasks to program sections
    # EXAMPLES: "Bachelor of Science in Computer Science", "Master of Science in CS"
    # HIERARCHY: Program belongs to Domain, contains Program Sections
    # NOTE: Task instance is assigned to a specific program
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=False)
    
    # PROGRAM_SECTION_ID: Specific section of the program
    # SIGNIFICANCE: Section within a program (Section A, B, C, etc.)
    # USECASE: Assign tasks to specific sections (e.g., "BSCS Section A")
    # EXAMPLES: "Section A", "Section B", "Section C"
    # NOTE: Can be NULL if task applies to entire program (not section-specific)
    # EXAMPLE: "DBMS Lecture for BSCS Section A" vs "Program Coordination" (no section)
    program_section_id = Column(Integer, ForeignKey("program_sections.section_id"), nullable=True)
    
    # SEMESTER: Which semester this task occurs in
    # SIGNIFICANCE: Temporal identifier for when task happens
    # FORMAT: "YYYYSN" where S = S1 (Spring) or S2 (Fall), N = semester number
    # USECASE: Filter tasks by semester, plan workload per semester
    # EXAMPLES: "2025S1" (Spring 2025), "2025S2" (Fall 2025)
    # NOTE: Combined with academic_year gives complete temporal context
    semester = Column(String(20), nullable=False)
    
    # ACADEMIC_YEAR: Which academic year this task belongs to
    # SIGNIFICANCE: Year grouping (academic years span two calendar years)
    # FORMAT: "YYYY-YYYY" (e.g., "2024-2025")
    # USECASE: Group tasks by academic year, generate yearly reports
    # EXAMPLES: "2024-2025", "2025-2026"
    # NOTE: Academic year typically runs from Fall to Spring (e.g., Fall 2024 to Spring 2025)
    academic_year = Column(String(10), nullable=False)
    
    # WEEK_NUMBER: Optional - which week of the semester (for weekly tasks)
    # SIGNIFICANCE: For tasks that happen in specific weeks
    # USECASE: Track weekly tasks, plan week-by-week workload
    # EXAMPLES: 1, 2, 3, ..., 16 (if 16-week semester)
    # NOTE: NULL for tasks that span entire semester (like regular lectures)
    # EXAMPLE: "Week 5 Guest Lecture" would have week_number=5
    week_number = Column(Integer, nullable=True)
    
    # MONTH: Optional - which month (for monthly tasks)
    # SIGNIFICANCE: For tasks that happen in specific months
    # USECASE: Track monthly tasks, plan monthly workload
    # VALUES: 1-12 (January to December)
    # NOTE: NULL for semester-long tasks
    # EXAMPLE: "December Exam Preparation" would have month=12
    month = Column(Integer, nullable=True)
    
    # EFFECTIVE_HOURS: Actual hours for this specific instance
    # SIGNIFICANCE: Overrides template default_hours if different
    # USECASE: Customize hours for specific instances
    # EXAMPLE: Template says 2.0 hours, but this instance needs 3.0 hours
    # NOTE: If not specified, uses template's default_hours
    # CALCULATION: Usually based on student count, complexity, or special requirements
    effective_hours = Column(Float, nullable=False)
    
    # STATUS: Workflow status of this task instance
    # SIGNIFICANCE: Tracks where task is in the approval/execution process
    # VALUES: 
    #   - "draft": Just created, not yet approved
    #   - "approved": Approved and ready for assignment
    #   - "completed": Task has been completed
    # USECASE: Workflow management, filter by status
    # NOTE: Only "approved" tasks should be assigned to staff
    # WORKFLOW: draft → approved → completed
    status = Column(String(20), default="draft", nullable=False)
