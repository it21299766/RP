"""
Domain API Routes

RESTful endpoints for domain management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.domain import DomainCreate, DomainUpdate, DomainResponse
from app.services.domain_service import DomainService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/domains", tags=["Domains"])


@router.post("", response_model=DomainResponse, status_code=status.HTTP_201_CREATED)
def create_domain(
    payload: DomainCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new domain. ADMIN only."""
    return DomainService.create_domain(db, payload)


@router.get("", response_model=list[DomainResponse])
def list_domains(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of domains. All authenticated users."""
    return DomainService.get_domains(db)


@router.put("/{domain_id}", response_model=DomainResponse)
def update_domain(
    domain_id: int,
    payload: DomainUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update domain. ADMIN only."""
    return DomainService.update_domain(db, domain_id, payload)


@router.delete("/{domain_id}", status_code=status.HTTP_200_OK)
def delete_domain(
    domain_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete domain. ADMIN only."""
    DomainService.delete_domain(db, domain_id)
    return {"message": "Domain deleted successfully"}
