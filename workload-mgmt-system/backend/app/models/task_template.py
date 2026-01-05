"""
TaskTemplate Model - Reusable Academic Work Definitions

This model represents task templates - reusable definitions of academic work
that can be instantiated multiple times across different semesters and programs.

THINK OF IT AS: A "recipe" or "template" for a type of work that gets reused.
Examples: "Database Management Systems Lecture", "Operating Systems Lab", "Exam Paper Evaluation"

WHY TEMPLATES?
- Don't repeat yourself: Define "DBMS Lecture" once, use it many times
- Consistency: Same task type has same requirements across semesters
- Easy updates: Change template once, affects all future instances
- Historical tracking: Can see which templates were used when
"""

from sqlalchemy import Column, Integer, String, Float, JSON, Boolean
from app.database import Base


class TaskTemplate(Base):
    """
    TaskTemplate Model - Database table for reusable task definitions.
    
    Each row represents one type of academic work that can be assigned.
    These templates are then instantiated as TaskInstances for specific semesters.
    
    RELATIONSHIP: One TaskTemplate → Many TaskInstances (one-to-many)
    EXAMPLE: "DBMS Lecture" template used in Fall 2024, Spring 2025, etc.
    """
    __tablename__ = "task_templates"

    # PRIMARY KEY: Unique identifier for each template
    # SIGNIFICANCE: Used to link TaskInstances to their template
    # USECASE: Foreign key in task_instances table
    # EXAMPLE: Template ID 5 = "Database Management Systems Lecture"
    id = Column(Integer, primary_key=True, index=True)
    
    # NAME: Human-readable name of the task template
    # SIGNIFICANCE: Identifies what this task is (display name)
    # USECASE: Shown in dropdowns, reports, task listings
    # EXAMPLES: "Database Management Systems Lecture", "Operating Systems Lab",
    #           "Final Exam Evaluation", "Research Supervision"
    # NOTE: Should be descriptive and specific
    name = Column(String(200), nullable=False)
    
    # TASK_TYPE: Category of the task
    # SIGNIFICANCE: Used for grouping, reporting, and tariff calculations
    # USECASE: Filter tasks by type, calculate hours based on type
    # VALUES: 
    #   - "lecture": Regular classroom teaching
    #   - "lab": Laboratory/practical sessions
    #   - "tutorial": Tutorial sessions
    #   - "exam": Exam creation, invigilation, marking
    #   - "admin": Administrative tasks (course prep, meetings)
    #   - "research": Research supervision, project guidance
    # NOTE: Different types may have different tariff rates
    task_type = Column(String(20), nullable=False)
    
    # DEFAULT_HOURS: Standard number of hours for this task type
    # SIGNIFICANCE: Base hours that can be overridden in TaskInstance
    # USECASE: Pre-fills hours when creating TaskInstance, used if not overridden
    # EXAMPLE: Lecture template = 2.0 hours, Lab template = 2.0 hours, Exam = 8.0 hours
    # NOTE: TaskInstance can override this with effective_hours
    # CALCULATION: Usually based on tariff rules (lectures are typically 2 hours per week)
    default_hours = Column(Float, nullable=False)
    
    # REQUIRED_QUALIFICATION_LEVEL: Minimum qualification needed (HARD CONSTRAINT)
    # SIGNIFICANCE: Determines which staff can be assigned (PhD > MSc > BSc)
    # USECASE: GA algorithm filters staff by qualification, hard constraint enforcement
    # VALUES: "BSc", "MSc", "PhD"
    # HIERARCHY: PhD can do all, MSc can do MSc/BSc, BSc can only do BSc
    # EXAMPLE: "PhD" requirement means only PhD staff can be assigned
    # NOTE: This is a MUST-HAVE requirement (hard constraint)
    required_qualification_level = Column(String(10), nullable=False)
    
    # REQUIRED_SPECIALIZATION: Preferred field of expertise (SOFT CONSTRAINT)
    # SIGNIFICANCE: Preferred matching - not required, but better if matched
    # USECASE: GA algorithm gives bonuses when staff specialization matches
    # EXAMPLES: "Computer Science", "Physics", "Mathematics", None (any specialization)
    # NOTE: Can be NULL if any specialization is acceptable
    # PREFERENCE: CS task assigned to CS staff is better than Physics staff
    required_specialization = Column(String(100), nullable=True)
    
    # REQUIRED_SKILLS: List of skills needed for this task (SOFT CONSTRAINT)
    # FORMAT: JSON array of strings
    # SIGNIFICANCE: Preferred matching - more matching skills = better assignment
    # USECASE: GA algorithm matches staff skills with required skills
    # EXAMPLES: ["Python", "SQL", "Database Design"], ["Java", "OOP"], []
    # NOTE: Empty list means no specific skills required
    # MATCHING: Staff with ["Python", "SQL"] matches task requiring ["Python"] (1 match)
    required_skills = Column(JSON, default=list)
    
    # REQUIRED_EXPERIENCE_YEARS: Minimum years of experience (SOFT CONSTRAINT)
    # SIGNIFICANCE: Preferred matching - staff with more experience preferred
    # USECASE: GA algorithm gives bonuses when staff experience >= requirement
    # EXAMPLE: Requirement of 5 years, staff with 7 years gets bonus
    # NOTE: This is a preference, not a hard requirement (soft constraint)
    required_experience_years = Column(Integer, default=0)
    
    # IS_ACTIVE: Whether this template is currently usable
    # SIGNIFICANCE: Soft deletion - keeps historical data, hides from active use
    # USECASE: 
    #   - Set to False for obsolete templates (old course no longer taught)
    #   - Prevents creating new instances of inactive templates
    #   - Keeps historical TaskInstances intact
    # NOTE: Inactive templates don't appear in dropdowns for new instances
    is_active = Column(Boolean, default=True, nullable=False)
