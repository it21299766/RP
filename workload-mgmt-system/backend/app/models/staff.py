"""
Staff Model - Represents Staff Members in the University

This model stores all information about staff members including:
- Personal information (name, username)
- Academic qualifications and experience
- Workload capacity and availability
- Authentication credentials

THINK OF IT AS: An employee record/HR file for each staff member.
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, JSON
from app.database import Base


class Staff(Base):
    """
    Staff Model - Database table representing staff members.
    
    Each row represents one staff member with all their information.
    Used for authentication, workload allocation, and staff management.
    """
    __tablename__ = "staff"

    # PRIMARY KEY: Unique identifier for each staff member
    # SIGNIFICANCE: Used to link staff to assignments, availability, etc.
    # USECASE: Foreign key in assignments table, used in authentication tokens
    staff_id = Column(Integer, primary_key=True, index=True)
    
    # USERNAME: Login identifier for authentication
    # SIGNIFICANCE: Used for login instead of staff_id (more user-friendly)
    # FORMAT: "sf" + staff_id for academic staff (e.g., "sf1", "sf7")
    #         "adm" + staff_id for admin/management (e.g., "adm1", "adm15")
    # USECASE: Primary login credential, must be unique
    # EXAMPLE: Academic staff with staff_id=7 has username="sf7"
    username = Column(String(20), unique=True, nullable=True, index=True)

    # NAME: Full name of the staff member
    # SIGNIFICANCE: Display name in the system
    # USECASE: Shown in reports, assignments, staff listings
    # EXAMPLE: "Dr. John Smith"
    name = Column(String(100), nullable=False)

    # DESIGNATION: Academic rank/position
    # SIGNIFICANCE: Determines workload limits (via DesignationWorkloadPolicy)
    # USECASE: Used to look up maximum hours from workload policy table
    # EXAMPLES: "Professor", "Associate Professor", "Senior Lecturer I", 
    #           "Senior Lecturer II", "Lecturer", "Head of Department"
    # NOTE: Different designations have different max hours (professors usually less teaching)
    designation = Column(String(50), nullable=False)

    # QUALIFICATION: Highest academic degree
    # SIGNIFICANCE: HARD CONSTRAINT - determines which tasks staff can be assigned
    # USECASE: Qualification matching (PhD can teach MSc tasks, but BSc cannot)
    # VALUES: "BSc", "MSc", "PhD"
    # HIERARCHY: PhD > MSc > BSc (PhD can do MSc/BSc tasks, MSc can do BSc tasks)
    # EXAMPLE: Staff with PhD can be assigned to tasks requiring MSc or BSc
    qualification = Column(String(10), nullable=False)

    # SPECIALIZATION: Field of expertise
    # SIGNIFICANCE: SOFT CONSTRAINT - preferred matching for task assignments
    # USECASE: GA algorithm gives bonuses when staff specialty matches task requirements
    # EXAMPLES: "Computer Science", "Physics", "Mathematics", "Software Engineering"
    # NOTE: Not required to match, but preferred (better assignments)
    specialization = Column(String(100), nullable=False)

    # DEPARTMENT: Academic department the staff belongs to
    # SIGNIFICANCE: Organizational grouping, used in reports and filtering
    # USECASE: Filter staff by department, generate department-level reports
    # EXAMPLES: "Computer Science", "Mathematics", "Physics"
    department = Column(String(100), nullable=False)

    # ROLE: System access level and responsibilities
    # SIGNIFICANCE: Determines what the user can access in the system
    # USECASE: Role-based access control (RBAC) - different permissions for different roles
    # VALUES: 
    #   - "ACADEMIC": Teaching staff, can view own workload, request changes
    #   - "ADMIN": Administrators, full access to all features
    #   - "MANAGEMENT": Management staff, can view reports, approve changes
    # NOTE: Used in authentication to determine permissions
    role = Column(String(20), nullable=False)

    # EXPERIENCE_YEARS: Years of professional experience
    # SIGNIFICANCE: SOFT CONSTRAINT - used in task assignment matching
    # USECASE: GA algorithm gives bonuses when staff experience >= task requirement
    # EXAMPLE: 5 years experience can handle tasks requiring 3 years
    # NOTE: More experience = better match score in optimization
    experience_years = Column(Integer, default=0)

    # SKILLS: List of technical/professional skills
    # SIGNIFICANCE: SOFT CONSTRAINT - used for task matching
    # FORMAT: JSON array of strings
    # USECASE: GA algorithm matches staff skills with task required skills
    # EXAMPLES: ["Python", "Java", "Machine Learning", "Database Design"]
    # NOTE: More matching skills = better assignment score
    skills = Column(JSON, default=list)
    
    # MAX_HOURS: Maximum teaching hours (DEPRECATED)
    # SIGNIFICANCE: Old way of storing workload limits (kept for backward compatibility)
    # USECASE: Legacy data, being replaced by DesignationWorkloadPolicy
    # NOTE: New system uses designation → workload policy lookup instead
    # STATUS: Deprecated - use DesignationWorkloadPolicy table instead
    max_hours = Column(Float, nullable=True)

    # AVAILABLE: Whether staff is currently available for new assignments
    # SIGNIFICANCE: Prevents assigning tasks to unavailable staff
    # USECASE: Set to False for staff on leave, sabbatical, or temporarily unavailable
    # NOTE: GA algorithm skips unavailable staff when generating assignments
    # EXAMPLE: Staff on maternity leave would have available=False
    available = Column(Boolean, default=True)
    
    # PASSWORD_HASH: Hashed password for authentication
    # SIGNIFICANCE: Stores encrypted password (never store plain text!)
    # FORMAT: bcrypt hash (e.g., "$2b$12$LQv3c1yqBWVHxkd0LHAkCO...")
    # USECASE: Password verification during login
    # SECURITY: Nullable for existing staff without passwords (must be set before login)
    # NOTE: Default password is username (set during staff creation)
    password_hash = Column(String(255), nullable=True)

    # IS_ACTIVE: Whether the account is active
    # SIGNIFICANCE: Allows disabling accounts without deleting them
    # USECASE: 
    #   - Set to False to disable login (retired staff, terminated employees)
    #   - Prevents authentication even with correct password
    #   - Useful for soft-deletion (keep data, disable access)
    # NOTE: Inactive accounts cannot login or access the system
    is_active = Column(Boolean, default=True, nullable=False)
    
    # PROFILE_PICTURE_PATH: Path to profile picture file
    # SIGNIFICANCE: Stores the file path/URL for the staff member's profile picture
    # FORMAT: Relative path from uploads directory (e.g., "profiles/staff_7.jpg")
    # USECASE: Display profile picture in UI, staff listings, reports
    # NOTE: Nullable - staff may not have a profile picture
    # EXAMPLE: "profiles/staff_7.jpg" or "profiles/staff_15.png"
    profile_picture_path = Column(String(255), nullable=True)
