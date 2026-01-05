"""
DesignationWorkloadPolicy Model - Workload Limits by Designation

This model defines workload limits (maximum hours) for each staff designation.
It replaces the hardcoded max_hours field in the staff table, allowing
flexible policy management.

THINK OF IT AS: A policy table that says "Professors can work X hours,
Senior Lecturers can work Y hours", etc.

WHY SEPARATE TABLE?
- Flexible: Change limits without updating all staff records
- Centralized: One place to manage all workload policies
- Historical: Can track policy changes over time
- Scalable: Easy to add new designations
"""

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class DesignationWorkloadPolicy(Base):
    """
    DesignationWorkloadPolicy Model - Database table for workload limits by designation.
    
    Each row defines the workload limits for one designation (e.g., "Professor", "Lecturer").
    Staff members with a specific designation get their max hours from this table.
    
    RELATIONSHIP: One Policy → Many Staff (one-to-many via designation string)
    EXAMPLE: "Professor" policy applies to all staff with designation="Professor"
    """
    __tablename__ = "designation_workload_policies"

    # PRIMARY KEY: Unique identifier for each policy
    # SIGNIFICANCE: Used to reference specific policies
    # USECASE: Primary key for policy operations
    id = Column(Integer, primary_key=True, index=True)
    
    # DESIGNATION: Staff designation this policy applies to
    # SIGNIFICANCE: Links policy to staff designation (e.g., "Professor", "Lecturer")
    # USECASE: Look up max hours for a staff member based on their designation
    # EXAMPLES: "Professor", "Associate Professor", "Senior Lecturer I", 
    #           "Senior Lecturer II", "Lecturer", "Head of Department"
    # UNIQUE: Each designation should have only one policy
    # NOTE: Must match designation values in staff table
    designation = Column(String(50), nullable=False, unique=True)
    
    # MAX_HOURS_PER_WEEK: Maximum teaching hours allowed per week
    # SIGNIFICANCE: Hard limit - staff cannot be assigned more than this
    # USECASE: 
    #   - GA algorithm uses this to prevent overloading
    #   - Workload reports show if staff is over limit
    #   - Used to calculate workload balance
    # EXAMPLE: Professors might have 15 hours, Lecturers might have 24 hours
    # NOTE: Different designations have different limits (professors typically less teaching)
    max_hours_per_week = Column(Float, nullable=False)
    
    # MIN_HOURS_PER_WEEK: Optional minimum hours required
    # SIGNIFICANCE: Soft guideline for minimum workload (optional)
    # USECASE: 
    #   - Ensure staff have minimum teaching load
    #   - Balance workload distribution
    #   - Fairness in assignment
    # NOTE: Can be NULL if no minimum required
    # EXAMPLE: Full-time lecturers might have minimum 18 hours
    min_hours_per_week = Column(Float, nullable=True)
    
    # DESCRIPTION: Explanation of the policy
    # SIGNIFICANCE: Documents why these limits exist
    # USECASE: 
    #   - Documentation and audit trail
    #   - Understanding policy rationale
    #   - Training and reference
    # EXAMPLES: "Professors have reduced teaching load to focus on research"
    # NOTE: Optional field for documentation purposes
    description = Column(String(255), nullable=True)
