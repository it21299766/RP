"""
Migration Script: Add username column to staff table

This script:
1. Adds username column to staff table
2. Generates usernames for existing staff based on their role and staff_id
3. Sets default password as username for existing staff without passwords
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db_url
from app.models.staff import Staff
from app.utils.username_generator import generate_username
from app.utils.security import hash_password


def migrate():
    """Run migration to add username column and generate usernames."""
    db_url = get_db_url()
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("Starting migration: Adding username column...")
        
        # Add username column if it doesn't exist
        try:
            db.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN username VARCHAR(20) NULL
            """))
            db.commit()
            print("[OK] Added username column")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                print("[OK] Username column already exists")
            else:
                raise
        
        # Add unique index on username
        try:
            db.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_staff_username 
                ON staff(username)
            """))
            db.commit()
            print("[OK] Added unique index on username")
        except Exception as e:
            if "already exists" in str(e).lower() or "Duplicate key" in str(e):
                print("[OK] Unique index already exists")
            else:
                print(f"[WARNING] Could not create index: {e}")
        
        # Generate usernames for existing staff
        print("\nGenerating usernames for existing staff...")
        all_staff = db.query(Staff).order_by(Staff.staff_id).all()
        
        updated_count = 0
        password_set_count = 0
        used_usernames = set()
        
        for staff in all_staff:
            if not staff.username:
                # Generate username (check against already used usernames in this batch)
                role_upper = staff.role.upper()
                if role_upper in ["ADMIN", "MANAGEMENT"]:
                    prefix = "adm"
                else:
                    prefix = "sf"
                
                username = f"{prefix}{staff.staff_id}"
                
                # Ensure uniqueness within this batch
                counter = 1
                while username in used_usernames or db.query(Staff).filter(Staff.username == username).first():
                    username = f"{prefix}{staff.staff_id}_{counter}"
                    counter += 1
                    if counter > 999:
                        raise ValueError(f"Could not generate unique username for staff_id {staff.staff_id}")
                
                staff.username = username
                used_usernames.add(username)
                updated_count += 1
                print(f"  Generated username for {staff.name} (ID: {staff.staff_id}): {staff.username}")
            
            # Set default password if not set
            if not staff.password_hash and staff.username:
                default_password = staff.username
                staff.password_hash = hash_password(default_password)
                password_set_count += 1
                print(f"  Set default password for {staff.name}: {staff.username}")
        
        db.commit()
        
        print(f"\n[SUCCESS] Migration completed successfully!")
        print(f"  - Updated {updated_count} staff members with usernames")
        print(f"  - Set default passwords for {password_set_count} staff members")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Migration failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()

