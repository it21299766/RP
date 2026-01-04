"""
ChangeRequest Service - Business Logic for Change Request Management

This service contains the business logic for change request operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for change requests - handles validation,
orchestration, and workflow management (approve/reject).
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.change_request import ChangeRequest
from app.repositories.change_request_repository import ChangeRequestRepository
from app.repositories.assignment_repository import AssignmentRepository


class ChangeRequestService:
    """
    Service class for change request business logic.
    
    This class contains methods that implement business rules for change request operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def get_all(db: Session):
        """Get all change requests. ADMIN only."""
        return ChangeRequestRepository.get_all(db)
    
    @staticmethod
    def get_by_staff(db: Session, staff_id: int):
        """Get all change requests for a specific staff member."""
        return ChangeRequestRepository.get_by_staff_id(db, staff_id)
    
    @staticmethod
    def create_request(db: Session, data):
        """
        Create a new change request.
        
        BUSINESS LOGIC:
        1. Validate assignment exists (cannot request change for non-existent assignment)
        2. Create change request object
        3. Save to database
        
        VALIDATION RULES:
        - Assignment must exist (404 if not found)
        - Reason is required (validated by schema)
        
        USE CASE: Staff member requests a change to their assignment
        
        WORKFLOW: Request starts with status="PENDING"
        
        Args:
            db: Database session
            data: Change request schema with assignment_id, requested_by_staff_id, reason
        
        Returns:
            Created ChangeRequest object
        
        Raises:
            HTTPException: 404 if assignment not found
        """
        # STEP 1: Validate assignment exists
        assignment = AssignmentRepository.get_by_id(db, data.assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # STEP 2: Create change request object
        request = ChangeRequest(
            assignment_id=data.assignment_id,
            requested_by_staff_id=data.requested_by_staff_id,
            reason=data.reason
        )
        # STEP 3: Save to database (status defaults to "PENDING")
        return ChangeRequestRepository.create(db, request)

    @staticmethod
    def approve_request(db: Session, request_id: int, admin_comment: str):
        """
        Approve a change request.
        
        BUSINESS LOGIC:
        1. Get request (validates existence - raises 404 if not found)
        2. Update status to "APPROVED"
        3. Set admin comment (optional explanation)
        4. Save changes
        
        WORKFLOW: Changes request status from "PENDING" to "APPROVED"
        
        USE CASE: Admin approves a staff request to change assignment
        
        NOTE: This only updates the request status. Actual assignment change
        should be handled separately (e.g., update assignment, create new assignment).
        
        Args:
            db: Database session
            request_id: ID of change request to approve
            admin_comment: Optional comment from admin
        
        Returns:
            Updated ChangeRequest object with status="APPROVED"
        
        Raises:
            HTTPException: 404 if request not found
        """
        # Get request (validates existence)
        req = ChangeRequestRepository.get_by_id(db, request_id)
        if not req:
            raise HTTPException(status_code=404, detail="Change request not found")

        # Update status to approved
        req.status = "APPROVED"
        # Set admin comment (explanation/notes)
        req.admin_comment = admin_comment
        
        # Save changes directly (not using repository.update for consistency)
        db.commit()
        db.refresh(req)
        return req

    @staticmethod
    def reject_request(db: Session, request_id: int, admin_comment: str):
        """
        Reject a change request.
        
        BUSINESS LOGIC:
        1. Get request (validates existence - raises 404 if not found)
        2. Update status to "REJECTED"
        3. Set admin comment (should explain why rejected)
        4. Save changes
        
        WORKFLOW: Changes request status from "PENDING" to "REJECTED"
        
        USE CASE: Admin rejects a staff request to change assignment
        
        NOTE: Admin comment should explain rejection reason for transparency.
        
        Args:
            db: Database session
            request_id: ID of change request to reject
            admin_comment: Comment from admin (should explain rejection reason)
        
        Returns:
            Updated ChangeRequest object with status="REJECTED"
        
        Raises:
            HTTPException: 404 if request not found
        """
        # Get request (validates existence)
        req = ChangeRequestRepository.get_by_id(db, request_id)
        if not req:
            raise HTTPException(status_code=404, detail="Change request not found")

        # Update status to rejected
        req.status = "REJECTED"
        # Set admin comment (should explain why rejected)
        req.admin_comment = admin_comment
        
        # Save changes directly (not using repository.update for consistency)
        db.commit()
        db.refresh(req)
        return req
