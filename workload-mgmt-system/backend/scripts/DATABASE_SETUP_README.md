# Database Setup Guide

This guide explains how to set up the WAM database from scratch or update an existing database.

## Quick Start

### Option 1: Python Script (Recommended)

The Python script is comprehensive and handles all edge cases:

```bash
cd backend
python scripts/setup_complete_database.py
```

**What it does:**
- Creates all tables if they don't exist
- Adds missing columns to existing tables
- Creates indexes for performance
- Verifies foreign keys
- Sets default values
- Handles errors gracefully

### Option 2: SQL Script

For users who prefer SQL:

```bash
# Using MySQL command line
mysql -u root -p wam_db < backend/scripts/setup_database.sql

# Or execute in MySQL Workbench
# Open backend/scripts/setup_database.sql and run it
```

**Note:** The SQL script creates tables but may not handle all edge cases. Use Python script for comprehensive setup.

## Prerequisites

1. **MySQL Server Running**
   - Default: `localhost:3307`
   - Database: `wam_db`
   - User: `root` (or configure in `.env`)

2. **Database Created**
   ```sql
   CREATE DATABASE IF NOT EXISTS wam_db;
   ```

3. **Python Dependencies Installed**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## What Gets Created

### Core Tables

1. **domains** - Academic domains (Computing, Engineering, etc.)
2. **programs** - Degree programs (BSCS, BSSE, etc.)
3. **program_sections** - Program sections (Section A, B, C)
4. **staff** - Staff members with all fields
5. **designation_workload_policies** - Workload limits by designation
6. **task_templates** - Reusable task definitions
7. **task_instances** - Specific task executions
8. **assignments** - Staff-to-task assignments
9. **staff_availability** - Leave and availability records
10. **change_requests** - Staff change requests
11. **modules** - Course modules
12. **module_sections** - Module sections
13. **tariffs** - Workload tariff rules
14. **tasks** - Legacy tasks table (backward compatibility)

### Indexes Created

- `idx_staff_username` - Unique index on staff username
- `idx_staff_department` - Index on staff department
- `idx_staff_role` - Index on staff role
- `idx_task_instance_status` - Index on task instance status
- `idx_task_instance_semester` - Index on semester
- `idx_assignments_staff` - Index on assignment staff_id
- `idx_assignments_task_instance` - Index on task_instance_id

### Foreign Keys

All foreign key relationships are established:
- `programs.domain_id` → `domains.domain_id`
- `program_sections.program_id` → `programs.program_id`
- `task_instances.task_template_id` → `task_templates.id`
- `task_instances.domain_id` → `domains.domain_id`
- `task_instances.program_id` → `programs.program_id`
- `task_instances.program_section_id` → `program_sections.section_id`
- `assignments.staff_id` → `staff.staff_id`
- `assignments.task_instance_id` → `task_instances.id`
- `staff_availability.staff_id` → `staff.staff_id`
- And more...

## Setup Process

### Step 1: Run Setup Script

```bash
cd backend
python scripts/setup_complete_database.py
```

**Expected Output:**
```
======================================================================
WAM DATABASE SETUP SCRIPT
======================================================================

This script will:
  1. Create all tables (if they don't exist)
  2. Add missing columns to existing tables
  3. Create indexes for performance
  4. Verify foreign keys
  5. Set default values where needed

======================================================================

STEP 1: Creating all tables (if they don't exist)
======================================================================
✓ All tables created/verified successfully

STEP 2: Setting up staff table
======================================================================
  ✓ Column username already exists
  ✓ Column designation already exists
  ...

STEP 3: Setting up assignments table
======================================================================
  ✓ Made task_id nullable (for migration support)
  ✓ Foreign key for task_instance_id already exists

STEP 4: Creating indexes
======================================================================
  ✓ Index idx_staff_username already exists
  ...

STEP 5: Verifying foreign keys
======================================================================
  ✓ Foreign key programs.domain_id → domains.domain_id exists
  ...

======================================================================
✓ DATABASE SETUP COMPLETED SUCCESSFULLY!
======================================================================
```

### Step 2: Seed Data (Optional)

After setup, populate with test data:

```bash
python scripts/seed_data.py
```

### Step 3: Verify Setup

Check that tables exist:

```sql
SHOW TABLES;
```

Should show all 14 tables.

## Troubleshooting

### Error: "Table already exists"

**Solution:** This is normal if tables already exist. The script will skip creation and update existing tables.

### Error: "Column already exists"

**Solution:** This is normal if columns already exist. The script will skip adding duplicate columns.

### Error: "Foreign key constraint fails"

**Solution:** 
1. Make sure parent tables exist (domains before programs, etc.)
2. Run the setup script - it creates tables in the correct order
3. Check that referenced tables have data

### Error: "Access denied"

**Solution:**
1. Check database credentials in `.env` or `database.py`
2. Verify MySQL user has CREATE, ALTER, INDEX permissions
3. Grant permissions: `GRANT ALL ON wam_db.* TO 'root'@'localhost';`

### Error: "Module not found"

**Solution:**
1. Make sure you're in the `backend` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Check Python path includes the project root

## Manual Verification

### Check Tables

```sql
USE wam_db;
SHOW TABLES;
```

### Check Staff Table Structure

```sql
DESCRIBE staff;
```

Should show all columns including:
- `username`
- `designation`
- `qualification`
- `specialization`
- `department`
- `role`
- `experience_years`
- `skills`
- `password_hash`
- `is_active`

### Check Indexes

```sql
SHOW INDEXES FROM staff;
```

Should show:
- `PRIMARY` on `staff_id`
- `idx_staff_username` on `username`
- `idx_staff_department` on `department`
- `idx_staff_role` on `role`

### Check Foreign Keys

```sql
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'wam_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

## Updating Existing Database

If you have an existing database, the setup script will:

1. **Keep existing data** - No data is deleted
2. **Add missing columns** - Only adds columns that don't exist
3. **Update constraints** - Sets NOT NULL after adding defaults
4. **Create missing indexes** - Only creates indexes that don't exist
5. **Verify foreign keys** - Checks but doesn't recreate existing ones

**Safe to run multiple times** - The script is idempotent.

## Next Steps

After database setup:

1. **Seed Data:**
   ```bash
   python scripts/seed_data.py
   ```

2. **Start Backend:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Access API Docs:**
   - Open: `http://localhost:8000/docs`

4. **Test Connection:**
   - Try login endpoint
   - Check dashboard metrics

## Database Configuration

### Environment Variables

Create `.env` file in `backend/`:

```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3307/wam_db
```

Or use default in `backend/app/database.py`:
```python
DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/wam_db"
```

### Change Database Settings

Edit `backend/app/database.py`:
```python
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE"
)
```

## Support

If you encounter issues:

1. Check error messages in the script output
2. Verify database connection settings
3. Check MySQL server is running
4. Verify user permissions
5. Review troubleshooting section above

## Script Features

- ✅ **Idempotent** - Safe to run multiple times
- ✅ **Non-destructive** - Doesn't delete existing data
- ✅ **Comprehensive** - Handles all tables and columns
- ✅ **Error handling** - Gracefully handles existing objects
- ✅ **Unicode support** - Works on Windows with UTF-8
- ✅ **Detailed output** - Shows what's being done

