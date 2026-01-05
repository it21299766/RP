"""
Tariff Repository - Database Access Layer for Tariffs

This repository handles all database operations for tariffs.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for tariffs.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.tariff import Tariff


class TariffRepository:
    """
    Repository class for Tariff database operations.
    
    This class contains methods to interact with the tariffs table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, obj: Tariff):
        """
        Create a new tariff rule in the database.
        
        WHAT THIS DOES: Inserts a new tariff record into the tariffs table.
        
        DATABASE OPERATION:
        - INSERT INTO tariffs (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like tariff_id)
        
        RETRIEVES: The created tariff object with all fields populated
        (including auto-generated tariff_id from database)
        
        WHY REFRESH: After insert, database generates tariff_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            obj: Tariff object to insert (must have task_type, category, hours, per_unit)
        
        Returns:
            Tariff object with tariff_id populated (database-generated)
        """
        # Add tariff object to session (prepares INSERT statement)
        db.add(obj)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (tariff_id)
        db.refresh(obj)
        return obj

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all tariff rules from the database.
        
        WHAT THIS DOES: Fetches all tariff records from the tariffs table.
        
        DATABASE OPERATION:
        - SELECT * FROM tariffs
        
        RETRIEVES: List of all Tariff objects (all columns for all tariffs)
        
        WHY: Used to display tariff list, lookup tariff rules for workload calculation
        
        USE CASES:
        - Tariff listing page (show all tariff rules)
        - Lookup tariff for task type (calculate workload hours)
        - Reports (generate tariff reports)
        - Workload calculation (get hours based on task type)
        
        Args:
            db: Database session
        
        Returns:
            List of Tariff objects (all tariffs in database)
        """
        # Query all tariff records from database
        # This executes: SELECT * FROM tariffs
        return db.query(Tariff).all()

    @staticmethod
    def get_by_id(db: Session, tariff_id: int):
        """
        Retrieve a single tariff rule by its ID.
        
        WHAT THIS DOES: Fetches one tariff record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM tariffs WHERE tariff_id = ?
        
        RETRIEVES: Single Tariff object matching the tariff_id, or None if not found
        
        WHY: Used to get specific tariff details, update tariff, delete tariff
        
        USE CASES:
        - View tariff details (get tariff by ID)
        - Update tariff (need to get tariff first)
        - Delete tariff (need to get tariff first)
        
        Args:
            db: Database session
            tariff_id: Primary key of tariff to retrieve
        
        Returns:
            Tariff object if found, None if not found
        """
        # Query tariff by primary key (tariff_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM tariffs WHERE tariff_id = ?
        return db.query(Tariff).filter(
            Tariff.tariff_id == tariff_id
        ).first()

    @staticmethod
    def delete(db: Session, tariff: Tariff):
        """
        Delete a tariff rule from the database.
        
        WHAT THIS DOES: Removes a tariff record from the tariffs table.
        
        DATABASE OPERATION:
        - DELETE FROM tariffs WHERE tariff_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Tariff object must already exist in database (retrieved via get_by_id)
        
        USE CASES:
        - Remove tariff rule (permanent deletion)
        - Clean up test data
        - Remove obsolete tariff rules
        
        Args:
            db: Database session
            tariff: Tariff object to delete (must have tariff_id set)
        
        Returns:
            None (void operation)
        """
        # Mark tariff object for deletion
        db.delete(tariff)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM tariffs WHERE tariff_id = ?
        db.commit()
