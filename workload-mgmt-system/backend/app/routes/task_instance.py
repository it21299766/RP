"""
TaskInstance API Routes

RESTful endpoints for task instance management.
Access: ADMIN for create/update/delete, all authenticated for read
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_instance import (
    TaskInstanceCreate,
    TaskInstanceUpdate,
    TaskInstanceResponse
)
from app.services.task_instance_service import TaskInstanceService
from app.utils.auth_guard import require_role
from app.models.staff import Staff
from typing import Optional

router = APIRouter(prefix="/api/task-instances", tags=["Task Instances"])


@router.post("", response_model=TaskInstanceResponse, status_code=status.HTTP_201_CREATED)
def create_task_instance(
    payload: TaskInstanceCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new task instance. ADMIN only."""
    return TaskInstanceService.create_instance(db, payload)


@router.get("", response_model=list[TaskInstanceResponse])
def list_task_instances(
    status: Optional[str] = Query(None, description="Filter by status"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    academic_year: Optional[str] = Query(None, description="Filter by academic year"),
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "ACADEMIC", "MANAGEMENT"))
):
    """Get list of task instances with optional filters. All authenticated users."""
    return TaskInstanceService.get_instance_list(
        db,
        status=status,
        semester=semester,
        academic_year=academic_year
    )


@router.get("/approved", response_model=list[TaskInstanceResponse])
def get_approved_instances(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "ACADEMIC", "MANAGEMENT"))
):
    """Get all approved task instances (for optimization). All authenticated users."""
    return TaskInstanceService.get_approved_instances(db)


@router.get("/{instance_id}", response_model=TaskInstanceResponse)
def get_task_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "ACADEMIC", "MANAGEMENT"))
):
    """Get task instance by ID. All authenticated users."""
    return TaskInstanceService.get_instance(db, instance_id)


@router.put("/{instance_id}", response_model=TaskInstanceResponse)
def update_task_instance(
    instance_id: int,
    payload: TaskInstanceUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update task instance. ADMIN only."""
    return TaskInstanceService.update_instance(db, instance_id, payload)


@router.post("/{instance_id}/approve", response_model=TaskInstanceResponse)
def approve_task_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Approve a task instance. ADMIN only."""
    return TaskInstanceService.approve_instance(db, instance_id)


@router.delete("/{instance_id}", status_code=status.HTTP_200_OK)
def delete_task_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete task instance (only if draft). ADMIN only."""
    TaskInstanceService.delete_instance(db, instance_id)
    return {"message": "Task instance deleted successfully"}

