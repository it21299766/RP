"""
Assignment Model - Links Staff to Task Instances

This model represents the actual assignment of a staff member to a task instance.
It's the "who does what" relationship in the system.

THINK OF IT AS: A record showing "Staff X is assigned to teach Task Y"

RELATIONSHIPS:
- Assignment → Staff (many-to-one): One staff can have many assignments
- Assignment → TaskInstance (many-to-one): One task instance assigned to one staff
- Assignment can be created by GA algorithm or manually by admin
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base


class Assignment(Base):
    """
    Assignment Model - Database table linking staff to task instances.
    
    Each row represents one assignment: one staff member assigned to one task instance.
    This is the core relationship that determines workload distribution.
    
    EXAMPLE: Staff ID 5 assigned to TaskInstance ID 12 (DBMS Lecture for BSCS-A)
    """
    __tablename__ = "assignments"

    # PRIMARY KEY: Unique identifier for each assignment
    # SIGNIFICANCE: Used to track, update, or delete specific assignments
    # USECASE: Primary key for assignment operations (edit, delete, view details)
    assignment_id = Column(Integer, primary_key=True, index=True)

    # STAFF_ID: Which staff member is assigned
    # SIGNIFICANCE: Links assignment to staff member (who is doing the work)
    # USECASE: 
    #   - Calculate staff workload (sum of all their assignments)
    #   - Filter assignments by staff member
    #   - Generate staff workload reports
    # RELATIONSHIP: Many Assignments → One Staff (many-to-one)
    # EXAMPLE: Staff ID 5 has 3 assignments = 3 tasks assigned to them
    staff_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)
    
    # TASK_INSTANCE_ID: Which task instance is assigned
    # SIGNIFICANCE: Links assignment to specific task (what work is being done)
    # USECASE:
    #   - Get task details (hours, requirements, program, semester)
    #   - Track which tasks are assigned and which are unassigned
    #   - Generate task assignment reports
    # RELATIONSHIP: Many Assignments → One TaskInstance (many-to-one)
    # NOTE: Currently one task instance = one staff (could be extended for team teaching)
    task_instance_id = Column(Integer, ForeignKey("task_instances.id"), nullable=False)
    
    # TASK_ID: Legacy field - kept for backward compatibility during migration
    # SIGNIFICANCE: Old system used task_id, new system uses task_instance_id
    # USECASE: Migration support, backward compatibility
    # STATUS: Deprecated - use task_instance_id instead
    # NOTE: Can be NULL - not used in new system
    task_id = Column(Integer, nullable=True)

    # ASSIGNED_BY: Who created this assignment
    # SIGNIFICANCE: Tracks assignment source (system vs. manual)
    # VALUES: 
    #   - "SYSTEM": Created by GA algorithm
    #   - "ADMIN": Created manually by administrator
    # USECASE: 
    #   - Audit trail (who assigned what)
    #   - Filter system vs. manual assignments
    #   - Understand assignment source for reporting
    # NOTE: System assignments can be overridden by admin
    assigned_by = Column(String(20), default="SYSTEM")

    # OVERRIDE: Whether this assignment overrides a system recommendation
    # SIGNIFICANCE: Flags manual changes to system-generated assignments
    # USECASE: 
    #   - Track when admin changes system assignments
    #   - Generate reports on override frequency
    #   - Understand system vs. manual assignment patterns
    # EXAMPLE: GA assigns Task A to Staff 1, admin overrides to Staff 2 (override=True)
    override = Column(Boolean, default=False)

    # OVERRIDE_REASON: Explanation for why assignment was overridden
    # SIGNIFICANCE: Documents why manual change was made
    # USECASE: 
    #   - Audit trail for manual changes
    #   - Understanding assignment decisions
    #   - Training and documentation
    # EXAMPLES: "Staff requested change", "Balance workload", "Expertise match"
    # NOTE: Only relevant if override=True
    override_reason = Column(String(255), nullable=True)

    # STATUS: Current status of the assignment
    # SIGNIFICANCE: Tracks assignment lifecycle
    # VALUES: 
    #   - "assigned": Task is assigned but not yet completed
    #   - "completed": Task has been completed
    # USECASE: 
    #   - Track completion status
    #   - Filter active vs. completed assignments
    #   - Generate workload reports (only count "assigned" tasks)
    # WORKFLOW: assigned → completed
    status = Column(String(20), default="assigned")
