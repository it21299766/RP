"""
Migration Script: Add task_instance_id to assignments table

This script adds the task_instance_id column to the assignments table.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db_url


def migrate():
    """Run migration to add task_instance_id column."""
    db_url = get_db_url()
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("Starting migration: Adding task_instance_id to assignments table...")
        
        # Make task_id nullable first (it's legacy, task_instance_id is the new one)
        try:
            db.execute(text("""
                ALTER TABLE assignments 
                MODIFY COLUMN task_id INT NULL
            """))
            db.commit()
            print("[OK] Made task_id column nullable")
        except Exception as e:
            if "Duplicate column" in str(e) or "already exists" in str(e).lower():
                print("[OK] task_id is already nullable")
            else:
                print(f"[WARNING] Could not make task_id nullable: {e}")
        
        # Check if task_instance_id column exists
        result = db.execute(text("SHOW COLUMNS FROM assignments LIKE 'task_instance_id'"))
        if result.fetchone():
            print("[OK] task_instance_id column already exists")
        else:
            # Add task_instance_id column
            db.execute(text("""
                ALTER TABLE assignments 
                ADD COLUMN task_instance_id INT NULL
            """))
            db.commit()
            print("[OK] Added task_instance_id column")
            
            # Add foreign key constraint
            try:
                db.execute(text("""
                    ALTER TABLE assignments 
                    ADD CONSTRAINT fk_assignments_task_instance 
                    FOREIGN KEY (task_instance_id) REFERENCES task_instances(id)
                """))
                db.commit()
                print("[OK] Added foreign key constraint")
            except Exception as e:
                if "Duplicate key" in str(e) or "already exists" in str(e).lower():
                    print("[OK] Foreign key constraint already exists")
                else:
                    print(f"[WARNING] Could not add foreign key: {e}")
            
            # Make task_id nullable (it's legacy, task_instance_id is the new one)
            try:
                db.execute(text("""
                    ALTER TABLE assignments 
                    MODIFY COLUMN task_id INT NULL
                """))
                db.commit()
                print("[OK] Made task_id column nullable")
            except Exception as e:
                print(f"[WARNING] Could not make task_id nullable: {e}")
        
        print("\n[SUCCESS] Migration completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()

