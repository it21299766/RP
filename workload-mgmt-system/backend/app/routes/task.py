"""
Legacy Task API Routes

NOTE: This is the legacy task route. New implementations should use:
- /api/task-templates (for reusable task definitions)
- /api/task-instances (for task executions)

This route is kept for backward compatibility.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/tasks", tags=["Tasks (Legacy)"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a task (legacy). ADMIN only. Use task-templates and task-instances instead."""
    return TaskService.create_task(db, payload)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of tasks (legacy). All authenticated users."""
    return TaskService.get_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get task by ID (legacy). All authenticated users."""
    return TaskService.get_task(db, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update task (legacy). ADMIN only."""
    return TaskService.update_task(db, task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete task (legacy). ADMIN only."""
    TaskService.delete_task(db, task_id)
    return {"message": "Task deleted successfully"}
