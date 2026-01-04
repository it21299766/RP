"""
Task Service - Business Logic for Legacy Tasks (Deprecated)

⚠️ DEPRECATED: This service is kept for backward compatibility during migration.
New code should use TaskTemplateService and TaskInstanceService instead.

This service handles business logic for the legacy Task model.
The new system splits tasks into TaskTemplate (reusable definitions) and TaskInstance (specific executions).
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    """
    Legacy Task Service - DEPRECATED
    
    This service is kept for backward compatibility but should not be used for new development.
    Use TaskTemplateService and TaskInstanceService instead.
    """

    @staticmethod
    def create_task(db: Session, data: TaskCreate):
        """
        Create a new legacy task.
        
        ⚠️ DEPRECATED: Use TaskTemplateService and TaskInstanceService instead.
        
        BUSINESS LOGIC:
        - Validates data via Pydantic schema
        - Creates task object from schema data
        - Saves to database via repository
        
        Args:
            db: Database session
            data: TaskCreate schema with task information
        
        Returns:
            Created Task object
        """
        # Convert schema to model object
        task = Task(**data.dict())
        # Save to database via repository
        return TaskRepository.create(db, task)

    @staticmethod
    def get_tasks(db: Session):
        """
        Get list of all legacy tasks.
        
        ⚠️ DEPRECATED: Use TaskTemplateService and TaskInstanceService instead.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all tasks
        
        Args:
            db: Database session
        
        Returns:
            List of all Task objects
        """
        # Simple delegation to repository
        return TaskRepository.get_all(db)

    @staticmethod
    def get_task(db: Session, task_id: int):
        """
        Get legacy task by ID.
        
        ⚠️ DEPRECATED: Use TaskTemplateService and TaskInstanceService instead.
        
        BUSINESS LOGIC:
        - Validates that task exists
        - Raises 404 error if not found
        
        Args:
            db: Database session
            task_id: ID of task to retrieve
        
        Returns:
            Task object if found
        
        Raises:
            HTTPException: 404 if task not found
        """
        # Get task from database
        task = TaskRepository.get_by_id(db, task_id)
        
        # Business rule: Task must exist
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, data: TaskUpdate):
        """
        Update an existing legacy task.
        
        ⚠️ DEPRECATED: Use TaskTemplateService and TaskInstanceService instead.
        
        BUSINESS LOGIC:
        1. Get task (validates existence)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        Args:
            db: Database session
            task_id: ID of task to update
            data: TaskUpdate schema with fields to update
        
        Returns:
            Updated Task object
        
        Raises:
            HTTPException: 404 if task not found
        """
        # Get task (validates existence)
        task = TaskService.get_task(db, task_id)
        
        # Update only provided fields (partial update)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        
        # Save changes to database
        return TaskRepository.update(db, task)

    @staticmethod
    def delete_task(db: Session, task_id: int):
        """
        Delete a legacy task.
        
        ⚠️ DEPRECATED: Use TaskTemplateService and TaskInstanceService instead.
        
        BUSINESS LOGIC:
        1. Get task (validates existence)
        2. Delete from database
        
        Args:
            db: Database session
            task_id: ID of task to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if task not found
        """
        # Get task (validates existence)
        task = TaskService.get_task(db, task_id)
        
        # Delete from database
        TaskRepository.delete(db, task)
