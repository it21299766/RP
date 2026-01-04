"""
Utility script to set or update staff passwords.
This is useful for initial setup or password resets.

Usage:
    python -m scripts.set_staff_password <staff_id> <password>
    
Example:
    python -m scripts.set_staff_password 1 admin123
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.staff import Staff
from app.utils.security import hash_password


def set_staff_password(staff_id: int, password: str):
    """
    Set or update password for a staff member.
    
    Args:
        staff_id: Staff ID
        password: Plain text password to set
    """
    db: Session = SessionLocal()
    try:
        # Find staff member
        staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        
        if not staff:
            print(f"Error: Staff with ID {staff_id} not found.")
            return False
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Update staff password
        staff.password_hash = hashed_password
        staff.is_active = True  # Ensure staff is active
        
        db.commit()
        print(f"Success: Password set for staff ID {staff_id} ({staff.name})")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error: Failed to set password - {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m scripts.set_staff_password <staff_id> <password>")
        print("Example: python -m scripts.set_staff_password 1 admin123")
        sys.exit(1)
    
    try:
        staff_id = int(sys.argv[1])
        password = sys.argv[2]
        
        if len(password) < 4:
            print("Error: Password must be at least 4 characters long.")
            sys.exit(1)
        
        # Initialize database
        init_db()
        
        # Set password
        success = set_staff_password(staff_id, password)
        sys.exit(0 if success else 1)
        
    except ValueError:
        print("Error: Staff ID must be a number.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

