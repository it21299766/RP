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
from fastapi import HTTPException, status
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from app.repositories.staff_repository import StaffRepository
from app.utils.security import hash_password
from app.utils.username_generator import generate_username


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
        for key, value in data.dict(exclude_unset=True).items():
            setattr(staff, key, value)  # staff.designation = value, etc.
        
        # STEP 3: Save changes to database
        return StaffRepository.update(db, staff)

    @staticmethod
    def delete_staff(db: Session, staff_id: int):
        """
        Delete a staff member.
        
        BUSINESS LOGIC:
        1. Get staff (validates existence - raises 404 if not found)
        2. Delete from database
        
        USE CASE: Remove staff member (permanent deletion)
        
        WARNING: Hard delete - permanently removes record.
        Consider soft delete (is_active=False) for production.
        
        ERROR HANDLING:
        - Raises 404 if staff not found (via get_staff())
        - May fail if staff has related records (foreign key constraints)
        
        Args:
            db: Database session
            staff_id: ID of staff to delete
        
        Returns:
            None (void operation)
        
        Raises:
            HTTPException: 404 if staff not found
        """
        # Get staff (validates existence)
        staff = StaffService.get_staff(db, staff_id)
        
        # Delete from database
        StaffRepository.delete(db, staff)
