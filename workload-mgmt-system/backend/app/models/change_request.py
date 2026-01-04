"""
ChangeRequest Model - Staff Requests for Assignment Changes

This model represents requests from staff members to change their task assignments.
Staff can request changes (e.g., swap assignments, remove assignment) which
administrators can approve or reject.

THINK OF IT AS: A "request system" where staff submit requests and admins review them.
EXAMPLE: Staff requests to swap "DBMS Lecture" assignment with another staff member.

WORKFLOW: Staff creates request → Admin reviews → Approved/Rejected
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ChangeRequest(Base):
    """
    ChangeRequest Model - Database table for assignment change requests.
    
    Each row represents one change request from a staff member.
    
    RELATIONSHIPS:
    - Many Change Requests → One Assignment (many-to-one)
    - Many Change Requests → One Staff (many-to-one via requested_by_staff_id)
    
    WORKFLOW: PENDING → APPROVED/REJECTED
    """
    __tablename__ = "change_requests"

    # PRIMARY KEY: Unique identifier for each change request
    # SIGNIFICANCE: Used to track, update, or delete requests
    # USECASE: Primary key for request operations
    request_id = Column(Integer, primary_key=True, index=True)

    # ASSIGNMENT_ID: Which assignment the request is about
    # SIGNIFICANCE: Links request to the specific assignment to be changed
    # USECASE: 
    #   - Get assignment details (what task, which staff)
    #   - Update assignment if approved
    #   - Track which assignments have change requests
    # RELATIONSHIP: Many Change Requests → One Assignment (many-to-one)
    # NOTE: One assignment could have multiple change requests (e.g., multiple staff want it)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)

    # REQUESTED_BY_STAFF_ID: Which staff member made this request
    # SIGNIFICANCE: Identifies who is requesting the change
    # USECASE: 
    #   - Filter requests by staff member
    #   - Display requestor information
    #   - Track request history per staff
    # RELATIONSHIP: Many Change Requests → One Staff (many-to-one)
    # NOTE: Staff requesting change may or may not be the assigned staff
    requested_by_staff_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=False)

    # REASON: Explanation for why the change is requested
    # SIGNIFICANCE: Documents the rationale for the request
    # USECASE: 
    #   - Admin reviews reason before approving/rejecting
    #   - Audit trail and documentation
    #   - Understanding request context
    # EXAMPLES: "Schedule conflict", "Overloaded", "Prefer different course", "Personal reason"
    # NOTE: Required field - staff must provide a reason
    reason = Column(String(255), nullable=False)

    # STATUS: Current status of the request
    # SIGNIFICANCE: Tracks request workflow state
    # VALUES: 
    #   - "PENDING": Request submitted, awaiting admin review
    #   - "APPROVED": Request approved, assignment changed
    #   - "REJECTED": Request rejected, assignment unchanged
    # USECASE: 
    #   - Filter requests by status
    #   - Display request status to staff
    #   - Track workflow progression
    # WORKFLOW: PENDING → APPROVED/REJECTED
    # DEFAULT: "PENDING" (new requests start as pending)
    status = Column(String(20), default="PENDING")
    
    # ADMIN_COMMENT: Optional comment from admin when reviewing request
    # SIGNIFICANCE: Allows admin to provide feedback or explanation
    # USECASE: 
    #   - Explain rejection reason to staff
    #   - Provide approval notes
    #   - Internal documentation
    # EXAMPLES: "Approved - workload balanced", "Rejected - no suitable replacement"
    # NOTE: Optional field - only filled when admin reviews request
    admin_comment = Column(String(255), nullable=True)
