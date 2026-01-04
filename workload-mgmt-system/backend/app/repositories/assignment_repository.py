"""
Assignment Repository - Database Access Layer for Assignments

This repository handles all database operations for assignments.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for assignments.
No business logic here - just CRUD operations.
"""

from sqlalchemy.orm import Session
from app.models.assignment import Assignment


class AssignmentRepository:
    """
    Repository class for Assignment database operations.
    
    This class contains methods to interact with the assignments table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, assignment: Assignment):
        """
        Create a new assignment in the database.
        
        WHAT THIS DOES: Inserts a new assignment record into the assignments table.
        
        DATABASE OPERATION:
        - INSERT INTO assignments (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like assignment_id)
        
        RETRIEVES: The created assignment object with all fields populated
        (including auto-generated assignment_id from database)
        
        WHY REFRESH: After insert, database generates assignment_id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            assignment: Assignment object to insert (must have staff_id and task_instance_id)
        
        Returns:
            Assignment object with assignment_id populated (database-generated)
        """
        # Add assignment object to session (prepares INSERT statement)
        db.add(assignment)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (assignment_id)
        db.refresh(assignment)
        return assignment

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all assignments from the database.
        
        WHAT THIS DOES: Fetches all assignment records from the assignments table.
        
        DATABASE OPERATION:
        - SELECT * FROM assignments
        
        RETRIEVES: List of all Assignment objects (all columns for all assignments)
        
        WHY: Used to display assignment list, generate reports, calculate workloads
        
        USE CASES:
        - Assignment listing page (show all assignments)
        - Workload calculation (sum assignments per staff)
        - Reports (generate assignment reports)
        - Optimization algorithm (get existing assignments)
        
        Args:
            db: Database session
        
        Returns:
            List of Assignment objects (all assignments in database)
        """
        # Query all assignment records from database
        # This executes: SELECT * FROM assignments
        return db.query(Assignment).all()

    @staticmethod
    def get_by_id(db: Session, assignment_id: int):
        """
        Retrieve a single assignment by its ID.
        
        WHAT THIS DOES: Fetches one assignment record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM assignments WHERE assignment_id = ?
        
        RETRIEVES: Single Assignment object matching the assignment_id, or None if not found
        
        WHY: Used to get specific assignment details, update assignment, delete assignment
        
        USE CASES:
        - View assignment details (get assignment by ID)
        - Update assignment (need to get assignment first)
        - Delete assignment (need to get assignment first)
        - Get assignment for change request
        
        Args:
            db: Database session
            assignment_id: Primary key of assignment to retrieve
        
        Returns:
            Assignment object if found, None if not found
        """
        # Query assignment by primary key (assignment_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM assignments WHERE assignment_id = ?
        return db.query(Assignment).filter(
            Assignment.assignment_id == assignment_id
        ).first()

    @staticmethod
    def get_by_staff_id(db: Session, staff_id: int):
        """
        Retrieve all assignments for a specific staff member.
        
        WHAT THIS DOES: Fetches all assignment records for a given staff member.
        
        DATABASE OPERATION:
        - SELECT * FROM assignments WHERE staff_id = ?
        
        RETRIEVES: List of Assignment objects for the specified staff_id
        
        WHY: Used to get all assignments for a staff member (for workload calculation, deletion)
        
        USE CASES:
        - Get all assignments for a staff member (workload calculation)
        - Delete all assignments for a staff member (before deleting staff)
        - Staff workload reports
        
        Args:
            db: Database session
            staff_id: Staff ID to get assignments for
        
        Returns:
            List of Assignment objects for the specified staff_id
        """
        # Query assignments by staff_id
        # This executes: SELECT * FROM assignments WHERE staff_id = ?
        return db.query(Assignment).filter(
            Assignment.staff_id == staff_id
        ).all()

    @staticmethod
    def delete(db: Session, assignment: Assignment):
        """
        Delete an assignment from the database.
        
        WHAT THIS DOES: Removes an assignment record from the assignments table.
        
        DATABASE OPERATION:
        - DELETE FROM assignments WHERE assignment_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        PREREQUISITE: Assignment object must already exist in database (retrieved via get_by_id)
        
        USE CASES:
        - Remove assignment (unassign staff from task)
        - Clean up test data
        - Remove incorrect assignments
        
        Args:
            db: Database session
            assignment: Assignment object to delete (must have assignment_id set)
        
        Returns:
            None (void operation)
        """
        # Mark assignment object for deletion
        db.delete(assignment)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM assignments WHERE assignment_id = ?
        db.commit()
    
    @staticmethod
    def delete_by_staff_id(db: Session, staff_id: int):
        """
        Delete all assignments for a specific staff member.
        
        WHAT THIS DOES: Removes all assignment records for a given staff member.
        
        DATABASE OPERATION:
        - DELETE FROM assignments WHERE staff_id = ?
        - Commits the transaction
        
        RETRIEVES: Number of assignments deleted (integer)
        
        WHY: Used to unassign all tasks from a staff member before deleting the staff record.
        This prevents foreign key constraint violations.
        
        USE CASES:
        - Unassign all tasks before deleting staff member
        - Bulk unassignment operations
        
        Args:
            db: Database session
            staff_id: Staff ID to delete all assignments for
        
        Returns:
            Number of assignments deleted (integer)
        """
        # Query all assignments for this staff member
        assignments = AssignmentRepository.get_by_staff_id(db, staff_id)
        
        # Delete each assignment
        count = 0
        for assignment in assignments:
            db.delete(assignment)
            count += 1
        
        # Commit all deletions
        if count > 0:
            db.commit()
        
        return count
