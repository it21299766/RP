"""
Tariff Service - Business Logic for Tariff Management

This service contains the business logic for tariff operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for tariffs - handles validation,
orchestration, and workload calculation rules.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.tariff import Tariff
from app.repositories.tariff_repository import TariffRepository


class TariffService:
    """
    Service class for tariff business logic.
    
    This class contains methods that implement business rules for tariff operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_tariff(db: Session, data):
        """
        Create a new tariff rule.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema
        - Creates tariff object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Field types and constraints validated by Pydantic
        
        USE CASE: Admin creates a new tariff rule (e.g., "Lecture = 2 hours per section")
        
        Args:
            db: Database session
            data: Tariff schema with tariff information
        
        Returns:
            Created Tariff object
        """
        # Convert schema to model object
        tariff = Tariff(**data.dict())
        # Save to database via repository
        return TariffRepository.create(db, tariff)

    @staticmethod
    def get_tariffs(db: Session):
        """
        Get list of all tariff rules.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all tariffs
        
        USE CASES:
        - Tariff listing page (show all tariff rules)
        - Lookup tariff for task type (calculate workload hours)
        - Reports (generate tariff reports)
        
        Args:
            db: Database session
        
        Returns:
            List of all Tariff objects
        """
        # Simple delegation to repository
        return TariffRepository.get_all(db)

    @staticmethod
    def update_tariff(db: Session, tariff_id: int, data):
        """
        Update an existing tariff rule.
        
        BUSINESS LOGIC:
        1. Get tariff (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just hours)
        
        USE CASE: Update tariff information (hours, per_unit, category)
        
        VALIDATION:
        - Tariff existence validated by get_by_id()
        - Field validation done by Pydantic schema
        
        Args:
            db: Database session
            tariff_id: ID of tariff to update
            data: Update schema with fields to update (only provided fields)
        
        Returns:
            Updated Tariff object
        
        Raises:
            HTTPException: 404 if tariff not found
        """
        # STEP 1: Get tariff (validates existence)
        tariff = TariffRepository.get_by_id(db, tariff_id)
        if not tariff:
            raise HTTPException(status_code=404, detail="Tariff not found")

        # STEP 2: Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(tariff, key, value)

        # STEP 3: Save changes directly (note: not using repository.update for consistency)
        db.commit()
        db.refresh(tariff)
        return tariff

    @staticmethod
    def delete_tariff(db: Session, tariff_id: int):
        """
        Delete a tariff rule.
        
        BUSINESS LOGIC:
        1. Get tariff (validates existence - raises 404 if not found)
        2. Delete from database
        
        USE CASE: Remove tariff rule (permanent deletion)
        
        WARNING: Hard delete - permanently removes record.
        Consider impact on workload calculations before deleting.
        
        ERROR HANDLING:
        - Raises 404 if tariff not found
        
        Args:
            db: Database session
            tariff_id: ID of tariff to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if tariff not found
        """
        # Get tariff (validates existence)
        tariff = TariffRepository.get_by_id(db, tariff_id)
        if not tariff:
            raise HTTPException(status_code=404, detail="Tariff not found")

        # Delete from database
        TariffRepository.delete(db, tariff)
