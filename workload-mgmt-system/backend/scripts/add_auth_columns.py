"""
Migration script to add authentication columns to staff table.
This script safely adds password_hash and is_active columns to existing staff table.

Usage:
    python -m scripts.add_auth_columns
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine, SessionLocal


def add_auth_columns():
    """
    Add password_hash and is_active columns to staff table.
    This is safe to run multiple times (checks if columns exist first).
    """
    db = SessionLocal()
    try:
        # Check if columns already exist
        with engine.connect() as conn:
            # Get existing columns
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'staff'
            """))
            existing_columns = [row[0] for row in result]
            
            # Add password_hash column if it doesn't exist
            if 'password_hash' not in existing_columns:
                print("Adding password_hash column...")
                conn.execute(text("""
                    ALTER TABLE staff 
                    ADD COLUMN password_hash VARCHAR(255) NULL
                """))
                conn.commit()
                print("[OK] password_hash column added successfully")
            else:
                print("[OK] password_hash column already exists")
            
            # Add is_active column if it doesn't exist
            if 'is_active' not in existing_columns:
                print("Adding is_active column...")
                conn.execute(text("""
                    ALTER TABLE staff 
                    ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE
                """))
                conn.commit()
                print("[OK] is_active column added successfully")
            else:
                print("[OK] is_active column already exists")
            
            # Update existing records to have is_active = TRUE if NULL
            conn.execute(text("""
                UPDATE staff 
                SET is_active = TRUE 
                WHERE is_active IS NULL
            """))
            conn.commit()
            print("[OK] Updated existing staff records (is_active = TRUE)")
            
        print("\n[SUCCESS] Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error during migration: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Staff Table Migration: Adding Authentication Columns")
    print("=" * 60)
    print()
    
    success = add_auth_columns()
    
    if success:
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Set passwords for existing staff using:")
        print("   python -m scripts.set_staff_password <staff_id> <password>")
        print("2. Restart your FastAPI server")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("Migration failed. Please check the error message above.")
        print("=" * 60)
        sys.exit(1)

