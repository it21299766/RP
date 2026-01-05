"""
Staff Service - Business Logic for Staff Management

This service contains the business logic for staff operations.
It coordinates between the repository (database) and the API layer (routes).

THINK OF IT AS: The "business rules" layer - handles validation, orchestration,
and complex operations that require multiple steps.

WHY SERVICE LAYER?
- Business logic separate from database access
- Validation and error handling
- Complex operations (multiple database calls, calculations)
- Coordinates between repositories and schemas
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate, PasswordUpdate
from app.repositories.staff_repository import StaffRepository
from app.utils.security import hash_password, verify_password
from app.utils.username_generator import generate_username
import os
import shutil
import uuid
from pathlib import Path


class StaffService:
    """
    Service class for staff business logic.
    
    This class contains methods that implement business rules for staff operations.
    It uses the repository to access the database and handles validation/errors.
    """

    @staticmethod
    def create_staff(db: Session, data: StaffCreate) -> Staff:
        """
        Create a new staff member with automatic username generation and password setting.
        
        BUSINESS LOGIC:
        This method implements the staff creation workflow:
        1. Extract staff data from request (excluding password/username)
        2. Create staff object and save to get staff_id (auto-increment)
        3. Generate username if not provided (sf{staff_id} or adm{staff_id})
        4. Set password (use provided password OR default to username)
        5. Hash password before storing
        6. Update staff with username and password hash
        
        WHY TWO STEPS (create then update)?
        - Need staff_id to generate username (username includes staff_id)
        - Database auto-generates staff_id only after INSERT
        - So we: INSERT → get ID → generate username → UPDATE with username/password
        
        VALIDATION:
        - Staff data validated by Pydantic schema (StaffCreate)
        - Username uniqueness checked by generate_username()
        - Password automatically hashed (never store plain text!)
        
        DEFAULT BEHAVIOR:
        - If no username provided: Auto-generate (sf1, sf2, adm1, etc.)
        - If no password provided: Default to username (sf1/sf1, adm1/adm1)
        - This ensures every staff member can login immediately
        
        Args:
            db: Database session
            data: StaffCreate schema with staff information
        
        Returns:
            Created Staff object with username and password_hash set
        """
        # STEP 1: Extract staff data, excluding password and username
        # We handle these separately because:
        # - Username needs staff_id (which doesn't exist yet)
        # - Password needs to be hashed
        staff_data = data.dict(exclude={'password', 'username'})
        
        # STEP 2: Create staff object with basic information
        # Set is_active=True by default (new staff can login immediately)
        staff = Staff(**staff_data)
        staff.is_active = True
        
        # STEP 3: Save to database to get staff_id (auto-increment)
        # This executes: INSERT INTO staff (...) VALUES (...)
        # After this, staff.staff_id is populated by database
        staff = StaffRepository.create(db, staff)
        
        # STEP 4: Generate username if not provided
        # Username format: sf{staff_id} for academic, adm{staff_id} for admin/management
        # Example: staff_id=7, role=ACADEMIC → username="sf7"
        if not data.username:
            staff.username = generate_username(staff.role, staff.staff_id, db)
        else:
            # Use provided username (must be unique - checked by database constraint)
            staff.username = data.username
        
        # STEP 5: Set password (hash it before storing)
        # Default password is the username (e.g., sf7/sf7)
        if data.password:
            # Use provided password
            staff.password_hash = hash_password(data.password)
        else:
            # Default password = username (e.g., staff with username "sf7" has password "sf7")
            default_password = staff.username
            staff.password_hash = hash_password(default_password)
        
        # STEP 6: Update staff record with username and password_hash
        # This executes: UPDATE staff SET username=?, password_hash=? WHERE staff_id=?
        return StaffRepository.update(db, staff)

    @staticmethod
    def get_staff_list(db: Session):
        """
        Get list of all staff members.
        
        BUSINESS LOGIC:
        - No filtering or business rules - just retrieve all staff
        - Service layer provides consistent interface (could add filtering later)
        
        USE CASE: Display staff list, pass to optimization algorithm, reports
        
        Args:
            db: Database session
        
        Returns:
            List of all Staff objects
        """
        # Simple delegation to repository
        # Could add filtering, sorting, pagination here in future
        return StaffRepository.get_all(db)

    @staticmethod
    def get_staff(db: Session, staff_id: int):
        """
        Get a single staff member by ID.
        
        BUSINESS LOGIC:
        - Validates that staff exists
        - Raises 404 error if not found (standard REST behavior)
        
        USE CASE: View staff profile, update staff (need to get first)
        
        ERROR HANDLING:
        - Raises HTTPException with 404 if staff not found
        - This is a business rule: "staff must exist to view"
        
        Args:
            db: Database session
            staff_id: ID of staff to retrieve
        
        Returns:
            Staff object if found
        
        Raises:
            HTTPException: 404 if staff not found
        """
        # Get staff from database
        staff = StaffRepository.get_by_id(db, staff_id)
        
        # Business rule: Staff must exist
        if not staff:
            raise HTTPException(status_code=404, detail="Staff not found")
        
        return staff

    @staticmethod
    def update_staff(db: Session, staff_id: int, data: StaffUpdate):
        """
        Update an existing staff member.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Update only fields that are provided (partial update)
        3. Save changes to database
        
        PARTIAL UPDATE:
        - Only updates fields that are provided (exclude_unset=True)
        - Fields not provided remain unchanged
        - This allows updating just one field (e.g., just designation)
        
        USE CASE: Update staff information (name, designation, availability, etc.)
        
        VALIDATION:
        - Staff existence validated by get_staff()
        - Field validation done by Pydantic schema (StaffUpdate)
        
        Args:
            db: Database session
            staff_id: ID of staff to update
            data: StaffUpdate schema with fields to update (only provided fields)
        
        Returns:
            Updated Staff object
        
        Raises:
            HTTPException: 404 if staff not found
        """
        # STEP 1: Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # STEP 2: Update only provided fields (partial update)
        # exclude_unset=True means only update fields that were actually provided
        # Example: If only designation provided, only update designation
        # Pydantic v1 uses .dict(), v2 uses .model_dump()
        # Check which version by trying v1 first (compatible with codebase)
        try:
            update_data = data.dict(exclude_unset=True)
        except AttributeError:
            # Pydantic v2
            update_data = data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(staff, key, value)  # staff.designation = value, etc.
        
        # STEP 3: Save changes to database
        return StaffRepository.update(db, staff)

    @staticmethod
    def delete_staff(db: Session, staff_id: int, unassign_tasks: bool = True):
        """
        Delete a staff member.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Check if staff has assignments (if unassign_tasks=False, raise error)
        3. If unassign_tasks=True, delete all assignments for this staff
        4. Delete profile picture if exists
        5. Delete staff from database
        
        USE CASE: Remove staff member (permanent deletion)
        
        WARNING: Hard delete - permanently removes record.
        Consider soft delete (is_active=False) for production.
        
        ERROR HANDLING:
        - Raises 404 if staff not found (via get_staff())
        - Raises 400 if staff has assignments and unassign_tasks=False
        
        Args:
            db: Database session
            staff_id: ID of staff to delete
            unassign_tasks: If True, automatically unassign all tasks before deletion.
                          If False, raise error if staff has assignments.
        
        Returns:
            Dictionary with deletion result:
            {
                "deleted": True,
                "unassigned_assignments": <number of assignments deleted>
            }
        
        Raises:
            HTTPException: 404 if staff not found
            HTTPException: 400 if staff has assignments and unassign_tasks=False
        """
        from app.repositories.assignment_repository import AssignmentRepository
        
        # STEP 1: Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # STEP 2: Check if staff has assignments
        assignments = AssignmentRepository.get_by_staff_id(db, staff_id)
        assignment_count = len(assignments)
        
        if assignment_count > 0:
            if not unassign_tasks:
                # Cannot delete staff with assignments
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete staff member. They have {assignment_count} active assignment(s). "
                           "Please unassign all tasks first, or use unassign_tasks=true parameter."
                )
            
            # STEP 3: Unassign all tasks (delete all assignments)
            AssignmentRepository.delete_by_staff_id(db, staff_id)
        
        # STEP 4: Delete profile picture if exists
        if staff.profile_picture_path:
            StaffService._delete_profile_picture_file(staff.profile_picture_path)
        
        # STEP 5: Delete staff from database
        StaffRepository.delete(db, staff)
        
        return {
            "deleted": True,
            "unassigned_assignments": assignment_count
        }
    
    @staticmethod
    def update_password(db: Session, staff_id: int, data: PasswordUpdate):
        """
        Update staff password.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Verify current password matches
        3. Hash new password
        4. Update password_hash in database
        
        SECURITY:
        - Current password must be provided and verified
        - New password is hashed before storing (never store plain text!)
        - Prevents unauthorized password changes
        
        USE CASE: Allow staff to change their password
        
        ERROR HANDLING:
        - Raises 404 if staff not found
        - Raises 400 if current password is incorrect
        - Raises 400 if new password is empty
        
        Args:
            db: Database session
            staff_id: ID of staff to update password for
            data: PasswordUpdate schema with current_password and new_password
        
        Returns:
            Updated Staff object
        
        Raises:
            HTTPException: 404 if staff not found
            HTTPException: 400 if current password incorrect or new password empty
        """
        # STEP 1: Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # STEP 2: Verify current password
        if not staff.password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No password set for this account"
            )
        
        if not verify_password(data.current_password, staff.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # STEP 3: Validate new password
        if not data.new_password or len(data.new_password.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password cannot be empty"
            )
        
        # STEP 4: Hash new password and update
        staff.password_hash = hash_password(data.new_password)
        
        # STEP 5: Save changes to database
        return StaffRepository.update(db, staff)
    
    @staticmethod
    def upload_profile_picture(db: Session, staff_id: int, file: UploadFile):
        """
        Upload profile picture for staff member.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Validate file type (images only)
        3. Generate unique filename
        4. Save file to uploads/profiles/ directory
        5. Delete old picture if exists
        6. Update profile_picture_path in database
        
        FILE STORAGE:
        - Files stored in: backend/uploads/profiles/
        - Filename format: staff_{staff_id}_{uuid}.{extension}
        - Example: staff_7_a1b2c3d4.jpg
        
        VALIDATION:
        - Only image files allowed (jpg, jpeg, png, gif)
        - File size limit: 5MB (configurable)
        
        USE CASE: Upload or update staff profile picture
        
        ERROR HANDLING:
        - Raises 404 if staff not found
        - Raises 400 if file type not supported
        - Raises 400 if file too large
        
        Args:
            db: Database session
            staff_id: ID of staff to upload picture for
            file: UploadFile object from FastAPI
        
        Returns:
            Updated Staff object with profile_picture_path
        
        Raises:
            HTTPException: 404 if staff not found
            HTTPException: 400 if file validation fails
        """
        # STEP 1: Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # STEP 2: Validate file type
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_extension = Path(file.filename).suffix.lower() if file.filename else ""
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # STEP 3: Validate file size (5MB limit)
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size: 5MB"
            )
        
        # STEP 4: Create uploads directory if it doesn't exist
        # Determine the correct upload directory path
        # __file__ is backend/app/services/staff_service.py, so parent.parent.parent gets backend/
        base_dir = Path(__file__).parent.parent.parent  # Go up from app/services/ to backend/
        upload_dir = base_dir / "uploads" / "profiles"
        
        # Create directory structure if it doesn't exist
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # STEP 5: Generate unique filename
        unique_id = str(uuid.uuid4())[:8]  # Short unique ID
        filename = f"staff_{staff_id}_{unique_id}{file_extension}"
        file_path = upload_dir / filename
        
        # STEP 6: Delete old picture if exists
        if staff.profile_picture_path:
            StaffService._delete_profile_picture_file(staff.profile_picture_path)
        
        # STEP 7: Save new file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
        
        # STEP 8: Update database with relative path (from uploads directory)
        # Path stored in DB: "profiles/staff_X_uuid.jpg"
        # Full path: uploads/profiles/staff_X_uuid.jpg (accessible via /uploads/profiles/...)
        relative_path = f"profiles/{filename}"
        staff.profile_picture_path = relative_path
        
        # STEP 9: Save changes to database
        return StaffRepository.update(db, staff)
    
    @staticmethod
    def delete_profile_picture(db: Session, staff_id: int):
        """
        Delete profile picture for staff member.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Delete picture file from filesystem
        3. Clear profile_picture_path in database
        
        USE CASE: Remove profile picture
        
        ERROR HANDLING:
        - Raises 404 if staff not found
        - No error if picture doesn't exist (idempotent)
        
        Args:
            db: Database session
            staff_id: ID of staff to delete picture for
        
        Returns:
            Updated Staff object with profile_picture_path = None
        
        Raises:
            HTTPException: 404 if staff not found
        """
        # STEP 1: Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # STEP 2: Delete file if exists
        if staff.profile_picture_path:
            StaffService._delete_profile_picture_file(staff.profile_picture_path)
            staff.profile_picture_path = None
            
            # STEP 3: Save changes to database
            return StaffRepository.update(db, staff)
        
        # No picture to delete - return staff as-is
        return staff
    
    @staticmethod
    def _delete_profile_picture_file(relative_path: str):
        """
        Helper method to delete profile picture file from filesystem.
        
        WHAT THIS DOES: Deletes the physical file from the uploads directory.
        
        Args:
            relative_path: Relative path to file (e.g., "profiles/staff_7.jpg")
        """
        try:
            # Determine the correct upload directory path (same logic as upload_profile_picture)
            # __file__ is backend/app/services/staff_service.py, so parent.parent.parent gets backend/
            base_dir = Path(__file__).parent.parent.parent  # Go up from app/services/ to backend/
            file_path = base_dir / "uploads" / relative_path
            
            if file_path.exists():
                file_path.unlink()  # Delete file
        except Exception:
            # Silently fail if file deletion fails (file may already be deleted)
            pass
