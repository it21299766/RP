"""
Module Repository - Database Access Layer for Modules

This repository handles all database operations for modules.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for modules.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.module import Module


class ModuleRepository:
    """
    Repository class for Module database operations.
    
    This class contains methods to interact with the modules table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, module: Module):
        """
        Create a new module in the database.
        
        WHAT THIS DOES: Inserts a new module record into the modules table.
        
        DATABASE OPERATION:
        - INSERT INTO modules (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like module_id)
        
        RETRIEVES: The created module object with all fields populated
        (including auto-generated module_id from database)
        
        WHY REFRESH: After insert, database generates module_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            module: Module object to insert (must have name, code, program_id, semester, credits)
        
        Returns:
            Module object with module_id populated (database-generated)
        """
        # Add module object to session (prepares INSERT statement)
        db.add(module)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (module_id)
        db.refresh(module)
        return module

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all modules from the database.
        
        WHAT THIS DOES: Fetches all module records from the modules table.
        
        DATABASE OPERATION:
        - SELECT * FROM modules
        
        RETRIEVES: List of all Module objects (all columns for all modules)
        
        WHY: Used to display module list, generate reports, populate dropdowns
        
        USE CASES:
        - Module listing page (show all modules)
        - Dropdown for selecting module
        - Reports (generate module-level reports)
        - Curriculum management
        
        Args:
            db: Database session
        
        Returns:
            List of Module objects (all modules in database)
        """
        # Query all module records from database
        # This executes: SELECT * FROM modules
        return db.query(Module).all()

    @staticmethod
    def get_by_id(db: Session, module_id: int):
        """
        Retrieve a single module by its ID.
        
        WHAT THIS DOES: Fetches one module record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM modules WHERE module_id = ?
        
        RETRIEVES: Single Module object matching the module_id, or None if not found
        
        WHY: Used to get specific module details, update module, delete module, validate module exists
        
        USE CASES:
        - View module details (get module by ID)
        - Update module (need to get module first)
        - Delete module (need to get module first)
        - Validate module exists before creating module section
        
        Args:
            db: Database session
            module_id: Primary key of module to retrieve
        
        Returns:
            Module object if found, None if not found
        """
        # Query module by primary key (module_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM modules WHERE module_id = ?
        return db.query(Module).filter(
            Module.module_id == module_id
        ).first()

    @staticmethod
    def delete(db: Session, module: Module):
        """
        Delete a module from the database.
        
        WHAT THIS DOES: Removes a module record from the modules table.
        
        DATABASE OPERATION:
        - DELETE FROM modules WHERE module_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Module object must already exist in database (retrieved via get_by_id)
        
        WARNING: Hard delete - may fail if module has related module sections (foreign key constraint)
        
        USE CASES:
        - Remove module (permanent deletion)
        - Clean up test data
        
        CAUTION: Consider cascade delete or preventing deletion if module sections exist
        
        Args:
            db: Database session
            module: Module object to delete (must have module_id set)
        
        Returns:
            None (void operation)
        """
        # Mark module object for deletion
        db.delete(module)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM modules WHERE module_id = ?
        db.commit()
