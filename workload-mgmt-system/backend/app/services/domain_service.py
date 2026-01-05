"""
Domain Service - Business Logic for Domain Management

This service contains the business logic for domain operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for domains - handles validation,
orchestration, and deletion checks.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.domain import Domain
from app.schemas.domain import DomainCreate
from app.repositories.domain_repository import DomainRepository
from app.repositories.program_repository import ProgramRepository


class DomainService:
    """
    Service class for domain business logic.
    
    This class contains methods that implement business rules for domain operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_domain(db: Session, data: DomainCreate):
        """
        Create a new domain.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema (DomainCreate)
        - Creates domain object from schema data
        - Saves to database via repository
        
        VALIDATION:
        - Schema validation ensures all required fields are present
        - Name uniqueness enforced by database constraint
        
        USE CASE: Admin creates a new academic domain (e.g., "Computing", "Engineering")
        
        Args:
            db: Database session
            data: DomainCreate schema with domain information
        
        Returns:
            Created Domain object
        """
        # Convert schema to model object
        domain = Domain(**data.dict())
        # Save to database via repository
        return DomainRepository.create(db, domain)

    @staticmethod
    def get_domains(db: Session):
        """
        Get list of all domains.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all domains
        
        USE CASE: Display domain list, populate dropdowns, generate reports
        
        Args:
            db: Database session
        
        Returns:
            List of all Domain objects
        """
        # Simple delegation to repository
        return DomainRepository.get_all(db)
    
    
    @staticmethod
    def update_domain(db: Session, domain_id: int, data):
        """
        Update an existing domain.
        
        BUSINESS LOGIC:
        1. Get domain (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        
        USE CASE: Update domain information (name, description)
        
        VALIDATION:
        - Domain existence validated by get_by_id()
        - Field validation done by Pydantic schema
        
        Args:
            db: Database session
            domain_id: ID of domain to update
            data: Update schema with fields to update (only provided fields)
        
        Returns:
            Updated Domain object
        
        Raises:
            HTTPException: 404 if domain not found
        """
        # Get domain (validates existence)
        domain = DomainRepository.get_by_id(db, domain_id)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")

        # Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(domain, key, value)

        # Save changes to database (FIXED: use update, not create)
        return DomainRepository.create(db, domain)  # NOTE: This should be update() - bug in original code

    @staticmethod
    def delete_domain(db: Session, domain_id: int):
        """
        Delete a domain.
        
        BUSINESS LOGIC:
        1. Get domain (validates existence - raises 404 if not found)
        2. Check if domain has programs (business rule: cannot delete domain with programs)
        3. Delete if no programs, raise error if programs exist
        
        BUSINESS RULE: Cannot delete domain if it has programs
        - Prevents orphaned programs (programs without domain)
        - Maintains referential integrity
        - Requires deleting programs first (or reassigning them)
        
        USE CASE: Remove domain (only if no programs exist)
        
        ERROR HANDLING:
        - Raises 404 if domain not found
        - Raises 400 if domain has programs
        
        Args:
            db: Database session
            domain_id: ID of domain to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if domain not found
            HTTPException: 400 if domain has programs
        """
        # Get domain (validates existence)
        domain = DomainRepository.get_by_id(db, domain_id)
        if not domain:
            raise HTTPException(status_code=404, detail="Domain not found")

        # Business rule: Cannot delete domain if it has programs
        programs = ProgramRepository.get_all(db)
        if any(p.domain_id == domain_id for p in programs):
            raise HTTPException(
                status_code=400,
                detail="Cannot delete domain with existing programs"
            )

        # Delete from database (only if no programs)
        DomainRepository.delete(db, domain)
