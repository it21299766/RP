"""
TaskTemplate Service - Business Logic for Task Template Management

This service contains the business logic for task template operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for task templates - handles validation,
orchestration, and complex operations.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task_template import TaskTemplate
from app.schemas.task_template import TaskTemplateCreate, TaskTemplateUpdate
from app.repositories.task_template_repository import TaskTemplateRepository


class TaskTemplateService:
    """
    Service class for task template business logic.
    
    This class contains methods that implement business rules for task template operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_template(db: Session, data: TaskTemplateCreate) -> TaskTemplate:
        """
        Create a new task template.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema (TaskTemplateCreate)
        - Creates template object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Field types and constraints validated by Pydantic
        
        USE CASE: Admin creates a new reusable task template (e.g., "DBMS Lecture")
        
        Args:
            db: Database session
            data: TaskTemplateCreate schema with template information
        
        Returns:
            Created TaskTemplate object
        """
        # Convert schema to model object
        template = TaskTemplate(**data.dict())
        # Save to database via repository
        return TaskTemplateRepository.create(db, template)

    @staticmethod
    def get_template_list(db: Session, active_only: bool = False):
        """
        Get list of task templates.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve templates
        - Optionally filters by active status
        
        USE CASES:
        - Template listing page (all templates)
        - Dropdown for creating task instances (active_only=True)
        - Reports (all templates including inactive)
        
        Args:
            db: Database session
            active_only: If True, only return active templates
        
        Returns:
            List of TaskTemplate objects
        """
        # Simple delegation to repository
        # active_only filter passed through to repository
        return TaskTemplateRepository.get_all(db, active_only=active_only)

    @staticmethod
    def get_template(db: Session, template_id: int) -> TaskTemplate:
        """
        Get task template by ID.
        
        BUSINESS LOGIC:
        - Validates that template exists
        - Raises 404 error if not found (standard REST behavior)
        
        USE CASE: View template details, update template (need to get first)
        
        ERROR HANDLING:
        - Raises HTTPException with 404 if template not found
        - This is a business rule: "template must exist to view"
        
        Args:
            db: Database session
            template_id: ID of template to retrieve
        
        Returns:
            TaskTemplate object if found
        
        Raises:
            HTTPException: 404 if template not found
        """
        # Get template from database
        template = TaskTemplateRepository.get_by_id(db, template_id)
        
        # Business rule: Template must exist
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task template not found"
            )
        return template

    @staticmethod
    def update_template(db: Session, template_id: int, data: TaskTemplateUpdate) -> TaskTemplate:
        """
        Update an existing task template.
        
        BUSINESS LOGIC:
        1. Get template (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just default_hours)
        
        USE CASE: Update template information (name, hours, requirements, is_active)
        
        VALIDATION:
        - Template existence validated by get_template()
        - Field validation done by Pydantic schema (TaskTemplateUpdate)
        
        Args:
            db: Database session
            template_id: ID of template to update
            data: TaskTemplateUpdate schema with fields to update (only provided fields)
        
        Returns:
            Updated TaskTemplate object
        
        Raises:
            HTTPException: 404 if template not found
        """
        # STEP 1: Get template (validates existence)
        template = TaskTemplateService.get_template(db, template_id)
        
        # STEP 2: Update only provided fields (partial update)
        # exclude_unset=True means only update fields that were actually provided
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(template, key, value)  # template.name = value, etc.
        
        # STEP 3: Save changes to database
        return TaskTemplateRepository.update(db, template)

    @staticmethod
    def delete_template(db: Session, template_id: int):
        """
        Soft delete a task template.
        
        BUSINESS LOGIC:
        1. Get template (validates existence - raises 404 if not found)
        2. Soft delete (set is_active=False) via repository
        
        SOFT DELETE:
        - Sets is_active=False instead of deleting record
        - Preserves historical data (existing task instances still reference template)
        - Template doesn't appear in active-only lists
        - Can be reactivated later if needed
        
        USE CASE: Deactivate obsolete templates (course no longer taught)
        
        Args:
            db: Database session
            template_id: ID of template to delete
        
        Returns:
            TaskTemplate object with is_active=False
        
        Raises:
            HTTPException: 404 if template not found
        """
        # Get template (validates existence)
        template = TaskTemplateService.get_template(db, template_id)
        
        # Soft delete via repository (sets is_active=False)
        return TaskTemplateRepository.delete(db, template)
