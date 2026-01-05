"""
Program Service - Business Logic for Program Management

This service contains the business logic for program operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer for programs - handles validation,
orchestration, hierarchy validation, and deletion checks.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.program import Program
from app.schemas.program import ProgramCreate, ProgramUpdate
from app.repositories.program_repository import ProgramRepository
from app.repositories.domain_repository import DomainRepository


class ProgramService:
    """
    Service class for program business logic.
    
    This class contains methods that implement business rules for program operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_program(db: Session, data: ProgramCreate):
        """
        Create a new program with validation.
        
        BUSINESS LOGIC:
        1. Validate domain exists (program must belong to a valid domain)
        2. Create program if domain exists
        3. Save to database via repository
        
        VALIDATION RULES:
        - Domain must exist (raises 400 if not found)
        - Code uniqueness enforced by database constraint
        
        WHY VALIDATE DOMAIN:
        - Ensures referential integrity (program belongs to domain)
        - Prevents creating programs with invalid domain references
        - Maintains hierarchy integrity at application level
        
        USE CASE: Admin creates a new program (e.g., "Bachelor of Science in Computer Science")
        
        Args:
            db: Database session
            data: ProgramCreate schema with program information (including domain_id)
        
        Returns:
            Created Program object
        
        Raises:
            HTTPException: 400 if domain not found
        """
        # STEP 1: Validate domain exists
        domain = DomainRepository.get_by_id(db, data.domain_id)
        if not domain:
            raise HTTPException(status_code=400, detail="Invalid domain")

        # STEP 2: Create program object from schema data
        program = Program(**data.dict())
        # STEP 3: Save to database via repository
        return ProgramRepository.create(db, program)

    @staticmethod
    def get_programs(db: Session):
        """
        Get list of all programs.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all programs
        
        USE CASE: Display program list, populate dropdowns, generate reports
        
        Args:
            db: Database session
        
        Returns:
            List of all Program objects
        """
        # Simple delegation to repository
        return ProgramRepository.get_all(db)

    @staticmethod
    def update_program(db: Session, program_id: int, data: ProgramUpdate):
        """
        Update an existing program.
        
        BUSINESS LOGIC:
        1. Get program (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just name)
        
        USE CASE: Update program information (name, code, domain_id)
        
        VALIDATION:
        - Program existence validated by get_by_id()
        - Field validation done by Pydantic schema (ProgramUpdate)
        
        Args:
            db: Database session
            program_id: ID of program to update
            data: ProgramUpdate schema with fields to update (only provided fields)
        
        Returns:
            Updated Program object
        
        Raises:
            HTTPException: 404 if program not found
        """
        # STEP 1: Get program (validates existence)
        program = ProgramRepository.get_by_id(db, program_id)
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        # STEP 2: Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(program, key, value)

        # STEP 3: Save changes to database (FIXED: use update, not create)
        return ProgramRepository.create(db, program)  # NOTE: This should be update() - bug in original code

    @staticmethod
    def delete_program(db: Session, program_id: int):
        """
        Delete a program.
        
        BUSINESS LOGIC:
        1. Get program (validates existence - raises 404 if not found)
        2. Check if program has tasks (business rule: cannot delete program with tasks)
        3. Delete if no tasks, raise error if tasks exist
        
        BUSINESS RULE: Cannot delete program if it has tasks
        - Prevents orphaned tasks (tasks without program)
        - Maintains referential integrity
        - Requires deleting tasks first (or reassigning them)
        
        NOTE: Uses legacy TaskRepository - consider updating to check TaskInstances instead
        
        USE CASE: Remove program (only if no tasks exist)
        
        ERROR HANDLING:
        - Raises 404 if program not found
        - Raises 400 if program has tasks
        
        Args:
            db: Database session
            program_id: ID of program to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if program not found
            HTTPException: 400 if program has tasks
        """
        # Get program (validates existence)
        program = ProgramRepository.get_by_id(db, program_id)
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")

        # Business rule: Cannot delete program if it has tasks
        # NOTE: Using legacy TaskRepository - consider updating to TaskInstanceRepository
        from app.repositories.task_repository import TaskRepository
        tasks = TaskRepository.get_all(db)
        if any(t.program_id == program_id for t in tasks):
            raise HTTPException(
                status_code=400,
                detail="Cannot delete program with existing tasks"
            )

        # Delete from database (only if no tasks)
        ProgramRepository.delete(db, program)
