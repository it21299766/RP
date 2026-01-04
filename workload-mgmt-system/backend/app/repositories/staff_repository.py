"""
Staff Repository - Database Access Layer for Staff

This repository handles all database operations for staff members.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for staff.
No business logic here - just CRUD operations (Create, Read, Update, Delete).

WHY REPOSITORY PATTERN?
- Separation of concerns: Database logic separate from business logic
- Testability: Easy to mock for unit tests
- Maintainability: Database changes don't affect service layer
- Reusability: Same repository methods used by multiple services
"""

from sqlalchemy.orm import Session
from app.models.staff import Staff


class StaffRepository:
    """
    Repository class for Staff database operations.
    
    This class contains methods to interact with the staff table in the database.
    All methods are static (no instance needed) and take a database session.
    """

    @staticmethod
    def create(db: Session, staff: Staff) -> Staff:
        """
        Create a new staff member in the database.
        
        WHAT THIS DOES: Inserts a new staff record into the staff table.
        
        DATABASE OPERATION:
        - INSERT INTO staff (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like staff_id)
        
        RETRIEVES: The created staff object with all fields populated
        (including auto-generated staff_id from database)
        
        WHY REFRESH: After insert, database generates staff_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session (connection to database)
            staff: Staff object to insert (must have all required fields)
        
        Returns:
            Staff object with staff_id populated (database-generated)
        """
        # Add staff object to session (prepares INSERT statement)
        db.add(staff)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (staff_id)
        db.refresh(staff)
        return staff

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all staff members from the database.
        
        WHAT THIS DOES: Fetches all staff records from the staff table.
        
        DATABASE OPERATION:
        - SELECT * FROM staff
        
        RETRIEVES: List of all Staff objects (all columns for all staff)
        
        WHY: Used to display staff list, generate reports, pass to optimization algorithm
        
        USE CASES:
        - Staff listing page (show all staff)
        - Optimization algorithm (needs all staff for assignment)
        - Reports (generate workload reports for all staff)
        - Admin dashboard (view all staff)
        
        Args:
            db: Database session
        
        Returns:
            List of Staff objects (all staff in database)
        """
        # Query all staff records from database
        # This executes: SELECT * FROM staff
        return db.query(Staff).all()

    @staticmethod
    def get_by_id(db: Session, staff_id: int):
        """
        Retrieve a single staff member by their ID.
        
        WHAT THIS DOES: Fetches one staff record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM staff WHERE staff_id = ?
        
        RETRIEVES: Single Staff object matching the staff_id, or None if not found
        
        WHY: Used to get specific staff details, update staff, delete staff
        
        USE CASES:
        - View staff profile (get staff by ID)
        - Update staff information (need to get staff first)
        - Delete staff (need to get staff first)
        - Check if staff exists before operations
        
        Args:
            db: Database session
            staff_id: Primary key of staff to retrieve
        
        Returns:
            Staff object if found, None if not found
        """
        # Query staff by primary key (staff_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM staff WHERE staff_id = ?
        return db.query(Staff).filter(Staff.staff_id == staff_id).first()

    @staticmethod
    def update(db: Session, staff: Staff):
        """
        Update an existing staff member in the database.
        
        WHAT THIS DOES: Saves changes to a staff record that was already retrieved.
        
        DATABASE OPERATION:
        - UPDATE staff SET ... WHERE staff_id = ?
        - Commits the transaction
        - Refreshes the object to get any database-generated values
        
        RETRIEVES: Updated staff object with latest values from database
        
        PREREQUISITE: Staff object must already exist in database (retrieved via get_by_id)
        
        HOW IT WORKS:
        1. Staff object is modified (e.g., staff.name = "New Name")
        2. SQLAlchemy tracks the changes automatically
        3. commit() executes UPDATE statement
        4. refresh() ensures object has latest database values
        
        USE CASES:
        - Update staff information (name, designation, etc.)
        - Update staff password
        - Activate/deactivate staff account
        - Update staff availability
        
        Args:
            db: Database session
            staff: Staff object with modified fields (must have staff_id set)
        
        Returns:
            Updated Staff object (refreshed from database)
        """
        # Commit changes (SQLAlchemy tracks modifications automatically)
        # This executes: UPDATE staff SET ... WHERE staff_id = ?
        db.commit()
        # Refresh to get latest values from database
        db.refresh(staff)
        return staff

    @staticmethod
    def delete(db: Session, staff: Staff):
        """
        Delete a staff member from the database.
        
        WHAT THIS DOES: Removes a staff record from the staff table.
        
        DATABASE OPERATION:
        - DELETE FROM staff WHERE staff_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Staff object must already exist in database (retrieved via get_by_id)
        
        WARNING: This is a hard delete - record is permanently removed.
        Consider soft delete (is_active=False) instead for data retention.
        
        USE CASES:
        - Remove staff member (permanent deletion)
        - Clean up test data
        - Data maintenance
        
        CAUTION: 
        - May fail if staff has related records (assignments, etc.) due to foreign keys
        - Consider cascade delete or soft delete for production systems
        
        Args:
            db: Database session
            staff: Staff object to delete (must have staff_id set)
        
        Returns:
            None (void operation)
        """
        # Mark staff object for deletion
        db.delete(staff)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM staff WHERE staff_id = ?
        db.commit()
