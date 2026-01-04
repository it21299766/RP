"""
Staff API Routes - RESTful Endpoints for Staff Management

This file defines the HTTP API endpoints for staff operations.
Each endpoint handles one type of request (GET, POST, PUT, DELETE).

THINK OF IT AS: The "front door" to staff functionality - defines what URLs
the frontend can call and what they do.

ROUTES:
- POST /api/staff - Create new staff (ADMIN only)
- GET /api/staff - List all staff (all authenticated users)
- GET /api/staff/{id} - Get staff by ID (ACADEMIC=own only, ADMIN/MANAGEMENT=any)
- PUT /api/staff/{id} - Update staff (ADMIN only)
- DELETE /api/staff/{id} - Delete staff (ADMIN only)

AUTHORIZATION:
- ADMIN: Full access (create, update, delete, view any)
- ACADEMIC: View own profile only
- MANAGEMENT: View any (read-only)
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.services.staff_service import StaffService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff

# Create router for staff endpoints
# All routes here will be prefixed with "/api/staff"
router = APIRouter(prefix="/api/staff", tags=["Staff"])


@router.post("", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """
    Create a new staff member.
    
    WHAT THIS ENDPOINT DOES: Allows admin to add a new staff member to the system.
    
    AUTHORIZATION: ADMIN only (require_role("ADMIN"))
    - Only administrators can create staff members
    - Academic and management staff cannot create staff
    
    REQUEST BODY: StaffCreate schema containing:
    - Required: name, designation, qualification, specialization, department, role
    - Optional: experience_years, skills, available, username, password
    - If password not provided: defaults to username
    - If username not provided: auto-generated (sf{staff_id} or adm{staff_id})
    
    RESPONSE: StaffResponse with created staff information (status 201 Created)
    
    BUSINESS LOGIC: Handled by StaffService.create_staff()
    - Generates username if not provided
    - Sets default password (username) if not provided
    - Hashes password before storing
    
    EXAMPLE REQUEST:
    POST /api/staff
    {
        "name": "Dr. John Smith",
        "designation": "Professor",
        "qualification": "PhD",
        "specialization": "Computer Science",
        "department": "Computer Science",
        "role": "ACADEMIC",
        "experience_years": 15
    }
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 7,
        "username": "sf7",
        "name": "Dr. John Smith",
        "designation": "Professor",
        ...
    }
    """
    # Delegate to service layer (handles business logic)
    return StaffService.create_staff(db, payload)


@router.get("", response_model=list[StaffResponse])
def list_staff(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get list of all staff members.
    
    WHAT THIS ENDPOINT DOES: Returns all staff in the system.
    
    AUTHORIZATION: All authenticated users
    - Any logged-in user can view staff list
    - No role restriction (but ACADEMIC can only view own details in get_staff)
    
    RESPONSE: List of StaffResponse objects (all staff)
    
    USE CASES:
    - Staff listing page
    - Dropdown for assigning tasks
    - Reports and analytics
    - Optimization algorithm (needs all staff)
    
    NOTE: This returns all staff, but individual staff details are restricted
    (ACADEMIC can only view own profile via get_staff endpoint)
    
    EXAMPLE RESPONSE:
    [
        {
            "staff_id": 1,
            "username": "sf1",
            "name": "Dr. John Smith",
            ...
        },
        {
            "staff_id": 2,
            "username": "sf2",
            "name": "Dr. Sarah Johnson",
            ...
        }
    ]
    """
    # Delegate to service layer
    return StaffService.get_staff_list(db)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get staff member by ID.
    
    WHAT THIS ENDPOINT DOES: Returns details of a specific staff member.
    
    AUTHORIZATION: Role-based access control
    - ACADEMIC: Can only view own profile (staff_id must match current_user.staff_id)
    - ADMIN: Can view any staff profile
    - MANAGEMENT: Can view any staff profile
    
    PATH PARAMETER: staff_id - ID of staff to retrieve
    
    RESPONSE: StaffResponse with staff details
    
    BUSINESS RULE: ACADEMIC staff can only view their own profile
    - Prevents academic staff from viewing other staff's information
    - Admin and management have full read access
    
    ERROR: 403 Forbidden if ACADEMIC tries to view another staff's profile
    ERROR: 404 Not Found if staff doesn't exist
    
    EXAMPLE REQUEST:
    GET /api/staff/5
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "username": "sf5",
        "name": "Dr. Michael Williams",
        ...
    }
    """
    # BUSINESS RULE: ACADEMIC can only view own profile
    # Check if user is ACADEMIC and trying to view someone else's profile
    if current_user.role == "ACADEMIC" and current_user.staff_id != staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )
    
    # Delegate to service layer (handles 404 if staff not found)
    return StaffService.get_staff(db, staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    payload: StaffUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """
    Update an existing staff member.
    
    WHAT THIS ENDPOINT DOES: Updates staff information (partial update).
    
    AUTHORIZATION: ADMIN only (require_role("ADMIN"))
    - Only administrators can update staff information
    - Academic staff cannot update their own or others' information
    
    PATH PARAMETER: staff_id - ID of staff to update
    
    REQUEST BODY: StaffUpdate schema with fields to update
    - All fields are optional (partial update)
    - Only provided fields are updated
    - Fields not provided remain unchanged
    
    RESPONSE: StaffResponse with updated staff information
    
    USE CASES:
    - Update staff designation (promotion)
    - Update availability (set to unavailable)
    - Update skills or experience
    - Activate/deactivate account (is_active)
    
    EXAMPLE REQUEST:
    PUT /api/staff/5
    {
        "designation": "Senior Lecturer I",
        "available": false
    }
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "designation": "Senior Lecturer I",
        "available": false,
        ...
    }
    """
    # Delegate to service layer (handles 404 if staff not found)
    return StaffService.update_staff(db, staff_id, payload)


@router.delete("/{staff_id}", status_code=status.HTTP_200_OK)
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """
    Delete a staff member.
    
    WHAT THIS ENDPOINT DOES: Permanently removes a staff member from the system.
    
    AUTHORIZATION: ADMIN only (require_role("ADMIN"))
    - Only administrators can delete staff
    - This is a destructive operation
    
    PATH PARAMETER: staff_id - ID of staff to delete
    
    RESPONSE: Success message (status 200 OK)
    
    WARNING: Hard delete - permanently removes record
    - Consider soft delete (is_active=False) for production
    - May fail if staff has related records (assignments, etc.)
    
    USE CASES:
    - Remove staff member (permanent deletion)
    - Clean up test data
    - Data maintenance
    
    ERROR: 404 Not Found if staff doesn't exist
    ERROR: Database error if staff has related records (foreign key constraint)
    
    EXAMPLE REQUEST:
    DELETE /api/staff/5
    
    EXAMPLE RESPONSE:
    {
        "message": "Staff deleted successfully"
    }
    """
    # Delegate to service layer (handles 404 if staff not found)
    StaffService.delete_staff(db, staff_id)
    
    # Return success message
    return {"message": "Staff deleted successfully"}
