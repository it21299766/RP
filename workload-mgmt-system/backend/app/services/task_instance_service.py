"""
TaskInstance Service - Business Logic for Task Instance Management

This service contains the business logic for task instance operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for task instances - handles validation,
orchestration, hierarchy validation, and workflow management.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task_instance import TaskInstance
from app.models.task_template import TaskTemplate
from app.models.domain import Domain
from app.models.program import Program
from app.schemas.task_instance import TaskInstanceCreate, TaskInstanceUpdate
from app.repositories.task_instance_repository import TaskInstanceRepository
from app.repositories.task_template_repository import TaskTemplateRepository


class TaskInstanceService:
    """
    Service class for task instance business logic.
    
    This class contains methods that implement business rules for task instance operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_instance(db: Session, data: TaskInstanceCreate) -> TaskInstance:
        """
        Create a new task instance with validation.
        
        BUSINESS LOGIC:
        This method implements the task instance creation workflow with comprehensive validation:
        1. Validate task template exists and is active
        2. Validate domain exists
        3. Validate program exists
        4. Validate program belongs to domain (hierarchy integrity)
        5. Create instance if all validations pass
        
        VALIDATION RULES:
        - Template must exist (404 if not found)
        - Template must be active (400 if inactive - cannot create instances from inactive templates)
        - Domain must exist (404 if not found)
        - Program must exist (404 if not found)
        - Program must belong to specified domain (400 if mismatch - maintains hierarchy)
        
        WHY VALIDATE HIERARCHY:
        - Ensures data integrity (Domain → Program → TaskInstance hierarchy)
        - Prevents creating instances with invalid relationships
        - Maintains referential integrity at application level
        
        USE CASE: Admin creates a specific task instance for a semester/program
        
        Args:
            db: Database session
            data: TaskInstanceCreate schema with instance information
        
        Returns:
            Created TaskInstance object
        
        Raises:
            HTTPException: 404 if template/domain/program not found
            HTTPException: 400 if template inactive or hierarchy mismatch
        """
        # STEP 1: Validate task template exists
        template = TaskTemplateRepository.get_by_id(db, data.task_template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task template not found"
            )
        
        # STEP 2: Validate template is active (business rule: cannot create instances from inactive templates)
        if not template.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create instance from inactive template"
            )
        
        # STEP 3: Validate domain exists
        domain = db.query(Domain).filter(Domain.domain_id == data.domain_id).first()
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domain not found"
            )
        
        # STEP 4: Validate program exists
        program = db.query(Program).filter(Program.program_id == data.program_id).first()
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )
        
        # STEP 5: Validate program belongs to domain (hierarchy integrity)
        # Business rule: Program must belong to the specified domain
        if program.domain_id != data.domain_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Program does not belong to specified domain"
            )
        
        # STEP 6: All validations passed - create instance
        instance = TaskInstance(**data.dict())
        return TaskInstanceRepository.create(db, instance)

    @staticmethod
    def get_instance_list(
        db: Session,
        status: str = None,
        semester: str = None,
        academic_year: str = None
    ):
        """
        Get list of task instances with optional filters.
        
        BUSINESS LOGIC:
        - No business rules - just retrieves instances with optional filtering
        - Filters passed through to repository
        
        USE CASES:
        - Instance listing page (all instances)
        - Filter by status (draft, approved, completed)
        - Filter by semester (e.g., "2025S1")
        - Filter by academic year (e.g., "2024-2025")
        - Combined filters (e.g., approved instances for Fall 2025)
        
        Args:
            db: Database session
            status: Optional status filter (draft, approved, completed)
            semester: Optional semester filter (e.g., "2025S1")
            academic_year: Optional academic year filter (e.g., "2024-2025")
        
        Returns:
            List of TaskInstance objects matching filters
        """
        # Delegate to repository with filters
        return TaskInstanceRepository.get_all(
            db,
            status=status,
            semester=semester,
            academic_year=academic_year
        )

    @staticmethod
    def get_instance(db: Session, instance_id: int) -> TaskInstance:
        """
        Get task instance by ID.
        
        BUSINESS LOGIC:
        - Validates that instance exists
        - Raises 404 error if not found (standard REST behavior)
        
        USE CASE: View instance details, update instance (need to get first)
        
        ERROR HANDLING:
        - Raises HTTPException with 404 if instance not found
        - This is a business rule: "instance must exist to view"
        
        Args:
            db: Database session
            instance_id: ID of instance to retrieve
        
        Returns:
            TaskInstance object if found
        
        Raises:
            HTTPException: 404 if instance not found
        """
        # Get instance from database
        instance = TaskInstanceRepository.get_by_id(db, instance_id)
        
        # Business rule: Instance must exist
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task instance not found"
            )
        return instance

    @staticmethod
    def get_approved_instances(db: Session):
        """
        Get all approved task instances (for GA optimization).
        
        BUSINESS LOGIC:
        - Returns only instances with status="approved"
        - No additional business rules
        
        USE CASE: GA optimization algorithm (needs approved instances to assign)
        
        WHY APPROVED ONLY:
        - Draft instances are not yet finalized (shouldn't be assigned)
        - Completed instances are already done (shouldn't be assigned)
        - Only approved instances need assignment/optimization
        
        Args:
            db: Database session
        
        Returns:
            List of approved TaskInstance objects (status="approved")
        """
        # Delegate to repository (get_approved method)
        return TaskInstanceRepository.get_approved(db)

    @staticmethod
    def update_instance(db: Session, instance_id: int, data: TaskInstanceUpdate) -> TaskInstance:
        """
        Update an existing task instance.
        
        BUSINESS LOGIC:
        1. Get instance (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just effective_hours)
        
        USE CASE: Update instance information (hours, status, semester, etc.)
        
        VALIDATION:
        - Instance existence validated by get_instance()
        - Field validation done by Pydantic schema (TaskInstanceUpdate)
        
        Args:
            db: Database session
            instance_id: ID of instance to update
            data: TaskInstanceUpdate schema with fields to update (only provided fields)
        
        Returns:
            Updated TaskInstance object
        
        Raises:
            HTTPException: 404 if instance not found
        """
        # STEP 1: Get instance (validates existence)
        instance = TaskInstanceService.get_instance(db, instance_id)
        
        # STEP 2: Update only provided fields (partial update)
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(instance, key, value)  # instance.effective_hours = value, etc.
        
        # STEP 3: Save changes to database
        return TaskInstanceRepository.update(db, instance)

    @staticmethod
    def delete_instance(db: Session, instance_id: int):
        """
        Delete a task instance (only if status is draft).
        
        BUSINESS LOGIC:
        1. Get instance (validates existence - raises 404 if not found)
        2. Check if status is "draft" (business rule: can only delete draft instances)
        3. Delete if draft, raise error if not
        
        BUSINESS RULE: Can only delete instances with "draft" status
        - Draft instances: Not yet finalized, safe to delete
        - Approved instances: Already approved, should not be deleted (use workflow)
        - Completed instances: Already done, should not be deleted (historical record)
        
        USE CASE: Remove draft instances that were created incorrectly
        
        ERROR HANDLING:
        - Raises 404 if instance not found
        - Raises 400 if status is not "draft"
        
        Args:
            db: Database session
            instance_id: ID of instance to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if instance not found
            HTTPException: 400 if status is not "draft"
        """
        # Get instance (validates existence)
        instance = TaskInstanceService.get_instance(db, instance_id)
        
        # Business rule: Can only delete draft instances
        if instance.status != "draft":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only delete task instances with draft status"
            )
        
        # Delete from database (hard delete for draft instances only)
        return TaskInstanceRepository.delete(db, instance)

    @staticmethod
    def approve_instance(db: Session, instance_id: int) -> TaskInstance:
        """
        Approve a task instance (change status to approved).
        
        BUSINESS LOGIC:
        1. Get instance (validates existence - raises 404 if not found)
        2. Check if status is "completed" (business rule: cannot approve completed instances)
        3. Set status to "approved"
        4. Save changes
        
        BUSINESS RULE: Cannot approve completed instances
        - Completed instances are already finished
        - Workflow: draft → approved → completed (cannot go backwards)
        
        WORKFLOW: This is part of the task instance workflow
        - draft: Just created, not yet approved
        - approved: Approved, ready for assignment/optimization
        - completed: Task has been completed
        
        USE CASE: Admin approves a draft instance so it can be assigned to staff
        
        ERROR HANDLING:
        - Raises 404 if instance not found
        - Raises 400 if status is "completed"
        
        Args:
            db: Database session
            instance_id: ID of instance to approve
        
        Returns:
            Updated TaskInstance object with status="approved"
        
        Raises:
            HTTPException: 404 if instance not found
            HTTPException: 400 if status is "completed"
        """
        # Get instance (validates existence)
        instance = TaskInstanceService.get_instance(db, instance_id)
        
        # Business rule: Cannot approve completed instances (workflow constraint)
        if instance.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot approve completed task instance"
            )
        
        # Update status to approved
        instance.status = "approved"
        return TaskInstanceRepository.update(db, instance)
