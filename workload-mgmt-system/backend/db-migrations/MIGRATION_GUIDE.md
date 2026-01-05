# Database Migration Guide

This guide explains how to use the SQL migration files in the `db-migrations` folder.

## Overview

All migration files are **idempotent** - they can be run multiple times safely. Each migration checks if columns/indexes/constraints already exist before creating them.

## Migration Files

| File | Description | Dependencies |
|------|-------------|--------------|
| `001_add_staff_base_columns.sql` | Adds designation, specialization, experience_years, username to staff table | staff table must exist |
| `002_add_auth_columns.sql` | Adds password_hash, is_active to staff table | Migration 001 |
| `003_add_username_index.sql` | Adds unique index on username column | Migration 001 |
| `004_add_task_instance_id.sql` | Adds task_instance_id to assignments table | assignments, task_instances tables must exist |
| `005_add_profile_picture_column.sql` | Adds profile_picture_path to staff table | Migration 001 |

## How to Run Migrations

### Option 1: MySQL Interactive Mode (Recommended for Windows)

This is the easiest and most reliable method for Windows:

```cmd
# Connect to MySQL
mysql -u root -p wam_db

# Then run these commands inside MySQL (use forward slashes for paths):
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/001_add_staff_base_columns.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/002_add_auth_columns.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/003_add_username_index.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/004_add_task_instance_id.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/005_add_profile_picture_column.sql;
exit;
```

**Note**: Replace `C:/rahul-projects/workload-mgmt-system` with your actual project path.

### Option 2: PowerShell Script (Windows)

Use the provided PowerShell script:

```powershell
cd backend/db-migrations
.\run_migrations.ps1
```

### Option 3: Batch Script (Windows)

Use the provided batch script:

```cmd
cd backend\db-migrations
run_migrations.bat
```

### Option 4: PowerShell (Windows - Manual)

Run each migration file using PowerShell:

```powershell
cd backend/db-migrations
Get-Content 001_add_staff_base_columns.sql | mysql -u root -p wam_db
Get-Content 002_add_auth_columns.sql | mysql -u root -p wam_db
Get-Content 003_add_username_index.sql | mysql -u root -p wam_db
Get-Content 004_add_task_instance_id.sql | mysql -u root -p wam_db
Get-Content 005_add_profile_picture_column.sql | mysql -u root -p wam_db
```

### Option 5: Command Prompt (Windows - Full Path)

Use full paths in Command Prompt:

```cmd
cd backend\db-migrations
mysql -u root -p wam_db < "C:\rahul-projects\workload-mgmt-system\backend\db-migrations\001_add_staff_base_columns.sql"
mysql -u root -p wam_db < "C:\rahul-projects\workload-mgmt-system\backend\db-migrations\002_add_auth_columns.sql"
mysql -u root -p wam_db < "C:\rahul-projects\workload-mgmt-system\backend\db-migrations\003_add_username_index.sql"
mysql -u root -p wam_db < "C:\rahul-projects\workload-mgmt-system\backend\db-migrations\004_add_task_instance_id.sql"
mysql -u root -p wam_db < "C:\rahul-projects\workload-mgmt-system\backend\db-migrations\005_add_profile_picture_column.sql"
```

### Option 6: Linux/Mac Command Line

```bash
# Navigate to migrations folder
cd backend/db-migrations

# Run migrations in order
mysql -u root -p wam_db < 001_add_staff_base_columns.sql
mysql -u root -p wam_db < 002_add_auth_columns.sql
mysql -u root -p wam_db < 003_add_username_index.sql
mysql -u root -p wam_db < 004_add_task_instance_id.sql
mysql -u root -p wam_db < 005_add_profile_picture_column.sql
```

### Option 2: Run All Migrations (Bash Script)

Create a script to run all migrations:

```bash
#!/bin/bash
cd backend/db-migrations
for file in $(ls -1 *.sql | sort); do
    echo "Running $file..."
    mysql -u root -p wam_db < "$file"
    if [ $? -eq 0 ]; then
        echo "✓ $file completed successfully"
    else
        echo "✗ $file failed"
        exit 1
    fi
done
echo "All migrations completed successfully!"
```

