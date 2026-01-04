"""
Domain Repository - Database Access Layer for Domains

This repository handles all database operations for domains.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for domains.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.domain import Domain


class DomainRepository:
    """
    Repository class for Domain database operations.
    
    This class contains methods to interact with the domains table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, domain: Domain):
        """
        Create a new domain in the database.
        
        WHAT THIS DOES: Inserts a new domain record into the domains table.
        
        DATABASE OPERATION:
        - INSERT INTO domains (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like domain_id)
        
        RETRIEVES: The created domain object with all fields populated
        (including auto-generated domain_id from database)
        
        WHY REFRESH: After insert, database generates domain_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            domain: Domain object to insert (must have name)
        
        Returns:
            Domain object with domain_id populated (database-generated)
        """
        # Add domain object to session (prepares INSERT statement)
        db.add(domain)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (domain_id)
        db.refresh(domain)
        return domain

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all domains from the database.
        
        WHAT THIS DOES: Fetches all domain records from the domains table.
        
        DATABASE OPERATION:
        - SELECT * FROM domains
        
        RETRIEVES: List of all Domain objects (all columns for all domains)
        
        WHY: Used to display domain list, generate reports, populate dropdowns
        
        USE CASES:
        - Domain listing page (show all domains)
        - Dropdown for selecting domain (when creating programs)
        - Reports (generate domain-level reports)
        - Filter programs by domain
        
        Args:
            db: Database session
        
        Returns:
            List of Domain objects (all domains in database)
        """
        # Query all domain records from database
        # This executes: SELECT * FROM domains
        return db.query(Domain).all()

    @staticmethod
    def get_by_id(db: Session, domain_id: int):
        """
        Retrieve a single domain by its ID.
        
        WHAT THIS DOES: Fetches one domain record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM domains WHERE domain_id = ?
        
        RETRIEVES: Single Domain object matching the domain_id, or None if not found
        
        WHY: Used to get specific domain details, update domain, delete domain, validate domain exists
        
        USE CASES:
        - View domain details (get domain by ID)
        - Update domain (need to get domain first)
        - Delete domain (need to get domain first)
        - Validate domain exists before creating program/task instance
        
        Args:
            db: Database session
            domain_id: Primary key of domain to retrieve
        
        Returns:
            Domain object if found, None if not found
        """
        # Query domain by primary key (domain_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM domains WHERE domain_id = ?
        return db.query(Domain).filter(Domain.domain_id == domain_id).first()

    @staticmethod
    def delete(db: Session, domain: Domain):
        """
        Delete a domain from the database.
        
        WHAT THIS DOES: Removes a domain record from the domains table.
        
        DATABASE OPERATION:
        - DELETE FROM domains WHERE domain_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Domain object must already exist in database (retrieved via get_by_id)
        
        WARNING: Hard delete - may fail if domain has related programs (foreign key constraint)
        
        USE CASES:
        - Remove domain (permanent deletion)
        - Clean up test data
        
        CAUTION: Consider cascade delete or preventing deletion if programs exist
        
        Args:
            db: Database session
            domain: Domain object to delete (must have domain_id set)
        
        Returns:
            None (void operation)
        """
        # Mark domain object for deletion
        db.delete(domain)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM domains WHERE domain_id = ?
        db.commit()
