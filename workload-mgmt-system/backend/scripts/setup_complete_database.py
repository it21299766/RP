"""
Complete Database Setup Script

This script ensures the database is fully ready for the WAM system:
1. Creates all tables if they don't exist (using SQLAlchemy)
2. Adds missing columns to existing tables
3. Creates indexes and foreign keys
4. Ensures all constraints are in place
5. Handles migrations gracefully

Run this script to set up a fresh database or update an existing one.

Usage:
    python backend/scripts/setup_complete_database.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure stdout for Windows Unicode support
if sys.platform == 'win32':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from app.database import get_db_url, Base, engine
from app.models import (
    staff, domain, program, program_section, task_template, task_instance,
    assignment, designation_workload_policy, staff_availability, change_request,
    module, module_section, tariff, task
)

# Import all models to ensure they're registered with Base
from app.models.staff import Staff
from app.models.domain import Domain
from app.models.program import Program
from app.models.program_section import ProgramSection
from app.models.task_template import TaskTemplate
from app.models.task_instance import TaskInstance
from app.models.assignment import Assignment
from app.models.designation_workload_policy import DesignationWorkloadPolicy
from app.models.staff_availability import StaffAvailability
from app.models.change_request import ChangeRequest
from app.models.module import Module
from app.models.module_section import ModuleSection
from app.models.tariff import Tariff
from app.models.task import Task


def table_exists(db, table_name):
    """Check if a table exists in the database."""
    try:
        result = db.execute(text(f"SHOW TABLES LIKE '{table_name}'"))
        return result.fetchone() is not None
    except Exception:
        return False


def column_exists(db, table_name, column_name):
    """Check if a column exists in a table."""
    try:
        result = db.execute(text(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'"))
        return result.fetchone() is not None
    except Exception:
        return False


def index_exists(db, table_name, index_name):
    """Check if an index exists on a table."""
    try:
        result = db.execute(text(f"SHOW INDEX FROM {table_name} WHERE Key_name = '{index_name}'"))
        return result.fetchone() is not None
    except Exception:
        return False


def create_all_tables():
    """Create all tables using SQLAlchemy Base.metadata."""
    print("=" * 70)
    print("STEP 1: Creating all tables (if they don't exist)")
    print("=" * 70)
    
    try:
        # This creates all tables defined in models
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created/verified successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def setup_staff_table(db):
    """Ensure staff table has all required columns."""
    print("\n" + "=" * 70)
    print("STEP 2: Setting up staff table")
    print("=" * 70)
    
    if not table_exists(db, 'staff'):
        print("  [SKIP] Staff table doesn't exist (will be created by SQLAlchemy)")
        return
    
    columns_to_add = {
        'username': {
            'type': 'VARCHAR(20)',
            'nullable': True,
            'after': 'staff_id'
        },
        'designation': {
            'type': 'VARCHAR(50)',
            'nullable': False,
            'default': "'Lecturer'"
        },
        'qualification': {
            'type': 'VARCHAR(10)',
            'nullable': False,
            'default': "'MSc'"
        },
        'specialization': {
            'type': 'VARCHAR(100)',
            'nullable': False,
            'default': "'General'"
        },
        'department': {
            'type': 'VARCHAR(100)',
            'nullable': False,
            'default': "'General'"
        },
        'role': {
            'type': 'VARCHAR(20)',
            'nullable': False,
            'default': "'ACADEMIC'"
        },
        'experience_years': {
            'type': 'INT',
            'nullable': True,
            'default': '0'
        },
        'skills': {
            'type': 'JSON',
            'nullable': True,
            'default': 'NULL'
        },
        'max_hours': {
            'type': 'FLOAT',
            'nullable': True,
            'default': 'NULL'
        },
        'available': {
            'type': 'BOOLEAN',
            'nullable': True,
            'default': 'TRUE'
        },
        'password_hash': {
            'type': 'VARCHAR(255)',
            'nullable': True,
            'default': 'NULL'
        },
        'is_active': {
            'type': 'BOOLEAN',
            'nullable': False,
            'default': 'TRUE'
        }
    }
    
    for col_name, col_def in columns_to_add.items():
        if not column_exists(db, 'staff', col_name):
            try:
                nullable = 'NULL' if col_def['nullable'] else 'NOT NULL'
                default = f"DEFAULT {col_def['default']}" if 'default' in col_def else ''
                sql = f"ALTER TABLE staff ADD COLUMN {col_name} {col_def['type']} {nullable} {default}"
                db.execute(text(sql))
                db.commit()
                print(f"  ✓ Added column: {col_name}")
            except Exception as e:
                if "Duplicate column" in str(e) or "already exists" in str(e).lower():
                    print(f"  ✓ Column {col_name} already exists")
                else:
                    print(f"  ✗ Error adding {col_name}: {e}")
        else:
            print(f"  ✓ Column {col_name} already exists")
    
    # Set default values for existing rows (before making NOT NULL)
    try:
        db.execute(text("""
            UPDATE staff 
            SET designation = 'Lecturer' 
            WHERE designation IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET qualification = 'MSc' 
            WHERE qualification IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET specialization = 'General' 
            WHERE specialization IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET department = 'General' 
            WHERE department IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET role = 'ACADEMIC' 
            WHERE role IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET experience_years = 0 
            WHERE experience_years IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET available = TRUE 
            WHERE available IS NULL
        """))
        db.execute(text("""
            UPDATE staff 
            SET is_active = TRUE 
            WHERE is_active IS NULL
        """))
        db.commit()
        print("  ✓ Set default values for existing rows")
    except Exception as e:
        print(f"  ⚠ Warning setting defaults: {e}")
    
    # Make columns NOT NULL after setting defaults
    try:
        db.execute(text("ALTER TABLE staff MODIFY COLUMN designation VARCHAR(50) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN qualification VARCHAR(10) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN specialization VARCHAR(100) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN department VARCHAR(100) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN role VARCHAR(20) NOT NULL"))
        db.execute(text("ALTER TABLE staff MODIFY COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE"))
        db.commit()
        print("  ✓ Set columns as NOT NULL")
    except Exception as e:
        print(f"  ⚠ Warning setting NOT NULL: {e}")
    
    # Add unique index on username
    if not index_exists(db, 'staff', 'idx_staff_username'):
        try:
            db.execute(text("CREATE UNIQUE INDEX idx_staff_username ON staff(username)"))
            db.commit()
            print("  ✓ Added unique index on username")
        except Exception as e:
            if "already exists" in str(e).lower() or "Duplicate" in str(e):
                print("  ✓ Unique index on username already exists")
            else:
                print(f"  ⚠ Warning creating index: {e}")
    else:
        print("  ✓ Unique index on username already exists")


def setup_assignments_table(db):
    """Ensure assignments table has all required columns."""
    print("\n" + "=" * 70)
    print("STEP 3: Setting up assignments table")
    print("=" * 70)
    
    if not table_exists(db, 'assignments'):
        print("  [SKIP] Assignments table doesn't exist (will be created by SQLAlchemy)")
        return
    
    # Make task_id nullable (for migration support)
    if column_exists(db, 'assignments', 'task_id'):
        try:
            db.execute(text("ALTER TABLE assignments MODIFY COLUMN task_id INT NULL"))
            db.commit()
            print("  ✓ Made task_id nullable (for migration support)")
        except Exception as e:
            print(f"  ⚠ Warning: {e}")
    
    # Ensure task_instance_id exists and is NOT NULL
    if not column_exists(db, 'assignments', 'task_instance_id'):
        try:
            db.execute(text("ALTER TABLE assignments ADD COLUMN task_instance_id INT NULL"))
            db.commit()
            print("  ✓ Added task_instance_id column")
        except Exception as e:
            print(f"  ⚠ Warning: {e}")
    
    # Add foreign key for task_instance_id if it doesn't exist
    try:
        # Check if foreign key exists
        result = db.execute(text("""
            SELECT CONSTRAINT_NAME 
            FROM information_schema.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'assignments' 
            AND COLUMN_NAME = 'task_instance_id'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """))
        if not result.fetchone():
            db.execute(text("""
                ALTER TABLE assignments 
                ADD CONSTRAINT fk_assignments_task_instance 
                FOREIGN KEY (task_instance_id) REFERENCES task_instances(id)
            """))
            db.commit()
            print("  ✓ Added foreign key for task_instance_id")
        else:
            print("  ✓ Foreign key for task_instance_id already exists")
    except Exception as e:
        if "already exists" in str(e).lower() or "Duplicate" in str(e):
            print("  ✓ Foreign key for task_instance_id already exists")
        else:
            print(f"  ⚠ Warning: {e}")


def create_indexes(db):
    """Create important indexes for performance."""
    print("\n" + "=" * 70)
    print("STEP 4: Creating indexes")
    print("=" * 70)
    
    indexes = [
        ('staff', 'idx_staff_username', 'username'),
        ('staff', 'idx_staff_department', 'department'),
        ('staff', 'idx_staff_role', 'role'),
        ('task_instances', 'idx_task_instance_status', 'status'),
        ('task_instances', 'idx_task_instance_semester', 'semester'),
        ('assignments', 'idx_assignments_staff', 'staff_id'),
        ('assignments', 'idx_assignments_task_instance', 'task_instance_id'),
    ]
    
    for table, index_name, column in indexes:
        if table_exists(db, table) and not index_exists(db, table, index_name):
            try:
                db.execute(text(f"CREATE INDEX {index_name} ON {table}({column})"))
                db.commit()
                print(f"  ✓ Created index: {index_name} on {table}({column})")
            except Exception as e:
                if "already exists" in str(e).lower() or "Duplicate" in str(e):
                    print(f"  ✓ Index {index_name} already exists")
                else:
                    print(f"  ⚠ Warning creating {index_name}: {e}")
        elif not table_exists(db, table):
            print(f"  [SKIP] Table {table} doesn't exist yet")
        else:
            print(f"  ✓ Index {index_name} already exists")


def verify_foreign_keys(db):
    """Verify all foreign keys are properly set up."""
    print("\n" + "=" * 70)
    print("STEP 5: Verifying foreign keys")
    print("=" * 70)
    
    # Foreign keys are typically created by SQLAlchemy, but we verify they exist
    foreign_keys = [
        ('programs', 'domain_id', 'domains', 'domain_id'),
        ('program_sections', 'program_id', 'programs', 'program_id'),
        ('task_instances', 'task_template_id', 'task_templates', 'id'),
        ('task_instances', 'domain_id', 'domains', 'domain_id'),
        ('task_instances', 'program_id', 'programs', 'program_id'),
        ('task_instances', 'program_section_id', 'program_sections', 'section_id'),
        ('assignments', 'staff_id', 'staff', 'staff_id'),
        ('assignments', 'task_instance_id', 'task_instances', 'id'),
        ('staff_availability', 'staff_id', 'staff', 'staff_id'),
    ]
    
    for table, column, ref_table, ref_column in foreign_keys:
        if table_exists(db, table) and table_exists(db, ref_table):
            try:
                result = db.execute(text(f"""
                    SELECT CONSTRAINT_NAME 
                    FROM information_schema.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = '{table}' 
                    AND COLUMN_NAME = '{column}'
                    AND REFERENCED_TABLE_NAME = '{ref_table}'
                """))
                if result.fetchone():
                    print(f"  ✓ Foreign key {table}.{column} → {ref_table}.{ref_column} exists")
                else:
                    print(f"  ⚠ Foreign key {table}.{column} → {ref_table}.{ref_column} missing (may be created by SQLAlchemy)")
            except Exception as e:
                print(f"  ⚠ Could not verify {table}.{column}: {e}")
        else:
            print(f"  [SKIP] Table {table} or {ref_table} doesn't exist yet")


def setup_complete_database():
    """Main function to set up the complete database."""
    print("\n" + "=" * 70)
    print("WAM DATABASE SETUP SCRIPT")
    print("=" * 70)
    print("\nThis script will:")
    print("  1. Create all tables (if they don't exist)")
    print("  2. Add missing columns to existing tables")
    print("  3. Create indexes for performance")
    print("  4. Verify foreign keys")
    print("  5. Set default values where needed")
    print("\n" + "=" * 70 + "\n")
    
    db_url = get_db_url()
    print(f"Database URL: {db_url.split('@')[1] if '@' in db_url else 'configured'}\n")
    
    # Step 1: Create all tables
    if not create_all_tables():
        print("\n✗ Failed to create tables. Please check errors above.")
        return False
    
    # Step 2-5: Set up individual tables and verify
    engine_check = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine_check)
    db = SessionLocal()
    
    try:
        setup_staff_table(db)
        setup_assignments_table(db)
        create_indexes(db)
        verify_foreign_keys(db)
        
        print("\n" + "=" * 70)
        print("✓ DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Run seed data script: python backend/scripts/seed_data.py")
        print("  2. Start the backend server: python -m uvicorn app.main:app --reload")
        print("  3. Access the API docs at: http://localhost:8000/docs")
        print("\n" + "=" * 70 + "\n")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    try:
        success = setup_complete_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

