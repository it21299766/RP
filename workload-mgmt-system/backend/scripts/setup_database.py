"""
Database Setup Script

This script:
1. Creates all tables if they don't exist (using SQLAlchemy)
2. Adds missing columns to existing tables
3. Ensures the database schema matches the models

Run this before seeding data.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from app.database import get_db_url, Base, engine
from app.models import staff, domain, program, program_section, task_template, task_instance
from app.models import assignment, designation_workload_policy, staff_availability


def get_table_columns(db, table_name):
    """Get list of column names for a table."""
    try:
        result = db.execute(text(f"SHOW COLUMNS FROM {table_name}"))
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"  [WARNING] Could not get columns for {table_name}: {e}")
        return []


def setup_staff_table(db):
    """Ensure staff table has all required columns."""
    print("Setting up staff table...")
    
    columns = get_table_columns(db, 'staff')
    required_columns = {
        'designation': "VARCHAR(50) NULL",
        'specialization': "VARCHAR(100) NULL",
        'experience_years': "INT DEFAULT 0",
        'username': "VARCHAR(20) NULL",
        'qualification': "VARCHAR(10) NULL",
    }
    
    for col_name, col_def in required_columns.items():
        if col_name not in columns:
            try:
                db.execute(text(f"ALTER TABLE staff ADD COLUMN {col_name} {col_def}"))
                db.commit()
                print(f"  [OK] Added column: {col_name}")
            except Exception as e:
                if "Duplicate column" in str(e) or "already exists" in str(e).lower():
                    print(f"  [OK] Column {col_name} already exists")
                else:
                    print(f"  [ERROR] Error adding {col_name}: {e}")
                    raise
        else:
            print(f"  [OK] Column {col_name} already exists")
    
    # Set default values for existing rows
    try:
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
        db.execute(text("""
            UPDATE staff 
            SET qualification = 'MSc' 
            WHERE qualification IS NULL
        """))
        db.commit()
        print("  [OK] Set default values for existing rows")
    except Exception as e:
        print(f"  [WARNING] Warning setting defaults: {e}")
    
    # Make columns NOT NULL after setting defaults
    try:
        db.execute(text("ALTER TABLE staff MODIFY COLUMN designation VARCHAR(50) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN specialization VARCHAR(100) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN qualification VARCHAR(10) NOT NULL"))
        db.commit()
        print("  [OK] Set columns as NOT NULL")
    except Exception as e:
        print(f"  [WARNING] Warning setting NOT NULL: {e}")
    
    # Add unique index on username (MySQL doesn't support IF NOT EXISTS for indexes)
    try:
        # Check if index exists first
        result = db.execute(text("SHOW INDEX FROM staff WHERE Key_name = 'idx_staff_username'"))
        if not result.fetchone():
            db.execute(text("CREATE UNIQUE INDEX idx_staff_username ON staff(username)"))
            db.commit()
            print("  [OK] Added unique index on username")
        else:
            print("  [OK] Unique index on username already exists")
    except Exception as e:
        if "already exists" in str(e).lower() or "Duplicate key" in str(e) or "Duplicate index" in str(e):
            print("  [OK] Unique index on username already exists")
        else:
            print(f"  [WARNING] Warning creating index: {e}")


def setup_all_tables():
    """Create all tables and ensure they have correct schema."""
    print("=" * 60)
    print("Database Setup Script")
    print("=" * 60)
    print()
    
    # First, create all tables (SQLAlchemy will skip if they exist)
    print("Creating tables (if they don't exist)...")
    try:
        Base.metadata.create_all(bind=engine)
        print("  [OK] Tables created/verified")
    except Exception as e:
        print(f"  [WARNING] Warning creating tables: {e}")
    
    print()
    
    # Then, ensure staff table has all columns
    db_url = get_db_url()
    engine_check = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine_check)
    db = SessionLocal()
    
    try:
        setup_staff_table(db)
        print()
        print("=" * 60)
        print("[SUCCESS] Database setup completed successfully!")
        print("=" * 60)
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    setup_all_tables()

