"""
TaskTemplate Repository - Database Access Layer for Task Templates

This repository handles all database operations for task templates.
It provides a clean interface between the service layer and the database.

THINK OF IT AS: A data access layer that handles all database queries for task templates.
No business logic here - just CRUD operations (Create, Read, Update, Delete).
"""

from sqlalchemy.orm import Session
from app.models.task_template import TaskTemplate


class TaskTemplateRepository:
    """
    Repository class for TaskTemplate database operations.
    
    This class contains methods to interact with the task_templates table.
    All methods are static and take a database session.
    """

    @staticmethod
    def create(db: Session, task_template: TaskTemplate) -> TaskTemplate:
        """
        Create a new task template in the database.
        
        WHAT THIS DOES: Inserts a new task template record into the task_templates table.
        
        DATABASE OPERATION:
        - INSERT INTO task_templates (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like id)
        
        RETRIEVES: The created task template object with all fields populated
        (including auto-generated id from database)
        
        WHY REFRESH: After insert, database generates id (auto-increment).
        Refresh ensures we have the complete object with the new ID.
        
        Args:
            db: Database session
            task_template: TaskTemplate object to insert (must have all required fields)
        
        Returns:
            TaskTemplate object with id populated (database-generated)
        """
        # Add template object to session (prepares INSERT statement)
        db.add(task_template)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (id)
        db.refresh(task_template)
        return task_template

    @staticmethod
    def get_all(db: Session, active_only: bool = False):
        """
        Retrieve all task templates from the database.
        
        WHAT THIS DOES: Fetches all task template records, optionally filtered by active status.
        
        DATABASE OPERATION:
        - SELECT * FROM task_templates [WHERE is_active = TRUE]
        
        RETRIEVES: List of TaskTemplate objects (all columns)
        
        WHY ACTIVE_ONLY OPTION:
        - active_only=False: Returns all templates (including inactive/soft-deleted ones)
        - active_only=True: Returns only active templates (for dropdowns, new instances)
        
        USE CASES:
        - Template listing (all templates for admin view)
        - Dropdown for creating task instances (active_only=True)
        - Reports (all templates for historical data)
        
        Args:
            db: Database session
            active_only: If True, only return templates where is_active=True
        
        Returns:
            List of TaskTemplate objects
        """
        # Start with query for all templates
        query = db.query(TaskTemplate)
        # Apply filter if active_only is True
        if active_only:
            # Only return active templates (soft-deleted ones excluded)
            query = query.filter(TaskTemplate.is_active == True)
        # Execute query and return results
        return query.all()

    @staticmethod
    def get_by_id(db: Session, template_id: int):
        """
        Retrieve a single task template by its ID.
        
        WHAT THIS DOES: Fetches one task template record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM task_templates WHERE id = ?
        
        RETRIEVES: Single TaskTemplate object matching the template_id, or None if not found
        
        WHY: Used to get specific template details, update template, delete template
        
        USE CASES:
        - View template details (get template by ID)
        - Update template (need to get template first)
        - Delete template (need to get template first)
        - Validate template exists before creating task instance
        
        Args:
            db: Database session
            template_id: Primary key of template to retrieve
        
        Returns:
            TaskTemplate object if found, None if not found
        """
        # Query template by primary key (id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM task_templates WHERE id = ?
        return db.query(TaskTemplate).filter(TaskTemplate.id == template_id).first()

    @staticmethod
    def update(db: Session, task_template: TaskTemplate):
        """
        Update an existing task template in the database.
        
        WHAT THIS DOES: Saves changes to a task template that was already retrieved.
        
        DATABASE OPERATION:
        - UPDATE task_templates SET ... WHERE id = ?
        - Commits the transaction
        - Refreshes the object to get any database-generated values
        
        RETRIEVES: Updated task template object with latest values from database
        
        PREREQUISITE: TaskTemplate object must already exist in database (retrieved via get_by_id)
        
        HOW IT WORKS:
        1. TaskTemplate object is modified (e.g., template.name = "New Name")
        2. SQLAlchemy tracks the changes automatically
        3. commit() executes UPDATE statement
        4. refresh() ensures object has latest database values
        
        USE CASES:
        - Update template information (name, hours, requirements)
        - Activate/deactivate template (is_active)
        - Update template requirements (qualification, skills)
        
        Args:
            db: Database session
            task_template: TaskTemplate object with modified fields (must have id set)
        
        Returns:
            Updated TaskTemplate object (refreshed from database)
        """
        # Commit changes (SQLAlchemy tracks modifications automatically)
        # This executes: UPDATE task_templates SET ... WHERE id = ?
        db.commit()
        # Refresh to get latest values from database
        db.refresh(task_template)
        return task_template

    @staticmethod
    def delete(db: Session, task_template: TaskTemplate):
        """
        Soft delete a task template (set is_active=False).
        
        WHAT THIS DOES: Marks a task template as inactive instead of deleting it.
        
        DATABASE OPERATION:
        - UPDATE task_templates SET is_active = FALSE WHERE id = ?
        - Commits the transaction
        
        RETRIEVES: Updated task template object with is_active=False
        
        WHY SOFT DELETE:
        - Preserves historical data (existing task instances still reference template)
        - Can reactivate templates later if needed
        - Maintains data integrity (no foreign key violations)
        - Better than hard delete for audit and reporting
        
        PREREQUISITE: TaskTemplate object must already exist in database
        
        USE CASES:
        - Deactivate obsolete templates (course no longer taught)
        - Hide templates from active use while keeping historical data
        
        Args:
            db: Database session
            task_template: TaskTemplate object to soft delete (must have id set)
        
        Returns:
            TaskTemplate object with is_active=False
        """
        # Set is_active to False (soft delete)
        task_template.is_active = False
        # Commit changes (execute UPDATE)
        db.commit()
        return task_template

    @staticmethod
    def hard_delete(db: Session, task_template: TaskTemplate):
        """
        Permanently delete a task template from the database.
        
        WHAT THIS DOES: Removes a task template record from the task_templates table.
        
        DATABASE OPERATION:
        - DELETE FROM task_templates WHERE id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        WARNING: Hard delete - permanently removes record.
        Use soft delete (delete method) instead unless absolutely necessary.
        
        PREREQUISITE: TaskTemplate object must already exist in database
        
        CAUTION: 
        - May fail if template has related task instances (foreign key constraint)
        - Consider soft delete for production systems
        
        USE CASES:
        - Clean up test data
        - Remove incorrectly created templates (if no instances exist)
        
        Args:
            db: Database session
            task_template: TaskTemplate object to delete (must have id set)
        
        Returns:
            None (void operation)
        """
        # Mark template object for deletion
        db.delete(task_template)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM task_templates WHERE id = ?
        db.commit()
