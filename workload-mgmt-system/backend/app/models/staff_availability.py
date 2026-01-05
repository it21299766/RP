"""
StaffAvailability Model - Tracks Staff Leave and Unavailability

This model tracks periods when staff members are unavailable (on leave,
sick, sabbatical, etc.). Used by the optimization algorithm to avoid
assigning tasks during unavailable periods.

THINK OF IT AS: A calendar/leave management system for staff availability.
EXAMPLE: "Dr. Smith is on leave from Jan 15 to Jan 20, 2025"

WHY THIS TABLE?
- Prevents assigning tasks to unavailable staff
- GA algorithm respects availability constraints
- Tracks leave history for reporting
- Supports different types of unavailability (leave, sick, sabbatical)
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text
from app.database import Base


class StaffAvailability(Base):
    """
    StaffAvailability Model - Database table for staff availability periods.
    
    Each row represents one period of availability/unavailability for a staff member.
    Used by optimization algorithm and workload planning.
    
    RELATIONSHIP: Many Availability Records → One Staff (many-to-one)
    EXAMPLE: One staff member can have multiple leave periods throughout the year
    """
    __tablename__ = "staff_availability"

    # PRIMARY KEY: Unique identifier for each availability record
    # SIGNIFICANCE: Used to track, update, or delete specific availability records
    # USECASE: Primary key for availability operations
    id = Column(Integer, primary_key=True, index=True)
    
    # STAFF_ID: Which staff member this availability record belongs to
    # SIGNIFICANCE: Links availability to staff member
    # USECASE: 
    #   - Filter availability by staff
    #   - Check if staff is available for a task
    #   - Generate staff availability reports
    # RELATIONSHIP: Many Availability Records → One Staff (many-to-one)
    # EXAMPLE: Staff ID 5 has 3 availability records (different leave periods)
    staff_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)
    
    # START_DATE: When the availability period begins
    # SIGNIFICANCE: Start of the availability/unavailability period
    # USECASE: 
    #   - Check if task date falls within unavailable period
    #   - Filter availability by date range
    #   - Generate calendar views
    # FORMAT: Date (YYYY-MM-DD)
    # EXAMPLE: "2025-01-15" (January 15, 2025)
    # NOTE: Must be before or equal to end_date
    start_date = Column(Date, nullable=False)
    
    # END_DATE: When the availability period ends
    # SIGNIFICANCE: End of the availability/unavailability period
    # USECASE: 
    #   - Check if task date falls within unavailable period
    #   - Calculate duration of leave
    #   - Generate calendar views
    # FORMAT: Date (YYYY-MM-DD)
    # EXAMPLE: "2025-01-20" (January 20, 2025)
    # NOTE: Must be after or equal to start_date
    end_date = Column(Date, nullable=False)
    
    # AVAILABILITY_TYPE: Type of unavailability
    # SIGNIFICANCE: Categorizes the reason for unavailability
    # USECASE: 
    #   - Filter by type (leave, sick, sabbatical)
    #   - Generate reports by type
    #   - Understand availability patterns
    # VALUES: 
    #   - "leave": Regular/annual leave
    #   - "sick": Medical/sick leave
    #   - "sabbatical": Sabbatical leave (research/study)
    #   - "other": Other types of unavailability
    # NOTE: Used for reporting and analytics
    availability_type = Column(String(20), nullable=False)
    
    # REASON: Optional explanation for the unavailability
    # SIGNIFICANCE: Documents why staff is unavailable
    # USECASE: 
    #   - Documentation and audit trail
    #   - Understanding leave reasons
    #   - Communication and planning
    # EXAMPLES: "Annual leave", "Medical leave", "Research sabbatical", "Personal leave"
    # NOTE: Optional field for additional context
    reason = Column(Text, nullable=True)
    
    # IS_AVAILABLE: Whether staff is available during this period
    # SIGNIFICANCE: Flags availability vs. unavailability
    # USECASE: 
    #   - GA algorithm skips staff with is_available=False
    #   - Filter available vs. unavailable periods
    # VALUES: 
    #   - False: Staff is NOT available (on leave, sick, etc.)
    #   - True: Staff IS available (rare, but can mark availability windows)
    # DEFAULT: False (most records are for unavailability)
    # EXAMPLE: Leave period has is_available=False
    is_available = Column(Boolean, default=False, nullable=False)
    
    # STATUS: Approval status of the availability record
    # SIGNIFICANCE: Tracks approval workflow for leave requests
    # USECASE: 
    #   - Workflow management (pending → approved/rejected)
    #   - Filter by status
    #   - Only use approved availability in optimization
    # VALUES: 
    #   - "pending": Leave request submitted, awaiting approval
    #   - "approved": Leave request approved, staff is unavailable
    #   - "rejected": Leave request rejected, staff is available
    # DEFAULT: "approved" (assume approved unless specified)
    # NOTE: GA algorithm typically only respects "approved" unavailability
    status = Column(String(20), default="approved", nullable=False)
