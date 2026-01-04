"""
Program Repository - Database Access Layer for Programs

This repository handles all database operations for programs.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for programs.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.program import Program


class ProgramRepository:
    """
    Repository class for Program database operations.
    
    This class contains methods to interact with the programs table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, program: Program):
        """
        Create a new program in the database.
        
        WHAT THIS DOES: Inserts a new program record into the programs table.
        
        DATABASE OPERATION:
        - INSERT INTO programs (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like program_id)
        
        RETRIEVES: The created program object with all fields populated
        (including auto-generated program_id from database)
        
        WHY REFRESH: After insert, database generates program_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            program: Program object to insert (must have name, code, domain_id)
        
        Returns:
            Program object with program_id populated (database-generated)
        """
        # Add program object to session (prepares INSERT statement)
        db.add(program)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (program_id)
        db.refresh(program)
        return program

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all programs from the database.
        
        WHAT THIS DOES: Fetches all program records from the programs table.
        
        DATABASE OPERATION:
        - SELECT * FROM programs
        
        RETRIEVES: List of all Program objects (all columns for all programs)
        
        WHY: Used to display program list, generate reports, populate dropdowns
        
        USE CASES:
        - Program listing page (show all programs)
        - Dropdown for selecting program (when creating task instances)
        - Reports (generate program-level reports)
        - Filter task instances by program
        
        Args:
            db: Database session
        
        Returns:
            List of Program objects (all programs in database)
        """
        # Query all program records from database
        # This executes: SELECT * FROM programs
        return db.query(Program).all()

    @staticmethod
    def get_by_id(db: Session, program_id: int):
        """
        Retrieve a single program by its ID.
        
        WHAT THIS DOES: Fetches one program record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM programs WHERE program_id = ?
        
        RETRIEVES: Single Program object matching the program_id, or None if not found
        
        WHY: Used to get specific program details, update program, delete program, validate program exists
        
        USE CASES:
        - View program details (get program by ID)
        - Update program (need to get program first)
        - Delete program (need to get program first)
        - Validate program exists before creating task instance/program section
        
        Args:
            db: Database session
            program_id: Primary key of program to retrieve
        
        Returns:
            Program object if found, None if not found
        """
        # Query program by primary key (program_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM programs WHERE program_id = ?
        return db.query(Program).filter(Program.program_id == program_id).first()

    @staticmethod
    def delete(db: Session, program: Program):
        """
        Delete a program from the database.
        
        WHAT THIS DOES: Removes a program record from the programs table.
        
        DATABASE OPERATION:
        - DELETE FROM programs WHERE program_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Program object must already exist in database (retrieved via get_by_id)
        
        WARNING: Hard delete - may fail if program has related sections/task instances (foreign key constraint)
        
        USE CASES:
        - Remove program (permanent deletion)
        - Clean up test data
        
        CAUTION: Consider cascade delete or preventing deletion if sections/task instances exist
        
        Args:
            db: Database session
            program: Program object to delete (must have program_id set)
        
        Returns:
            None (void operation)
        """
        # Mark program object for deletion
        db.delete(program)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM programs WHERE program_id = ?
        db.commit()
