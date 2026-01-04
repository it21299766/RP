"""
Assignment Service - Business Logic for Task Assignments

This service contains the business logic for assignment operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for assignments - handles validation,
constraint checking, and complex operations that require multiple steps.

WHY SERVICE LAYER?
- Business logic separate from database access
- Validation and error handling
- Complex operations (multiple database calls, constraint checking)
- Coordinates between repositories and schemas
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.staff_repository import StaffRepository
from app.repositories.task_repository import TaskRepository


class AssignmentService:
    """
    Service class for assignment business logic.
    
    This class contains methods that implement business rules for assignment operations.
    It uses repositories to access the database and handles validation/errors.
    """

    @staticmethod
    def create_assignment(db: Session, data):
        """
        Create a new assignment with constraint validation.
        
        BUSINESS LOGIC:
        This method implements the assignment creation workflow:
        1. Validate staff and task exist
        2. Check hard constraints (qualification requirement)
        3. Check teaching constraints (role, department, specialization) if teaching task
        4. Validate override reason if override is requested
        5. Create and save assignment
        
        HARD CONSTRAINTS (never overridden):
        - Qualification: Staff qualification must meet task requirement (PhD > MSc > BSc)
        
        TEACHING CONSTRAINTS (unless override):
        - Role: Only ACADEMIC staff can teach
        - Department: Staff department must match task department
        - Specialization: Staff specialization must match task required specialization
        
        OVERRIDE:
        - Admin can override teaching constraints with a reason
        - Override requires override_reason to be provided
        
        Args:
            db: Database session
            data: Assignment data with staff_id, task_id, override flag, etc.
        
        Returns:
            Created Assignment object
        
        Raises:
            HTTPException: 404 if staff or task not found
            HTTPException: 400 if constraints not met or override reason missing
        """
        staff = StaffRepository.get_by_id(db, data.staff_id)
        task = TaskRepository.get_by_id(db, data.task_id)

        if not staff or not task:
            raise HTTPException(status_code=404, detail="Staff or Task not found")

        # Hard qualification check (never overridden)
        if staff.qualification < task.required_qualification:
            raise HTTPException(status_code=400, detail="Qualification requirement not met")

        if task.category == "Teaching" and not data.override:
            if staff.role != "ACADEMIC":
                raise HTTPException(status_code=400, detail="Only academic staff can teach")

            if staff.department != task.department:
                raise HTTPException(status_code=400, detail="Department mismatch")

            if staff.specialty != task.required_specialty:
                raise HTTPException(status_code=400, detail="Specialty mismatch")

        if data.override and not data.override_reason:
            raise HTTPException(status_code=400, detail="Override reason required")

        assignment = Assignment(
            staff_id=data.staff_id,
            task_id=data.task_id,
            override=data.override,
            override_reason=data.override_reason,
            assigned_by="ADMIN" if data.override else "SYSTEM"
        )

        return AssignmentRepository.create(db, assignment)

    @staticmethod
    def update_assignment(db, assignment_id: int, data):
        """
        Update an existing assignment.
        
        BUSINESS LOGIC:
        1. Get assignment (validates existence - raises 404 if not found)
        2. Validate override reason if override is enabled
        3. Update only fields that are provided (partial update)
        4. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just status)
        
        VALIDATION:
        - Assignment existence validated
        - Override reason required if override flag is set
        
        Args:
            db: Database session
            assignment_id: ID of assignment to update
            data: Assignment data with fields to update (only provided fields)
        
        Returns:
            Updated Assignment object
        
        Raises:
            HTTPException: 404 if assignment not found
            HTTPException: 400 if override reason missing when override enabled
        """
        assignment = AssignmentRepository.get_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Validate override reason if override is enabled
        if data.override and not data.override_reason:
            raise HTTPException(
                status_code=400,
                detail="Override reason required when override is enabled"
            )

        # Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(assignment, key, value)

        # Save changes
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def delete_assignment(db, assignment_id: int):
        """
        Delete an assignment.
        
        BUSINESS LOGIC:
        1. Get assignment (validates existence - raises 404 if not found)
        2. Check if assignment is completed (cannot delete completed assignments)
        3. Delete from database
        
        BUSINESS RULE: Completed assignments cannot be deleted
        - Prevents accidental deletion of historical data
        - Maintains data integrity for completed work
        
        Args:
            db: Database session
            assignment_id: ID of assignment to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if assignment not found
            HTTPException: 400 if assignment is completed
        """
        assignment = AssignmentRepository.get_by_id(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Business rule: Cannot delete completed assignments
        if assignment.status == "completed":
            raise HTTPException(
                status_code=400,
                detail="Completed assignments cannot be deleted"
            )

        # Delete assignment
        AssignmentRepository.delete(db, assignment)
