"""
ModuleSection Repository - Database Access Layer for Module Sections

This repository handles all database operations for module sections.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for module sections.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.module_section import ModuleSection


class ModuleSectionRepository:
    """
    Repository class for ModuleSection database operations.
    
    This class contains methods to interact with the module_sections table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, obj: ModuleSection):
        """
        Create a new module section in the database.
        
        WHAT THIS DOES: Inserts a new module section record into the module_sections table.
        
        DATABASE OPERATION:
        - INSERT INTO module_sections (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like section_id)
        
        RETRIEVES: The created module section object with all fields populated
        (including auto-generated section_id from database)
        
        WHY REFRESH: After insert, database generates section_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            obj: ModuleSection object to insert (must have module_id, section_code, student_count)
        
        Returns:
            ModuleSection object with section_id populated (database-generated)
        """
        # Add module section object to session (prepares INSERT statement)
        db.add(obj)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (section_id)
        db.refresh(obj)
        return obj

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all module sections from the database.
        
        WHAT THIS DOES: Fetches all module section records from the module_sections table.
        
        DATABASE OPERATION:
        - SELECT * FROM module_sections
        
        RETRIEVES: List of all ModuleSection objects (all columns for all sections)
        
        WHY: Used to display section list, generate reports
        
        USE CASES:
        - Module section listing page (show all sections)
        - Reports (generate section-level reports)
        - Scheduling and planning
        
        Args:
            db: Database session
        
        Returns:
            List of ModuleSection objects (all module sections in database)
        """
        # Query all module section records from database
        # This executes: SELECT * FROM module_sections
        return db.query(ModuleSection).all()

    @staticmethod
    def get_by_id(db: Session, section_id: int):
        """
        Retrieve a single module section by its ID.
        
        WHAT THIS DOES: Fetches one module section record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM module_sections WHERE section_id = ?
        
        RETRIEVES: Single ModuleSection object matching the section_id, or None if not found
        
        WHY: Used to get specific section details, update section, delete section
        
        USE CASES:
        - View section details (get section by ID)
        - Update section (need to get section first)
        - Delete section (need to get section first)
        
        Args:
            db: Database session
            section_id: Primary key of module section to retrieve
        
        Returns:
            ModuleSection object if found, None if not found
        """
        # Query module section by primary key (section_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM module_sections WHERE section_id = ?
        return db.query(ModuleSection).filter(
            ModuleSection.section_id == section_id
        ).first()

    @staticmethod
    def delete(db: Session, section: ModuleSection):
        """
        Delete a module section from the database.
        
        WHAT THIS DOES: Removes a module section record from the module_sections table.
        
        DATABASE OPERATION:
        - DELETE FROM module_sections WHERE section_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: ModuleSection object must already exist in database (retrieved via get_by_id)
        
        USE CASES:
        - Remove module section (permanent deletion)
        - Clean up test data
        
        Args:
            db: Database session
            section: ModuleSection object to delete (must have section_id set)
        
        Returns:
            None (void operation)
        """
        # Mark module section object for deletion
        db.delete(section)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM module_sections WHERE section_id = ?
        db.commit()
