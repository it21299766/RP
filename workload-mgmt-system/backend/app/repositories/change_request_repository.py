"""
ChangeRequest Repository - Database Access Layer for Change Requests

This repository handles all database operations for change requests.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for change requests.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.change_request import ChangeRequest


class ChangeRequestRepository:
    """
    Repository class for ChangeRequest database operations.
    
    This class contains methods to interact with the change_requests table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, obj: ChangeRequest):
        """
        Create a new change request in the database.
        
        WHAT THIS DOES: Inserts a new change request record into the change_requests table.
        
        DATABASE OPERATION:
        - INSERT INTO change_requests (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like request_id)
        
        RETRIEVES: The created change request object with all fields populated
        (including auto-generated request_id from database)
        
        WHY REFRESH: After insert, database generates request_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            obj: ChangeRequest object to insert (must have assignment_id, requested_by_staff_id, reason)
        
        Returns:
            ChangeRequest object with request_id populated (database-generated)
        """
        # Add change request object to session (prepares INSERT statement)
        db.add(obj)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (request_id)
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, request_id: int):
        """
        Retrieve a single change request by its ID.
        
        WHAT THIS DOES: Fetches one change request record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM change_requests WHERE request_id = ?
        
        RETRIEVES: Single ChangeRequest object matching the request_id, or None if not found
        
        WHY: Used to get specific request details, update request, approve/reject request
        
        USE CASES:
        - View request details (get request by ID)
        - Update request status (approve/reject)
        - Get request for processing
        
        Args:
            db: Database session
            request_id: Primary key of change request to retrieve
        
        Returns:
            ChangeRequest object if found, None if not found
        """
        # Query change request by primary key (request_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM change_requests WHERE request_id = ?
        return db.query(ChangeRequest).filter(
            ChangeRequest.request_id == request_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all change requests from the database.
        
        WHAT THIS DOES: Fetches all change request records from the change_requests table.
        
        DATABASE OPERATION:
        - SELECT * FROM change_requests
        
        RETRIEVES: List of all ChangeRequest objects (all columns for all requests)
        
        WHY: Used to display request list, generate reports, filter by status
        
        USE CASES:
        - Change request listing page (show all requests)
        - Admin dashboard (view pending requests)
        - Reports (generate request reports)
        - Filter requests by status (pending, approved, rejected)
        
        Args:
            db: Database session
        
        Returns:
            List of ChangeRequest objects (all change requests in database)
        """
        # Query all change request records from database
        # This executes: SELECT * FROM change_requests
        return db.query(ChangeRequest).all()
    
    @staticmethod
    def get_by_staff_id(db: Session, staff_id: int):
        """
        Retrieve all change requests for a specific staff member.
        
        WHAT THIS DOES: Fetches change request records filtered by staff ID.
        
        DATABASE OPERATION:
        - SELECT * FROM change_requests WHERE requested_by_staff_id = ?
        
        RETRIEVES: List of ChangeRequest objects for the specified staff member
        
        WHY: Used to display staff's own change requests
        
        USE CASES:
        - Staff view of their own change requests
        - Filter requests by staff member
        
        Args:
            db: Database session
            staff_id: ID of staff member to get requests for
        
        Returns:
            List of ChangeRequest objects for the specified staff member
        """
        # Query change requests by staff ID
        # This executes: SELECT * FROM change_requests WHERE requested_by_staff_id = ?
        return db.query(ChangeRequest).filter(
            ChangeRequest.requested_by_staff_id == staff_id
        ).all()
