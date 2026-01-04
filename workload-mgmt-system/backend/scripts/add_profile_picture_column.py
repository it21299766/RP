"""
Add Profile Picture Column to Staff Table

This script adds the profile_picture_path column to the staff table.
It is safe to run multiple times (idempotent).

WHAT THIS DOES:
- Adds profile_picture_path column to staff table (nullable VARCHAR(255))
- Allows staff to have profile pictures stored in uploads/profiles/

WHY THIS COLUMN:
- Stores the path to profile picture files
- Enables profile picture upload/update/delete functionality
- Format: "profiles/staff_{staff_id}_{uuid}.{extension}"
"""

import sys
import os

# Add parent directory to path to import database utilities
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, inspect, text
from app.database import get_db_url

# Configure stdout encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

def column_exists(inspector, table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def add_profile_picture_column():
    """
    Add profile_picture_path column to staff table.
    
    This function:
    1. Connects to database
    2. Checks if column already exists
    3. Adds column if it doesn't exist
    4. Reports success or skip message
    """
    print("=" * 60)
    print("Adding profile_picture_path column to staff table")
    print("=" * 60)
    
    # Get database URL
    database_url = get_db_url()
    print(f"Database URL: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
    
    # Create engine
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    table_name = "staff"
    column_name = "profile_picture_path"
    
    # Check if table exists
    if table_name not in inspector.get_table_names():
        print(f"❌ ERROR: Table '{table_name}' does not exist!")
        print("   Please run setup_database.py first to create tables.")
        return False
    
    # Check if column already exists
    if column_exists(inspector, table_name, column_name):
        print(f"✓ Column '{column_name}' already exists in '{table_name}' table")
        print("  Skipping column addition (idempotent operation)")
        return True
    
    # Add column
    try:
        with engine.connect() as conn:
            # Add profile_picture_path column (nullable VARCHAR(255))
            alter_sql = text(f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} VARCHAR(255) NULL
            """)
            conn.execute(alter_sql)
            conn.commit()
        
        print(f"✓ Successfully added column '{column_name}' to '{table_name}' table")
        print(f"  Column type: VARCHAR(255) NULL")
        print(f"  Purpose: Store path to profile picture files")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to add column '{column_name}'")
        print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n")
    success = add_profile_picture_column()
    print("\n")
    
    if success:
        print("=" * 60)
        print("Migration completed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("Migration failed! Please check the errors above.")
        print("=" * 60)
        sys.exit(1)

