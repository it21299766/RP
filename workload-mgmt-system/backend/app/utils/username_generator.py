"""
Username Generator Utility

Generates usernames for staff members based on their role and staff_id.
Format:
- ACADEMIC: sf1, sf2, sf10, ... (lowercase "sf" + staff_id)
- ADMIN: adm1, adm2, adm10, ... (lowercase "adm" + staff_id)
- MANAGEMENT: adm1, adm2, adm10, ... (same as ADMIN)
"""

from sqlalchemy.orm import Session
from app.models.staff import Staff


def generate_username(role: str, staff_id: int, db: Session = None) -> str:
    """
    Generate a username based on role and staff_id.
    
    Args:
        role: Staff role (ACADEMIC, ADMIN, MANAGEMENT)
        staff_id: Staff ID (integer)
        db: Optional database session to check for uniqueness
        
    Returns:
        Generated username string
    """
    role_upper = role.upper()
    
    if role_upper in ["ADMIN", "MANAGEMENT"]:
        # Format: adm1, adm2, adm10, ...
        prefix = "adm"
    else:
        # Format: sf1, sf2, sf10, ... (ACADEMIC)
        prefix = "sf"
    
    username = f"{prefix}{staff_id}"
    
    # Check for uniqueness if db session provided
    if db:
        counter = 1
        original_username = username
        while db.query(Staff).filter(Staff.username == username).first():
            username = f"{prefix}{staff_id}_{counter}"
            counter += 1
            if counter > 999:  # Safety limit
                raise ValueError("Could not generate unique username")
    
    return username

