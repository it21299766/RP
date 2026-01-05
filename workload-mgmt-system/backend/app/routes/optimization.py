"""
Optimization API Routes

RESTful endpoints for workload optimization using GA.
Access: ADMIN only
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.optimization import OptimizationRequest, OptimizationResponse
from app.services.optimization_service import OptimizationService
from app.utils.auth_guard import require_role
from app.models.staff import Staff

router = APIRouter(prefix="/api/optimization", tags=["Optimization"])


@router.post("/run", response_model=OptimizationResponse)
def run_optimization(
    payload: OptimizationRequest,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """Run GA optimization. ADMIN only."""
    return OptimizationService.run_optimization(db, payload)
