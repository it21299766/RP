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
- PUT /api/staff/{id} - Update staff (ACADEMIC=own availability only, ADMIN=all fields)
- DELETE /api/staff/{id} - Delete staff (ADMIN only, unassigns tasks first)
- PUT /api/staff/{id}/password - Update password (ACADEMIC=own only, ADMIN=any)
- POST /api/staff/{id}/profile-picture - Upload profile picture (ADMIN only)
- DELETE /api/staff/{id}/profile-picture - Delete profile picture (ADMIN only)

AUTHORIZATION:
- ADMIN: Full access (create, update, delete, view any)
- ACADEMIC: View own profile only, update own availability
- MANAGEMENT: View any (read-only)
"""

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse, PasswordUpdate
from app.services.staff_service import StaffService
from app.utils.auth_guard import require_role, get_current_user
from app.models.staff import Staff
from typing import Optional

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
    Get a single staff member by ID.
    
    WHAT THIS ENDPOINT DOES: Returns staff details for the specified staff_id.
    
    AUTHORIZATION:
    - ACADEMIC: Can only view own profile (staff_id must match current_user.staff_id)
    - ADMIN/MANAGEMENT: Can view any staff profile
    
    PATH PARAMETER: staff_id - ID of staff to retrieve
    
    RESPONSE: StaffResponse with staff information
    
    USE CASES:
    - View staff profile
    - Edit staff form (get existing data)
    - Staff details page
    
    ERROR: 404 Not Found if staff doesn't exist
    ERROR: 403 Forbidden if ACADEMIC tries to view another staff's profile
    
    EXAMPLE REQUEST:
    GET /api/staff/5
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "username": "sf5",
        "name": "Dr. John Smith",
        ...
    }
    """
    # ACADEMIC can only view own profile
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
    current_user: Staff = Depends(get_current_user)
):
    """
    Update an existing staff member.
    
    WHAT THIS ENDPOINT DOES: Updates staff information (partial update).
    
    AUTHORIZATION:
    - ACADEMIC: Can only update their own profile (staff_id must match current_user.staff_id)
               Can only update the 'available' field
    - ADMIN/MANAGEMENT: Can update any staff member (all fields)
    
    PATH PARAMETER: staff_id - ID of staff to update
    
    REQUEST BODY: StaffUpdate schema with fields to update
    - All fields are optional (partial update)
    - Only provided fields are updated
    - Fields not provided remain unchanged
    
    RESPONSE: StaffResponse with updated staff information
    
    USE CASES:
    - Staff updating their own availability (ACADEMIC)
    - Admin updating staff designation (promotion)
    - Admin updating availability, skills, experience, etc.
    
    EXAMPLE REQUEST (Staff updating availability):
    PUT /api/staff/5
    {
        "available": false
    }
    
    EXAMPLE REQUEST (Admin updating staff):
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
    
    ERROR: 403 Forbidden if ACADEMIC tries to update someone else's profile
    ERROR: 403 Forbidden if ACADEMIC tries to update fields other than 'available'
    ERROR: 404 Not Found if staff doesn't exist
    """
    # ACADEMIC can only update their own profile
    if current_user.role == "ACADEMIC" and current_user.staff_id != staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    # ACADEMIC can only update availability field
    if current_user.role == "ACADEMIC":
        # Check if trying to update fields other than available
        update_dict = payload.model_dump(exclude_unset=True)
        allowed_fields = {"available"}
        forbidden_fields = set(update_dict.keys()) - allowed_fields
        if forbidden_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You can only update availability. Attempted to update: {', '.join(forbidden_fields)}"
            )
    
    # Delegate to service layer (handles 404 if staff not found)
    return StaffService.update_staff(db, staff_id, payload)


