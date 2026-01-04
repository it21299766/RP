"""
Migration Script: Add missing columns to staff table

This script adds the new columns required by the updated Staff model:
- designation
- specialization
- experience_years
- username (if not already added)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db_url


def migrate():
    """Run migration to add missing columns to staff table."""
    db_url = get_db_url()
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("Starting migration: Adding missing columns to staff table...")
        
        # Check and add designation column
        try:
            db.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN designation VARCHAR(50) NULL
            """))
            db.commit()
            print("✓ Added designation column")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                print("✓ Designation column already exists")
            else:
                raise
        
        # Check and add specialization column
        try:
            db.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN specialization VARCHAR(100) NULL
            """))
            db.commit()
            print("✓ Added specialization column")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                print("✓ Specialization column already exists")
            else:
                raise
        
        # Check and add experience_years column
        try:
            db.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN experience_years INT DEFAULT 0
            """))
            db.commit()
            print("✓ Added experience_years column")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                print("✓ Experience_years column already exists")
            else:
                raise
        
        # Check and add username column (if not already added)
        try:
            db.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN username VARCHAR(20) NULL
            """))
            db.commit()
            print("✓ Added username column")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                print("✓ Username column already exists")
            else:
                raise
        
        # Add unique index on username if it doesn't exist
        try:
            db.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_staff_username 
                ON staff(username)
            """))
            db.commit()
            print("✓ Added unique index on username")
        except Exception as e:
            if "already exists" in str(e).lower() or "Duplicate key" in str(e):
                print("✓ Unique index on username already exists")
            else:
                print(f"Warning: Could not create index: {e}")
        
        # Update existing staff to have default values if needed
        db.execute(text("""
            UPDATE staff 
            SET designation = 'Lecturer' 
            WHERE designation IS NULL
        """))
        
        db.execute(text("""
            UPDATE staff 
            SET specialization = 'General' 
            WHERE specialization IS NULL
        """))
        
        db.execute(text("""
            UPDATE staff 
            SET experience_years = 0 
            WHERE experience_years IS NULL
        """))
        
        # Make designation and specialization NOT NULL after setting defaults
        try:
            db.execute(text("""
                ALTER TABLE staff 
                MODIFY COLUMN designation VARCHAR(50) NOT NULL
            """))
            db.commit()
            print("✓ Set designation as NOT NULL")
        except Exception as e:
            print(f"Warning: Could not set designation as NOT NULL: {e}")
        
        try:
            db.execute(text("""
                ALTER TABLE staff 
                MODIFY COLUMN specialization VARCHAR(100) NOT NULL
            """))
            db.commit()
            print("✓ Set specialization as NOT NULL")
        except Exception as e:
            print(f"Warning: Could not set specialization as NOT NULL: {e}")
        
        db.commit()
        print(f"\n✓ Migration completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()

