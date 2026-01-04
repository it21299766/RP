"""
Tariff Model - Workload Calculation Rules

This model defines tariff rules - how many hours different types of tasks take.
Tariffs are used to calculate workload hours based on task type, category, and unit.

THINK OF IT AS: A "rate card" that says "Lectures = 2 hours per section",
"Lab sessions = 2 hours per section", "Marking = 0.1 hours per student".

WHY TARIFFS?
- Standardized workload calculation
- Consistent hours across the system
- Easy to update rates (change once, affects all calculations)
- Transparent policy (hours are based on documented rules)

EXAMPLE: Lecture type, Teaching category, 2 hours, Per Section
= Each lecture section = 2 hours of workload
"""

from sqlalchemy import Column, Integer, String
from app.database import Base


class Tariff(Base):
    """
    Tariff Model - Database table for workload calculation rules.
    
    Each row represents one tariff rule that defines hours for a task type/category/unit combination.
    
    USE CASE: Used to calculate workload hours for tasks
    EXAMPLE: Task Type="lecture", Category="teaching", Per Unit="PER_SECTION", Hours=2
    = Each lecture section = 2 hours
    """
    __tablename__ = "tariffs"

    # PRIMARY KEY: Unique identifier for each tariff rule
    # SIGNIFICANCE: Used to reference specific tariff rules
    # USECASE: Look up tariff rules for workload calculation
    tariff_id = Column(Integer, primary_key=True, index=True)

    # TASK_TYPE: Type of task this tariff applies to
    # SIGNIFICANCE: Categorizes the type of work
    # USECASE: Match tasks to appropriate tariff rules
    # VALUES: 
    #   - "LECTURE": Classroom lectures
    #   - "LAB": Laboratory/practical sessions
    #   - "TUTORIAL": Tutorial sessions
    #   - "MARKING": Exam/assignment marking
    #   - "EXAM": Exam preparation/invigilation
    #   - "ADMIN": Administrative tasks
    #   - "RESEARCH": Research supervision
    # NOTE: Must match task_type values in TaskTemplate
    task_type = Column(String(50), nullable=False)
    
    # CATEGORY: Broad category of work
    # SIGNIFICANCE: Groups related task types for reporting
    # USECASE: 
    #   - Filter tariffs by category
    #   - Generate category-level reports
    #   - Policy grouping
    # VALUES: 
    #   - "TEACHING": Teaching-related tasks (lectures, labs, tutorials)
    #   - "ADMIN": Administrative tasks (meetings, prep work)
    #   - "RESEARCH": Research-related tasks (supervision, projects)
    # NOTE: Helps organize different types of academic work
    category = Column(String(50), nullable=False)
    
    # HOURS: Number of hours for this tariff rule
    # SIGNIFICANCE: The base hours value
    # USECASE: Used in workload calculation (multiplied by unit count if per-unit)
    # EXAMPLES: 2 hours, 4 hours, 0.1 hours
    # NOTE: 
    #   - If per_unit="FIXED": This is the total hours
    #   - If per_unit="PER_SECTION": This is hours per section
    #   - If per_unit="PER_STUDENT": This is hours per student
    hours = Column(Integer, nullable=False)
    
    # PER_UNIT: What unit this tariff is calculated per
    # SIGNIFICANCE: Determines how hours are calculated (per section, per student, or fixed)
    # USECASE: Workload calculation logic
    # VALUES: 
    #   - "PER_SECTION": Hours per section (e.g., 2 hours per lecture section)
    #   - "PER_STUDENT": Hours per student (e.g., 0.1 hours per student for marking)
    #   - "FIXED": Fixed hours regardless of size (e.g., 5 hours for course prep)
    # CALCULATION EXAMPLES:
    #   - PER_SECTION: 2 hours × 1 section = 2 hours
    #   - PER_STUDENT: 0.1 hours × 50 students = 5 hours
    #   - FIXED: 5 hours (regardless of section/student count)
    per_unit = Column(String(50), nullable=False)