@router.delete("/{staff_id}", status_code=status.HTTP_200_OK)
def delete_staff(
    staff_id: int,
    unassign_tasks: bool = Query(True, description="Automatically unassign all tasks before deletion"),
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
    
    QUERY PARAMETER: unassign_tasks (default: true)
    - If true: Automatically unassigns all tasks before deletion
    - If false: Returns error if staff has assignments
    
    RESPONSE: Success message with number of unassigned tasks (status 200 OK)
    
    BUSINESS LOGIC:
    1. Checks if staff has assignments
    2. If unassign_tasks=true: Deletes all assignments automatically
    3. If unassign_tasks=false and staff has assignments: Returns error
    4. Deletes profile picture if exists
    5. Deletes staff record
    
    WARNING: Hard delete - permanently removes record
    - Consider soft delete (is_active=False) for production
    - All assignments for this staff will be deleted if unassign_tasks=true
    
    USE CASES:
    - Remove staff member (permanent deletion)
    - Clean up test data
    - Data maintenance
    
    ERROR: 404 Not Found if staff doesn't exist
    ERROR: 400 Bad Request if staff has assignments and unassign_tasks=false
    
    EXAMPLE REQUEST:
    DELETE /api/staff/5
    DELETE /api/staff/5?unassign_tasks=true
    DELETE /api/staff/5?unassign_tasks=false
    
    EXAMPLE RESPONSE (success):
    {
        "message": "Staff deleted successfully",
        "unassigned_assignments": 3
    }
    
    EXAMPLE RESPONSE (error - has assignments):
    {
        "detail": "Cannot delete staff member. They have 3 active assignment(s). 
                   Please unassign all tasks first, or use unassign_tasks=true parameter."
    }
    """
    # Delegate to service layer (handles 404 if staff not found, 400 if has assignments)
    result = StaffService.delete_staff(db, staff_id, unassign_tasks=unassign_tasks)
    
    # Return success message
    return {
        "message": "Staff deleted successfully",
        "unassigned_assignments": result.get("unassigned_assignments", 0)
    }


@router.put("/{staff_id}/password", response_model=StaffResponse)
def update_password(
    staff_id: int,
    payload: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Update staff password.
    
    WHAT THIS ENDPOINT DOES: Allows staff to change their password.
    
    AUTHORIZATION: Staff can update their own password, ADMIN can update any password
    - ACADEMIC: Can only update own password (staff_id must match current_user.staff_id)
    - ADMIN: Can update any staff password
    - MANAGEMENT: Can update any staff password
    
    PATH PARAMETER: staff_id - ID of staff to update password for
    
    REQUEST BODY: PasswordUpdate schema containing:
    - current_password: Current password (for verification)
    - new_password: New password to set
    
    RESPONSE: StaffResponse with updated staff information
    
    SECURITY:
    - Current password must be provided and verified
    - New password is hashed before storing
    - Prevents unauthorized password changes
    
    USE CASE: Allow staff to change their password
    
    ERROR: 404 Not Found if staff doesn't exist
    ERROR: 403 Forbidden if ACADEMIC tries to update another user's password
    ERROR: 400 Bad Request if current password is incorrect
    
    EXAMPLE REQUEST:
    PUT /api/staff/5/password
    {
        "current_password": "oldpassword123",
        "new_password": "newpassword456"
    }
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "username": "sf5",
        ...
    }
    """
    # Authorization check: ACADEMIC can only update their own password
    if current_user.role == "ACADEMIC" and current_user.staff_id != staff_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to change this user's password."
        )
    
    return StaffService.update_password(db, staff_id, payload)


@router.post("/{staff_id}/profile-picture", response_model=StaffResponse)
def upload_profile_picture(
    staff_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """
    Upload or update staff profile picture.
    
    WHAT THIS ENDPOINT DOES: Allows admin to upload/update a staff member's profile picture.
    
    AUTHORIZATION: ADMIN only (require_role("ADMIN"))
    - Only administrators can upload profile pictures
    
    PATH PARAMETER: staff_id - ID of staff to upload picture for
    
    REQUEST BODY: multipart/form-data with file field
    - file: Image file (jpg, jpeg, png, gif, webp)
    - Maximum size: 5MB
    
    RESPONSE: StaffResponse with updated profile_picture_path
    
    FILE STORAGE:
    - Files stored in: backend/uploads/profiles/
    - Filename format: staff_{staff_id}_{uuid}.{extension}
    - Old picture is automatically deleted when uploading new one
    
    VALIDATION:
    - Only image files allowed (jpg, jpeg, png, gif, webp)
    - File size limit: 5MB
    
    ERROR: 404 Not Found if staff doesn't exist
    ERROR: 400 Bad Request if file type not supported or file too large
    
    EXAMPLE REQUEST:
    POST /api/staff/5/profile-picture
    Content-Type: multipart/form-data
    file: [binary image data]
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "username": "sf5",
        "profile_picture_path": "profiles/staff_5_a1b2c3d4.jpg",
        ...
    }
    """
    # Delegate to service layer (handles file upload, validation, storage)
    return StaffService.upload_profile_picture(db, staff_id, file)


@router.delete("/{staff_id}/profile-picture", response_model=StaffResponse)
def delete_profile_picture(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: Staff = Depends(require_role("ADMIN"))
):
    """
    Delete staff profile picture.
    
    WHAT THIS ENDPOINT DOES: Allows admin to delete a staff member's profile picture.
    
    AUTHORIZATION: ADMIN only (require_role("ADMIN"))
    - Only administrators can delete profile pictures
    
    PATH PARAMETER: staff_id - ID of staff to delete picture for
    
    RESPONSE: StaffResponse with profile_picture_path = None
    
    FILE DELETION:
    - Deletes the physical file from the filesystem
    - Clears the profile_picture_path in the database
    
    ERROR: 404 Not Found if staff doesn't exist
    
    EXAMPLE REQUEST:
    DELETE /api/staff/5/profile-picture
    
    EXAMPLE RESPONSE:
    {
        "staff_id": 5,
        "username": "sf5",
        "profile_picture_path": null,
        ...
    }
    """
    return StaffService.delete_profile_picture(db, staff_id)