### Option 3: MySQL Workbench

1. Open MySQL Workbench
2. Connect to your database
3. For each migration file (in order):
   - File → Open SQL Script
   - Select the migration file
   - Click Execute (⚡) button
   - Verify success message

### Option 4: Python Script (If Needed)

If you need to run migrations from Python:

```python
import pymysql
import os

# Database connection
connection = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password='root',
    database='wam_db'
)

# Migration files in order
migrations = [
    '001_add_staff_base_columns.sql',
    '002_add_auth_columns.sql',
    '003_add_username_index.sql',
    '004_add_task_instance_id.sql',
    '005_add_profile_picture_column.sql'
]

try:
    for migration_file in migrations:
        print(f"Running {migration_file}...")
        with open(f'backend/db-migrations/{migration_file}', 'r') as f:
            sql = f.read()
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        print(f"✓ {migration_file} completed")
    print("\nAll migrations completed successfully!")
finally:
    connection.close()
```

## Verification

After running migrations, verify the schema:

```sql
-- Check staff table columns
DESCRIBE staff;

-- Check assignments table columns
DESCRIBE assignments;

-- Check indexes on staff table
SHOW INDEX FROM staff;

-- Check foreign keys on assignments table
SELECT 
    CONSTRAINT_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'wam_db'
AND TABLE_NAME = 'assignments'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

## Expected Results

After running all migrations, you should see:

### Staff Table Columns:
- ✅ designation (VARCHAR(50) NULL)
- ✅ specialization (VARCHAR(100) NULL)
- ✅ experience_years (INT DEFAULT 0)
- ✅ username (VARCHAR(20) NULL)
- ✅ password_hash (VARCHAR(255) NULL)
- ✅ is_active (BOOLEAN NOT NULL DEFAULT TRUE)
- ✅ profile_picture_path (VARCHAR(255) NULL)

### Staff Table Indexes:
- ✅ idx_staff_username (UNIQUE on username)

### Assignments Table Columns:
- ✅ task_id (INT NULL - made nullable)
- ✅ task_instance_id (INT NULL)
- ✅ Foreign key: fk_assignments_task_instance → task_instances(id)

## Troubleshooting

### Error: "Table doesn't exist"
**Solution**: Run `setup_database.sql` first to create base tables.

### Error: "Column already exists"
**Solution**: This is normal - migrations are idempotent. The migration will skip creating the column if it already exists.

### Error: "Index already exists"
**Solution**: This is normal - migrations check for existence before creating indexes.

### Error: "Foreign key constraint fails"
**Solution**: Ensure `task_instances` table exists before running migration 004.

### Error: "Duplicate key" or "Duplicate column"
**Solution**: This means the migration was already applied. Check the schema to verify, then continue with the next migration.

## Rollback

**Important**: These migrations do NOT include rollback scripts. To rollback:
1. Create a backup before running migrations
2. Restore from backup if needed
3. Or manually drop columns/indexes if needed

## Best Practices

1. ✅ **Always backup** your database before running migrations
2. ✅ **Test migrations** on a development database first
3. ✅ **Run migrations in order** (001 → 002 → 003 → 004 → 005)
4. ✅ **Verify schema** after each migration
5. ✅ **Don't modify** existing migration files after they've been applied
6. ✅ **Create new migrations** for schema changes (006, 007, etc.)

## Migration Status Tracking

To track which migrations have been applied, you can:

1. **Check schema directly** (recommended):
   ```sql
   DESCRIBE staff;
   DESCRIBE assignments;
   ```

2. **Create a migrations table** (optional):
   ```sql
   CREATE TABLE IF NOT EXISTS schema_migrations (
       migration_file VARCHAR(255) PRIMARY KEY,
       applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **Use version control** - track applied migrations in your deployment process

## Next Steps

After running migrations:
1. Verify schema matches expected structure
2. Update application code if needed
3. Test application functionality
4. Document any custom data migrations needed

---

**Note**: All migrations use MySQL's `INFORMATION_SCHEMA` to check for existing columns/indexes/constraints, making them idempotent and safe to run multiple times.

