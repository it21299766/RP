"""
ProgramSection Service - Business Logic for Program Section Management

This service contains the business logic for program section operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for program sections - handles validation,
orchestration, and deletion checks.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.program_section import ProgramSection
from app.repositories.program_section_repository import ProgramSectionRepository
from app.repositories.module_repository import ModuleRepository


class ProgramSectionService:
    """
    Service class for program section business logic.
    
    This class contains methods that implement business rules for program section operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_section(db: Session, data):
        """
        Create a new program section.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema
        - Creates section object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Program existence should be validated (enforced by foreign key)
        
        USE CASE: Admin creates a new program section (e.g., "BSCS Section A")
        
        Args:
            db: Database session
            data: Program section schema with section information
        
        Returns:
            Created ProgramSection object
        """
        # Convert schema to model object
        section = ProgramSection(**data.dict())
        # Save to database via repository
        return ProgramSectionRepository.create(db, section)

    @staticmethod
    def get_sections(db: Session):
        """
        Get list of all program sections.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all sections
        
        USE CASE: Display section list, populate dropdowns, generate reports
        
        Args:
            db: Database session
        
        Returns:
            List of all ProgramSection objects
        """
        # Simple delegation to repository
        return ProgramSectionRepository.get_all(db)

    @staticmethod
    def update_section(db: Session, section_id: int, data):
        """
        Update an existing program section.
        
        BUSINESS LOGIC:
        1. Get section (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        
        USE CASE: Update section information (student_count, section_code, etc.)
        
        VALIDATION:
        - Section existence validated by get_by_id()
        - Field validation done by Pydantic schema
        
        Args:
            db: Database session
            section_id: ID of section to update
            data: Update schema with fields to update (only provided fields)
        
        Returns:
            Updated ProgramSection object
        
        Raises:
            HTTPException: 404 if section not found
        """
        # Get section (validates existence)
        section = ProgramSectionRepository.get_by_id(db, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Program section not found")

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
        Delete a program section.
        
        BUSINESS LOGIC:
        1. Get section (validates existence - raises 404 if not found)
        2. Check if section has modules (business rule: cannot delete section with modules)
        3. Delete if no modules, raise error if modules exist
        
        BUSINESS RULE: Cannot delete section if it has modules
        - Prevents orphaned modules (modules without section)
        - Maintains referential integrity
        - Requires deleting modules first (or reassigning them)
        
        NOTE: Uses ModuleRepository.get_by_program_section (method may not exist in repository)
        
        USE CASE: Remove program section (only if no modules exist)
        
        ERROR HANDLING:
        - Raises 404 if section not found
        - Raises 400 if section has modules
        
        Args:
            db: Database session
            section_id: ID of section to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if section not found
            HTTPException: 400 if section has modules
        """
        # Get section (validates existence)
        section = ProgramSectionRepository.get_by_id(db, section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Program section not found")

        # Business rule: Cannot delete section if it has modules
        # NOTE: This method may need to be implemented in ModuleRepository
        modules = ModuleRepository.get_by_program_section(db, section_id)
        if modules:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete program section with existing modules"
            )

        # Delete from database (only if no modules)
        ProgramSectionRepository.delete(db, section)
