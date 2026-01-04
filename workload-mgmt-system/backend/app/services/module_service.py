"""
Module Service - Business Logic for Module Management

This service contains the business logic for module operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for modules - handles validation,
orchestration, and deletion checks.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.module import Module
from app.repositories.module_repository import ModuleRepository
from app.repositories.task_repository import TaskRepository


class ModuleService:
    """
    Service class for module business logic.
    
    This class contains methods that implement business rules for module operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_module(db: Session, data):
        """
        Create a new module.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema
        - Creates module object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Program existence should be validated (enforced by foreign key)
        - Code uniqueness enforced by database constraint
        
        USE CASE: Admin creates a new module/course (e.g., "Database Management Systems")
        
        Args:
            db: Database session
            data: Module schema with module information
        
        Returns:
            Created Module object
        """
        # Convert schema to model object
        module = Module(**data.dict())
        # Save to database via repository
        return ModuleRepository.create(db, module)

    @staticmethod
    def get_modules(db: Session):
        """
        Get list of all modules.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all modules
        
        USE CASE: Display module list, populate dropdowns, generate reports
        
        Args:
            db: Database session
        
        Returns:
            List of all Module objects
        """
        # Simple delegation to repository
        return ModuleRepository.get_all(db)

    @staticmethod
    def update_module(db: Session, module_id: int, data):
        """
        Update an existing module.
        
        BUSINESS LOGIC:
        1. Get module (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        
        USE CASE: Update module information (name, code, credits, semester)
        
        VALIDATION:
        - Module existence validated by get_by_id()
        - Field validation done by Pydantic schema
        
        Args:
            db: Database session
            module_id: ID of module to update
            data: Update schema with fields to update (only provided fields)
        
        Returns:
            Updated Module object
        
        Raises:
            HTTPException: 404 if module not found
        """
        # Get module (validates existence)
        module = ModuleRepository.get_by_id(db, module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        # Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(module, key, value)

        # Save changes directly (not using repository.update for consistency)
        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def delete_module(db: Session, module_id: int):
        """
        Delete a module.
        
        BUSINESS LOGIC:
        1. Get module (validates existence - raises 404 if not found)
        2. Check if module has tasks (business rule: cannot delete module with tasks)
        3. Delete if no tasks, raise error if tasks exist
        
        BUSINESS RULE: Cannot delete module if it has assigned tasks
        - Prevents orphaned tasks (tasks without module)
        - Maintains referential integrity
        - Requires deleting/reassigning tasks first
        
        NOTE: Uses legacy TaskRepository.get_by_module (method may not exist in repository)
        
        USE CASE: Remove module (only if no tasks exist)
        
        ERROR HANDLING:
        - Raises 404 if module not found
        - Raises 400 if module has tasks
        
        Args:
            db: Database session
            module_id: ID of module to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if module not found
            HTTPException: 400 if module has tasks
        """
        # Get module (validates existence)
        module = ModuleRepository.get_by_id(db, module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        # Business rule: Cannot delete module if it has assigned tasks
        # NOTE: This method may need to be implemented in TaskRepository
        tasks = TaskRepository.get_by_module(db, module_id)
        if tasks:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete module with assigned tasks"
            )

        # Delete from database (only if no tasks)
        ModuleRepository.delete(db, module)
