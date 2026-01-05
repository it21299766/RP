"""
ModuleSection Service - Business Logic for Module Section Management

This service contains the business logic for module section operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for module sections - handles validation,
orchestration, and deletion checks.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.module_section import ModuleSection
from app.repositories.module_section_repository import ModuleSectionRepository
from app.repositories.task_repository import TaskRepository


class ModuleSectionService:
    """
    Service class for module section business logic.
    
    This class contains methods that implement business rules for module section operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_section(db: Session, data):
        """
        Create a new module section.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema
        - Creates section object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Module existence should be validated (enforced by foreign key)
        
        USE CASE: Admin creates a new module section (e.g., "DBMS Section A")
        
        Args:
            db: Database session
            data: Module section schema with section information
        
        Returns:
            Created ModuleSection object
        """
        # Convert schema to model object
        section = ModuleSection(**data.dict())
        # Save to database via repository
        return ModuleSectionRepository.create(db, section)

    @staticmethod
    def get_sections(db: Session):
        """
        Get list of all module sections.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all sections
        
        USE CASE: Display section list, generate reports
        
        Args:
            db: Database session
        
        Returns:
            List of all ModuleSection objects
        """
        # Simple delegation to repository
        return ModuleSectionRepository.get_all(db)

    @staticmethod
    def update_section(db: Session, section_id: int, data):
        """
        Update an existing module section.
        
        BUSINESS LOGIC:
        1. Get section (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        
        USE CASE: Update section information (student_count, section_code)
        
        VALIDATION:
        - Section existence validated by get_by_id()
        - Field validation done by Pydantic schema
        
        Args:
            db: Database session
            section_id: ID of section to update
            data: Update schema with fields to update (only provided fields)
        
        Returns:
            Updated ModuleSection object
        
        Raises:
            HTTPException: 404 if section not found
        """
        # Get section (validates existence)
        section = ModuleSectionRepository.get_by_id(db, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Module section not found")

        # Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(section, key, value)

        # Save changes directly (not using repository.update for consistency)
        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def delete_section(db: Session, section_id: int):
        """
        Delete a module section.
        
        BUSINESS LOGIC:
        1. Get section (validates existence - raises 404 if not found)
        2. Check if section has tasks (business rule: cannot delete section with tasks)
        3. Delete if no tasks, raise error if tasks exist
        
        BUSINESS RULE: Cannot delete section if it has assigned tasks
        - Prevents orphaned tasks (tasks without section)
        - Maintains referential integrity
        - Requires deleting/reassigning tasks first
        
        NOTE: Uses legacy TaskRepository.get_by_module_section (method may not exist in repository)
        
        USE CASE: Remove module section (only if no tasks exist)
        
        ERROR HANDLING:
        - Raises 404 if section not found
        - Raises 400 if section has tasks
        
        Args:
            db: Database session
            section_id: ID of section to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if section not found
            HTTPException: 400 if section has tasks
        """
        # Get section (validates existence)
        section = ModuleSectionRepository.get_by_id(db, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Module section not found")

        # Business rule: Cannot delete section if it has assigned tasks
        # NOTE: This method may need to be implemented in TaskRepository
        tasks = TaskRepository.get_by_module_section(db, section_id)
        if tasks:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete module section with assigned tasks"
            )

        # Delete from database (only if no tasks)
        ModuleSectionRepository.delete(db, section)
