"""
Task Model - Legacy Task Model (Deprecated)

⚠️ DEPRECATED: This model is kept for backward compatibility during migration.
New code should use TaskTemplate and TaskInstance instead.

This was the old monolithic task model that combined template and instance.
The new system splits this into:
- TaskTemplate: Reusable task definitions
- TaskInstance: Specific task executions in time

MIGRATION STATUS: Being phased out in favor of TaskTemplate + TaskInstance
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Task(Base):
    """
    Legacy Task Model - DEPRECATED
    
    This model is kept for backward compatibility but should not be used for new development.
    Use TaskTemplate and TaskInstance instead.
    """
    __tablename__ = "tasks"

    # PRIMARY KEY: Unique identifier (legacy)
    task_id = Column(Integer, primary_key=True, index=True)
    
    # Legacy fields - kept for migration compatibility
    # See TaskTemplate and TaskInstance for new structure
    name = Column(String(200), nullable=False)
    task_type = Column(String(20), nullable=False)
    hours = Column(Float, nullable=False)
    domain_id = Column(Integer, ForeignKey("domains.domain_id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=False)
    program_section_id = Column(Integer, ForeignKey("program_sections.section_id"), nullable=True)
    semester = Column(String(20), nullable=False)
    academic_year = Column(String(10), nullable=False)
