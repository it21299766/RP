"""
Tariff API Routes

RESTful endpoints for tariff management.
Access: ADMIN for write, all authenticated for read
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.tariff import TariffCreate, TariffUpdate, TariffResponse
from app.services.tariff_service import TariffService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

router = APIRouter(prefix="/api/tariffs", tags=["Tariffs"])


@router.post("", response_model=TariffResponse, status_code=status.HTTP_201_CREATED)
def create_tariff(
    payload: TariffCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Create a new tariff. ADMIN only."""
    return TariffService.create_tariff(db, payload)


@router.get("", response_model=list[TariffResponse])
def list_tariffs(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """Get list of tariffs. All authenticated users."""
    return TariffService.get_tariffs(db)


@router.put("/{tariff_id}", response_model=TariffResponse)
def update_tariff(
    tariff_id: int,
    payload: TariffUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Update tariff. ADMIN only."""
    return TariffService.update_tariff(db, tariff_id, payload)


@router.delete("/{tariff_id}", status_code=status.HTTP_200_OK)
def delete_tariff(
    tariff_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Delete tariff. ADMIN only."""
    TariffService.delete_tariff(db, tariff_id)
    return {"message": "Tariff deleted successfully"}
