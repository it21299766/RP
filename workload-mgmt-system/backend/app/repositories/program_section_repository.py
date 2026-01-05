"""
ProgramSection Repository - Database Access Layer for Program Sections

This repository handles all database operations for program sections.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for program sections.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.program_section import ProgramSection


class ProgramSectionRepository:
    """
    Repository class for ProgramSection database operations.
    
    This class contains methods to interact with the program_sections table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, obj: ProgramSection):
        """
        Create a new program section in the database.
        
        WHAT THIS DOES: Inserts a new program section record into the program_sections table.
        
        DATABASE OPERATION:
        - INSERT INTO program_sections (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like section_id)
        
        RETRIEVES: The created program section object with all fields populated
        (including auto-generated section_id from database)
        
        WHY REFRESH: After insert, database generates section_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            obj: ProgramSection object to insert (must have program_id, section_code, student_count, academic_year)
        
        Returns:
            ProgramSection object with section_id populated (database-generated)
        """
        # Add program section object to session (prepares INSERT statement)
        db.add(obj)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (section_id)
        db.refresh(obj)
        return obj

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all program sections from the database.
        
        WHAT THIS DOES: Fetches all program section records from the program_sections table.
        
        DATABASE OPERATION:
        - SELECT * FROM program_sections
        
        RETRIEVES: List of all ProgramSection objects (all columns for all sections)
        
        WHY: Used to display section list, generate reports, populate dropdowns
        
        USE CASES:
        - Program section listing page (show all sections)
        - Dropdown for selecting section (when creating task instances)
        - Reports (generate section-level reports)
        - Filter task instances by section
        
        Args:
            db: Database session
        
        Returns:
            List of ProgramSection objects (all program sections in database)
        """
        # Query all program section records from database
        # This executes: SELECT * FROM program_sections
        return db.query(ProgramSection).all()

    @staticmethod
    def get_by_id(db: Session, section_id: int):
        """
        Retrieve a single program section by its ID.
        
        WHAT THIS DOES: Fetches one program section record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM program_sections WHERE section_id = ?
        
        RETRIEVES: Single ProgramSection object matching the section_id, or None if not found
        
        WHY: Used to get specific section details, update section, delete section, validate section exists
        
        USE CASES:
        - View section details (get section by ID)
        - Update section (need to get section first)
        - Delete section (need to get section first)
        - Validate section exists before creating task instance
        
        Args:
            db: Database session
            section_id: Primary key of program section to retrieve
        
        Returns:
            ProgramSection object if found, None if not found
        """
        # Query program section by primary key (section_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM program_sections WHERE section_id = ?
        return db.query(ProgramSection).filter(
            ProgramSection.section_id == section_id
        ).first()

    @staticmethod
    def delete(db: Session, section: ProgramSection):
        """
        Delete a program section from the database.
        
        WHAT THIS DOES: Removes a program section record from the program_sections table.
        
        DATABASE OPERATION:
        - DELETE FROM program_sections WHERE section_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: ProgramSection object must already exist in database (retrieved via get_by_id)
        
        WARNING: Hard delete - may fail if section has related task instances (foreign key constraint)
        
        USE CASES:
        - Remove program section (permanent deletion)
        - Clean up test data
        
        CAUTION: Consider cascade delete or preventing deletion if task instances exist
        
        Args:
            db: Database session
            section: ProgramSection object to delete (must have section_id set)
        
        Returns:
            None (void operation)
        """
        # Mark program section object for deletion
        db.delete(section)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM program_sections WHERE section_id = ?
        db.commit()
