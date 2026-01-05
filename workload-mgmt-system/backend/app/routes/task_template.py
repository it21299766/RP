"""
TaskTemplate API Routes

RESTful endpoints for task template management.
Access: ADMIN only
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_template import (
    TaskTemplateCreate,
    TaskTemplateUpdate,
    TaskTemplateResponse
)
from app.services.task_template_service import TaskTemplateService
from app.utils.auth_guard import require_role
from app.models.staff import Staff

router = APIRouter(prefix="/api/task-templates", tags=["Task Templates"])


@router.post("", response_model=TaskTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_task_template(
    payload: TaskTemplateCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new task template. ADMIN only."""
    return TaskTemplateService.create_template(db, payload)


@router.get("", response_model=list[TaskTemplateResponse])
def list_task_templates(
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "ACADEMIC", "MANAGEMENT"))
):
    """Get list of task templates. All authenticated users."""
    return TaskTemplateService.get_template_list(db, active_only=active_only)


@router.get("/{template_id}", response_model=TaskTemplateResponse)
def get_task_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN", "ACADEMIC", "MANAGEMENT"))
):
    """Get task template by ID. All authenticated users."""
    return TaskTemplateService.get_template(db, template_id)


@router.put("/{template_id}", response_model=TaskTemplateResponse)
def update_task_template(
    template_id: int,
    payload: TaskTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update task template. ADMIN only."""
    return TaskTemplateService.update_template(db, template_id, payload)


@router.delete("/{template_id}", status_code=status.HTTP_200_OK)
def delete_task_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete task template (soft delete). ADMIN only."""
    TaskTemplateService.delete_template(db, template_id)
    return {"message": "Task template deleted successfully"}

