"""
Task Repository - Database Access Layer for Legacy Tasks (Deprecated)

⚠️ DEPRECATED: This repository is kept for backward compatibility during migration.
New code should use TaskTemplateRepository and TaskInstanceRepository instead.

This repository handles database operations for the legacy Task model.
The new system splits tasks into TaskTemplate (reusable definitions) and TaskInstance (specific executions).
"""

from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:
    """
    Legacy Task Repository - DEPRECATED
    
    This repository is kept for backward compatibility but should not be used for new development.
    Use TaskTemplateRepository and TaskInstanceRepository instead.
    """

    @staticmethod
    def create(db: Session, task: Task):
        """
        Create a new legacy task in the database.
        
        ⚠️ DEPRECATED: Use TaskTemplateRepository and TaskInstanceRepository instead.
        
        WHAT THIS DOES: Inserts a new task record into the legacy tasks table.
        
        DATABASE OPERATION:
        - INSERT INTO tasks (...) VALUES (...)
        - Commits the transaction
        - Refreshes the object to get database-generated values (like task_id)
        
        RETRIEVES: The created task object with all fields populated
        
        Args:
            db: Database session
            task: Task object to insert
        
        Returns:
            Task object with task_id populated (database-generated)
        """
        # Add task object to session (prepares INSERT statement)
        db.add(task)
        # Execute INSERT and commit transaction
        db.commit()
        # Refresh object to get database-generated values (task_id)
        db.refresh(task)
        return task

    @staticmethod
    def get_all(db: Session):
        """
        Retrieve all legacy tasks from the database.
        
        ⚠️ DEPRECATED: Use TaskTemplateRepository and TaskInstanceRepository instead.
        
        WHAT THIS DOES: Fetches all task records from the legacy tasks table.
        
        DATABASE OPERATION:
        - SELECT * FROM tasks
        
        RETRIEVES: List of all Task objects
        
        Args:
            db: Database session
        
        Returns:
            List of Task objects (all legacy tasks in database)
        """
        # Query all task records from database
        # This executes: SELECT * FROM tasks
        return db.query(Task).all()

    @staticmethod
    def get_by_id(db: Session, task_id: int):
        """
        Retrieve a single legacy task by its ID.
        
        ⚠️ DEPRECATED: Use TaskTemplateRepository and TaskInstanceRepository instead.
        
        WHAT THIS DOES: Fetches one task record by primary key.
        
        DATABASE OPERATION:
        - SELECT * FROM tasks WHERE task_id = ?
        
        RETRIEVES: Single Task object matching the task_id, or None if not found
        
        Args:
            db: Database session
            task_id: Primary key of task to retrieve
        
        Returns:
            Task object if found, None if not found
        """
        # Query task by primary key (task_id)
        # .first() returns the first match or None
        # This executes: SELECT * FROM tasks WHERE task_id = ?
        return db.query(Task).filter(Task.task_id == task_id).first()

    @staticmethod
    def update(db: Session, task: Task):
        """
        Update an existing legacy task in the database.
        
        ⚠️ DEPRECATED: Use TaskTemplateRepository and TaskInstanceRepository instead.
        
        WHAT THIS DOES: Saves changes to a task that was already retrieved.
        
        DATABASE OPERATION:
        - UPDATE tasks SET ... WHERE task_id = ?
        - Commits the transaction
        - Refreshes the object to get any database-generated values
        
        RETRIEVES: Updated task object with latest values from database
        
        Args:
            db: Database session
            task: Task object with modified fields (must have task_id set)
        
        Returns:
            Updated Task object (refreshed from database)
        """
        # Commit changes (SQLAlchemy tracks modifications automatically)
        # This executes: UPDATE tasks SET ... WHERE task_id = ?
        db.commit()
        # Refresh to get latest values from database
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task: Task):
        """
        Delete a legacy task from the database.
        
        ⚠️ DEPRECATED: Use TaskTemplateRepository and TaskInstanceRepository instead.
        
        WHAT THIS DOES: Removes a task record from the tasks table.
        
        DATABASE OPERATION:
        - DELETE FROM tasks WHERE task_id = ?
        - Commits the transaction
        
        RETRIEVES: Nothing (void operation)
        
        Args:
            db: Database session
            task: Task object to delete (must have task_id set)
        
        Returns:
            None (void operation)
        """
        # Mark task object for deletion
        db.delete(task)
        # Execute DELETE and commit transaction
        # This executes: DELETE FROM tasks WHERE task_id = ?
        db.commit()
