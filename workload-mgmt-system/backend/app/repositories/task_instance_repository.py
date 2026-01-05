"""
TaskInstance Repository - Database Access Layer for Task Instances

This repository handles all database operations for task instances.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for task instances.
No business logic here - just CRUD operations and filtering.
"""

from sqlalchemy.orm import Session
from app.models.task_instance import TaskInstance
from typing import Optional, List


class TaskInstanceRepository:
    """
    Repository class for TaskInstance database operations.
    
    This class contains methods to interact with the task_instances table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, task_instance: TaskInstance) -> TaskInstance:
        """
        Create a new task instance in the database.
        
        WHAT THIS DOES: Inserts a new task instance record into the task_instances table.
        
        DATABASE OPERATION:
        - INSERT INTO task_instances (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like id)
        
        RETRIEVES: The created task instance object with all fields populated
        (including auto-generated id from database)
        
        WHY REFRESH: After insert, database generates id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            task_instance: TaskInstance object to insert (must have all required fields)
        
        Returns:
            TaskInstance object with id populated (database-generated)
        """
        # Add instance object to session (prepares INSERT statement)
        db.add(task_instance)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (id)
        db.refresh(task_instance)
        return task_instance

    @staticmethod
    def get_all(
        db: Session,
        status: Optional[str] = None,
        semester: Optional[str] = None,
        academic_year: Optional[str] = None
    ) -> List[TaskInstance]:
        """
        Retrieve all task instances with optional filters.
        
        WHAT THIS DOES: Fetches task instance records, optionally filtered by status, semester, or academic year.
        
        DATABASE OPERATION:
        - SELECT * FROM task_instances [WHERE status = ? AND semester = ? AND academic_year = ?]
        
        RETRIEVES: List of TaskInstance objects matching the filters
        
        FILTERS (all optional):
        - status: Filter by workflow status (draft, approved, completed)
        - semester: Filter by semester (e.g., "2025S1", "2025S2")
        - academic_year: Filter by academic year (e.g., "2024-2025")
        
        USE CASES:
        - List all instances (no filters)
        - Get approved instances for optimization (status="approved")
        - Get instances for specific semester (semester="2025S1")
        - Get instances for academic year (academic_year="2024-2025")
        - Combined filters (e.g., approved instances for Fall 2025)
        
        WHY FILTERS:
        - Optimization algorithm needs only approved instances
        - Reports need instances for specific time periods
        - Workflow management needs instances by status
        
        Args:
            db: Database session
            status: Optional status filter (draft, approved, completed)
            semester: Optional semester filter (e.g., "2025S1")
            academic_year: Optional academic year filter (e.g., "2024-2025")
        
        Returns:
            List of TaskInstance objects matching the filters
        """
        # Start with query for all instances
        query = db.query(TaskInstance)
        
        # Apply filters if provided
        if status:
            # Filter by workflow status
            query = query.filter(TaskInstance.status == status)
        if semester:
            # Filter by semester
            query = query.filter(TaskInstance.semester == semester)
        if academic_year:
            # Filter by academic year
            query = query.filter(TaskInstance.academic_year == academic_year)
        
        # Execute query and return results
        return query.all()

    @staticmethod
    def get_by_id(db: Session, instance_id: int) -> Optional[TaskInstance]:
        """
        Retrieve a single task instance by its ID.
        
        WHAT THIS DOES: Fetches one task instance record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM task_instances WHERE id = ?
        
        RETRIEVES: Single TaskInstance object matching the instance_id, or None if not found
        
        WHY: Used to get specific instance details, update instance, delete instance
        
        USE CASES:
        - View instance details (get instance by ID)
        - Update instance (need to get instance first)
        - Delete instance (need to get instance first)
        - Get instance for assignment creation
        
        Args:
            db: Database session
            instance_id: Primary key of instance to retrieve
        
        Returns:
            TaskInstance object if found, None if not found
        """
        # Query instance by primary key (id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM task_instances WHERE id = ?
        return db.query(TaskInstance).filter(TaskInstance.id == instance_id).first()

    @staticmethod
    def get_approved(db: Session) -> List[TaskInstance]:
        """
        Get all approved task instances (for GA optimization).
        
        WHAT THIS DOES: Fetches only task instances with status="approved".
        
        DATABASE OPERATION:
        - SELECT * FROM task_instances WHERE status = 'approved'
        
        RETRIEVES: List of approved TaskInstance objects
        
        WHY SEPARATE METHOD:
        - Optimization algorithm only works with approved instances
        - Common use case (used frequently)
        - Convenience method for clarity
        
        USE CASES:
        - GA optimization algorithm (needs approved instances to assign)
        - Workload planning (only plan for approved tasks)
        - Assignment creation (only assign approved instances)
        
        WHY APPROVED ONLY:
        - Draft instances are not yet finalized
        - Completed instances are already done
        - Only approved instances need assignment/optimization
        
        Args:
            db: Database session
        
        Returns:
            List of approved TaskInstance objects (status="approved")
        """
        # Query only approved instances
        # This executes: SELECT * FROM task_instances WHERE status = 'approved'
        return db.query(TaskInstance).filter(TaskInstance.status == "approved").all()

    @staticmethod
    def update(db: Session, task_instance: TaskInstance) -> TaskInstance:
        """
        Update an existing task instance in the database.
        
        WHAT THIS DOES: Saves changes to a task instance that was already retrieved.
        
        DATABASE OPERATION:
        - UPDATE task_instances SET ... WHERE id = ?
        - Commits the transaction
        - Refreshes the object to get any database-generated values
        
        RETRIEVES: Updated task instance object with latest values from database
        
        PREREQUISITE: TaskInstance object must already exist in database (retrieved via get_by_id)
        
        HOW IT WORKS:
        1. TaskInstance object is modified (e.g., instance.status = "approved")
        2. SQLAlchemy tracks the changes automatically
        3. commit() executes UPDATE statement
        4. refresh() ensures object has latest database values
        
        USE CASES:
        - Update instance status (draft → approved → completed)
        - Update instance hours (effective_hours)
        - Update instance details (semester, program_section_id)
        
        Args:
            db: Database session
            task_instance: TaskInstance object with modified fields (must have id set)
        
        Returns:
            Updated TaskInstance object (refreshed from database)
        """
        # Commit changes (SQLAlchemy tracks modifications automatically)
        # This executes: UPDATE task_instances SET ... WHERE id = ?
        db.commit()
        # Refresh to get latest values from database
        db.refresh(task_instance)
        return task_instance

    @staticmethod
    def delete(db: Session, task_instance: TaskInstance):
        """
        Delete a task instance from the database.
        
        WHAT THIS DOES: Removes a task instance record from the task_instances table.
        
        DATABASE OPERATION:
        - DELETE FROM task_instances WHERE id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        WARNING: Hard delete - permanently removes record.
        Typically only allowed for draft instances (business rule enforced in service layer).
        
        PREREQUISITE: TaskInstance object must already exist in database
        
        CAUTION: 
        - May fail if instance has related assignments (foreign key constraint)
        - Consider soft delete for production systems
        
        USE CASES:
        - Delete draft instances (not yet approved)
        - Clean up test data
        - Remove incorrectly created instances (if no assignments exist)
        
        Args:
            db: Database session
            task_instance: TaskInstance object to delete (must have id set)
        
        Returns:
            None (void operation)
        """
        # Mark instance object for deletion
        db.delete(task_instance)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM task_instances WHERE id = ?
        db.commit()
