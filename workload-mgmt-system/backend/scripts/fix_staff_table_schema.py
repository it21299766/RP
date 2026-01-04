"""
Fix Staff Table Schema

This script fixes the staff table to match the current model:
- Renames 'specialty' to 'specialization' if it exists
- Adds missing columns
- Sets proper defaults
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db_url


def fix_staff_table():
    """Fix staff table schema to match the model."""
    print("=" * 60)
    print("Fixing Staff Table Schema")
    print("=" * 60)
    print()
    
    db_url = get_db_url()
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get current columns
        result = db.execute(text("SHOW COLUMNS FROM staff"))
        columns = {row[0]: row for row in result.fetchall()}
        print(f"Current columns: {list(columns.keys())}")
        print()
        
        # Handle specialty column - either rename or make nullable
        if 'specialty' in columns:
            print("Handling 'specialty' column...")
            # If specialization doesn't exist, copy data from specialty
            if 'specialization' not in columns:
                try:
                    db.execute(text("ALTER TABLE staff ADD COLUMN specialization VARCHAR(100) NULL"))
                    db.execute(text("UPDATE staff SET specialization = specialty WHERE specialty IS NOT NULL"))
                    db.execute(text("UPDATE staff SET specialization = 'General' WHERE specialization IS NULL"))
                    db.commit()
                    print("  [OK] Added specialization column and copied data from specialty")
                except Exception as e:
                    print(f"  [WARNING] Could not add specialization: {e}")
            # Make specialty nullable or drop it (since we're using specialization now)
            try:
                db.execute(text("ALTER TABLE staff MODIFY COLUMN specialty VARCHAR(100) NULL"))
                db.commit()
                print("  [OK] Made specialty column nullable")
            except Exception as e:
                print(f"  [WARNING] Could not modify specialty: {e}")
        
        # Handle experience column - copy to experience_years if needed
        if 'experience' in columns and 'experience_years' not in columns:
            print("Copying 'experience' to 'experience_years'...")
            try:
                db.execute(text("ALTER TABLE staff ADD COLUMN experience_years INT DEFAULT 0"))
                db.execute(text("UPDATE staff SET experience_years = experience WHERE experience IS NOT NULL"))
                db.commit()
                print("  [OK] Added experience_years and copied data")
            except Exception as e:
                print(f"  [WARNING] Could not copy experience: {e}")
        
        # Add missing columns
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
            else:
                print(f"  [OK] Column {col_name} already exists")
        
        # Set default values for existing rows
        print()
        print("Setting default values...")
        try:
            db.execute(text("UPDATE staff SET designation = 'Lecturer' WHERE designation IS NULL"))
            db.execute(text("UPDATE staff SET specialization = COALESCE(specialization, 'General') WHERE specialization IS NULL"))
            db.execute(text("UPDATE staff SET experience_years = 0 WHERE experience_years IS NULL"))
            db.execute(text("UPDATE staff SET qualification = 'MSc' WHERE qualification IS NULL"))
            db.commit()
            print("  [OK] Set default values")
        except Exception as e:
            print(f"  [WARNING] Warning setting defaults: {e}")
        
        # Make columns NOT NULL after setting defaults
        print()
        print("Setting columns as NOT NULL...")
        try:
            db.execute(text("ALTER TABLE staff MODIFY COLUMN designation VARCHAR(50) NOT NULL"))
            db.execute(text("ALTER TABLE staff MODIFY COLUMN specialization VARCHAR(100) NOT NULL"))
            db.execute(text("ALTER TABLE staff MODIFY COLUMN qualification VARCHAR(10) NOT NULL"))
            db.commit()
            print("  [OK] Set columns as NOT NULL")
        except Exception as e:
            print(f"  [WARNING] Warning setting NOT NULL: {e}")
        
        # Add unique index on username
        print()
        print("Adding unique index on username...")
        try:
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
        
        print()
        print("=" * 60)
        print("[SUCCESS] Staff table schema fixed successfully!")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_staff_table()

