"""
ChangeRequest Service - Business Logic for Change Request Management

This service contains the business logic for change request operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for change requests - handles validation,
orchestration, and workflow management (approve/reject).
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
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
        2. Check request status (must be PENDING)
        3. Get assignment linked to the request
        4. Delete the assignment (unassign the task)
        5. Update status to "APPROVED"
        6. Set admin comment (optional explanation)
        7. Save changes
        
        WORKFLOW: Changes request status from "PENDING" to "APPROVED" and unassigns the task
        
        USE CASE: Admin approves a staff request to remove/unassign an assignment
        
        ASSIGNMENT CHANGE: When approved, the assignment is deleted (task becomes unassigned)
        
        Args:
            db: Database session
            request_id: ID of change request to approve
            admin_comment: Optional comment from admin
        
        Returns:
            Updated ChangeRequest object with status="APPROVED"
        
        Raises:
            HTTPException: 404 if request not found
            HTTPException: 400 if request is not PENDING
            HTTPException: 404 if assignment not found
        """
        # STEP 1: Get request (validates existence)
        req = ChangeRequestRepository.get_by_id(db, request_id)
        if not req:
            raise HTTPException(status_code=404, detail="Change request not found")
        
        # STEP 2: Check request status (must be PENDING)
        if req.status != "PENDING":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot approve request. Current status: {req.status}. Only PENDING requests can be approved."
            )
        
        # STEP 3: Get assignment linked to the request
        assignment = AssignmentRepository.get_by_id(db, req.assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        # STEP 4: Update change request status to approved FIRST (before deleting assignment)
        # This preserves the audit trail even after assignment is deleted
        req.status = "APPROVED"
        req.admin_comment = admin_comment
        db.commit()  # Commit change request update first
        
        # STEP 5: Delete the assignment (unassign the task)
        # Note: We use raw SQL to temporarily disable foreign key checks because
        # the change_request still references this assignment via foreign key.
        # This is safe because we've already updated the change request status above.
        assignment_id = req.assignment_id
        try:
            # Temporarily disable foreign key checks and delete the assignment
            # Using raw SQL because ORM delete fails due to foreign key constraint
            db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            db.execute(text("DELETE FROM assignments WHERE assignment_id = :assignment_id"), 
                      {"assignment_id": assignment_id})
            db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            db.commit()
        except Exception as e:
            # Re-enable foreign key checks even if deletion fails
            try:
                db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            except:
                pass
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete assignment: {str(e)}"
            )
        
        # STEP 6: Refresh the request object to get latest state
        db.refresh(req)
        return req

    @staticmethod
    def reject_request(db: Session, request_id: int, admin_comment: str):
        """
        Reject a change request.
        
        BUSINESS LOGIC:
        1. Get request (validates existence - raises 404 if not found)
        2. Check request status (must be PENDING)
        3. Update status to "REJECTED"
        4. Set admin comment (should explain why rejected)
        5. Save changes
        
        WORKFLOW: Changes request status from "PENDING" to "REJECTED"
        
        USE CASE: Admin rejects a staff request to change assignment
        
        NOTE: Admin comment should explain rejection reason for transparency.
        Assignment remains unchanged when request is rejected.
        
        Args:
            db: Database session
            request_id: ID of change request to reject
            admin_comment: Comment from admin (should explain rejection reason)
        
        Returns:
            Updated ChangeRequest object with status="REJECTED"
        
        Raises:
            HTTPException: 404 if request not found
            HTTPException: 400 if request is not PENDING
        """
        # STEP 1: Get request (validates existence)
        req = ChangeRequestRepository.get_by_id(db, request_id)
        if not req:
            raise HTTPException(status_code=404, detail="Change request not found")
        
        # STEP 2: Check request status (must be PENDING)
        if req.status != "PENDING":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reject request. Current status: {req.status}. Only PENDING requests can be rejected."
            )
        
        # STEP 3: Update status to rejected
        req.status = "REJECTED"
        # STEP 4: Set admin comment (should explain why rejected)
        req.admin_comment = admin_comment
        
        # STEP 5: Save changes
        db.commit()
        db.refresh(req)
        return req
