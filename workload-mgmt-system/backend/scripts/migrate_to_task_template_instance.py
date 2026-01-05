"""
Migration script to create TaskTemplate and TaskInstance tables.

This script:
1. Creates task_templates table
2. Creates task_instances table
3. Updates assignments table to include task_instance_id
4. Updates staff table with new fields (designation, specialization, experience_years)
5. Creates designation_workload_policies table
6. Creates staff_availability table

Usage:
    python -m scripts.migrate_to_task_template_instance
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, inspect
from app.database import engine, SessionLocal


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        return False
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def migrate():
    """Run all migrations."""
    db = SessionLocal()
    try:
        with engine.connect() as conn:
            print("=" * 60)
            print("Migration: TaskTemplate and TaskInstance Model")
            print("=" * 60)
            print()
            
            # 1. Create task_templates table
            if not table_exists("task_templates"):
                print("Creating task_templates table...")
                conn.execute(text("""
                    CREATE TABLE task_templates (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        task_type VARCHAR(20) NOT NULL,
                        default_hours FLOAT NOT NULL,
                        required_qualification_level VARCHAR(10) NOT NULL,
                        required_specialization VARCHAR(100),
                        required_skills JSON,
                        required_experience_years INT DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        INDEX idx_task_type (task_type),
                        INDEX idx_is_active (is_active)
                    )
                """))
                conn.commit()
                print("[OK] task_templates table created")
            else:
                print("[OK] task_templates table already exists")
            
            # 2. Create task_instances table
            if not table_exists("task_instances"):
                print("Creating task_instances table...")
                conn.execute(text("""
                    CREATE TABLE task_instances (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        task_template_id INT NOT NULL,
                        domain_id INT NOT NULL,
                        program_id INT NOT NULL,
                        program_section_id INT,
                        semester VARCHAR(20) NOT NULL,
                        academic_year VARCHAR(10) NOT NULL,
                        week_number INT,
                        month INT,
                        effective_hours FLOAT NOT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'draft',
                        FOREIGN KEY (task_template_id) REFERENCES task_templates(id),
                        FOREIGN KEY (domain_id) REFERENCES domains(domain_id),
                        FOREIGN KEY (program_id) REFERENCES programs(program_id),
                        FOREIGN KEY (program_section_id) REFERENCES program_sections(section_id),
                        INDEX idx_task_template (task_template_id),
                        INDEX idx_status (status),
                        INDEX idx_semester (semester),
                        INDEX idx_academic_year (academic_year)
                    )
                """))
                conn.commit()
                print("[OK] task_instances table created")
            else:
                print("[OK] task_instances table already exists")
            
            # 3. Update assignments table
            if not column_exists("assignments", "task_instance_id"):
                print("Adding task_instance_id to assignments table...")
                conn.execute(text("""
                    ALTER TABLE assignments
                    ADD COLUMN task_instance_id INT,
                    ADD FOREIGN KEY (task_instance_id) REFERENCES task_instances(id)
                """))
                conn.commit()
                print("[OK] task_instance_id column added to assignments")
            else:
                print("[OK] task_instance_id column already exists in assignments")
            
            # 4. Update staff table
            if not column_exists("staff", "designation"):
                print("Adding designation to staff table...")
                conn.execute(text("""
                    ALTER TABLE staff
                    ADD COLUMN designation VARCHAR(50) NOT NULL DEFAULT 'Lecturer'
                """))
                conn.commit()
                print("[OK] designation column added to staff")
            else:
                print("[OK] designation column already exists in staff")
            
            if not column_exists("staff", "specialization"):
                print("Adding specialization to staff table...")
                # Check if specialty exists (old column name)
                if column_exists("staff", "specialty"):
                    conn.execute(text("""
                        ALTER TABLE staff
                        ADD COLUMN specialization VARCHAR(100),
                        UPDATE staff SET specialization = specialty WHERE specialization IS NULL
                    """))
                else:
                    conn.execute(text("""
                        ALTER TABLE staff
                        ADD COLUMN specialization VARCHAR(100) NOT NULL DEFAULT 'General'
                    """))
                conn.commit()
                print("[OK] specialization column added to staff")
            else:
                print("[OK] specialization column already exists in staff")
            
            if not column_exists("staff", "experience_years"):
                print("Adding experience_years to staff table...")
                # Check if experience exists (old column name)
                if column_exists("staff", "experience"):
                    conn.execute(text("""
                        ALTER TABLE staff
                        ADD COLUMN experience_years INT DEFAULT 0,
                        UPDATE staff SET experience_years = experience WHERE experience_years = 0
                    """))
                else:
                    conn.execute(text("""
                        ALTER TABLE staff
                        ADD COLUMN experience_years INT DEFAULT 0
                    """))
                conn.commit()
                print("[OK] experience_years column added to staff")
            else:
                print("[OK] experience_years column already exists in staff")
            
            # 5. Create designation_workload_policies table
            if not table_exists("designation_workload_policies"):
                print("Creating designation_workload_policies table...")
                conn.execute(text("""
                    CREATE TABLE designation_workload_policies (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        designation VARCHAR(50) NOT NULL UNIQUE,
                        max_hours_per_week FLOAT NOT NULL,
                        min_hours_per_week FLOAT,
                        description VARCHAR(255),
                        INDEX idx_designation (designation)
                    )
                """))
                conn.commit()
                print("[OK] designation_workload_policies table created")
            else:
                print("[OK] designation_workload_policies table already exists")
            
            # 6. Create staff_availability table
            if not table_exists("staff_availability"):
                print("Creating staff_availability table...")
                conn.execute(text("""
                    CREATE TABLE staff_availability (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        staff_id INT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        availability_type VARCHAR(20) NOT NULL,
                        reason TEXT,
                        is_available BOOLEAN NOT NULL DEFAULT FALSE,
                        status VARCHAR(20) NOT NULL DEFAULT 'approved',
                        FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
                        INDEX idx_staff_id (staff_id),
                        INDEX idx_dates (start_date, end_date)
                    )
                """))
                conn.commit()
                print("[OK] staff_availability table created")
            else:
                print("[OK] staff_availability table already exists")
            
            print()
            print("=" * 60)
            print("[SUCCESS] Migration completed successfully!")
            print("=" * 60)
            return True
            
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)

