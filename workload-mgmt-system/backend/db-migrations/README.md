# Database Migrations

This folder contains SQL migration files for database schema changes. All migrations are **idempotent** (safe to run multiple times).

## Migration Files

Migrations are numbered sequentially and should be executed in order:

1. **001_add_staff_base_columns.sql** - Add designation, specialization, experience_years, username columns to staff table
2. **002_add_auth_columns.sql** - Add password_hash and is_active columns to staff table
3. **003_add_username_index.sql** - Add unique index on username column
4. **004_add_task_instance_id.sql** - Add task_instance_id column to assignments table
5. **005_add_profile_picture_column.sql** - Add profile_picture_path column to staff table

## Execution Order

**IMPORTANT**: Run migrations in sequential order (001 → 002 → 003 → 004 → 005).

## How to Run Migrations

### Option 1: MySQL Interactive Mode (Recommended for Windows)

```cmd
# Connect to MySQL
mysql -u root -p wam_db

# Then run these commands (use forward slashes /):
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/001_add_staff_base_columns.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/002_add_auth_columns.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/003_add_username_index.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/004_add_task_instance_id.sql;
source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/005_add_profile_picture_column.sql;
exit;
```

### Option 2: Windows Scripts

**PowerShell Script**:
```powershell
cd backend\db-migrations
.\run_migrations.ps1
```

**Batch Script**:
```cmd
cd backend\db-migrations
run_migrations.bat
```

### Option 3: PowerShell (Manual)

```powershell
cd backend\db-migrations
Get-Content 001_add_staff_base_columns.sql | mysql -u root -p wam_db
Get-Content 002_add_auth_columns.sql | mysql -u root -p wam_db
Get-Content 003_add_username_index.sql | mysql -u root -p wam_db
Get-Content 004_add_task_instance_id.sql | mysql -u root -p wam_db
Get-Content 005_add_profile_picture_column.sql | mysql -u root -p wam_db
```

### Option 4: MySQL Workbench

1. Open MySQL Workbench
2. Connect to your database
3. Open each SQL file in order
4. Execute each file

### Option 5: Linux/Mac Command Line

```bash
cd backend/db-migrations
mysql -u root -p wam_db < 001_add_staff_base_columns.sql
mysql -u root -p wam_db < 002_add_auth_columns.sql
mysql -u root -p wam_db < 003_add_username_index.sql
mysql -u root -p wam_db < 004_add_task_instance_id.sql
mysql -u root -p wam_db < 005_add_profile_picture_column.sql
```

## Idempotency

All migrations are idempotent - they can be run multiple times safely. Each migration:
- Checks if columns/indexes exist before creating them
- Uses `IF NOT EXISTS` clauses where supported
- Handles "already exists" errors gracefully

## Migration Status

To check which migrations have been applied, check the database schema or run:

```sql
DESCRIBE staff;
DESCRIBE assignments;
SHOW INDEX FROM staff;
```

## Idempotency Details

All migrations use MySQL's `INFORMATION_SCHEMA` to check if columns/indexes/constraints exist before creating them. This makes them:
- ✅ Safe to run multiple times
- ✅ Won't fail if already applied
- ✅ Can be re-run after partial failures

## Migration Details

### 001_add_staff_base_columns.sql
- Adds: designation, specialization, experience_years, username
- Dependencies: staff table must exist
- Sets default values for existing rows

### 002_add_auth_columns.sql
- Adds: password_hash, is_active
- Dependencies: staff table (from migration 001 or setup)
- Sets is_active = TRUE for existing rows

### 003_add_username_index.sql
- Adds: Unique index on username column
- Dependencies: username column (from migration 001)

### 004_add_task_instance_id.sql
- Adds: task_instance_id column to assignments table
- Makes: task_id nullable (for backward compatibility)
- Adds: Foreign key constraint to task_instances table
- Dependencies: assignments and task_instances tables must exist

### 005_add_profile_picture_column.sql
- Adds: profile_picture_path column to staff table
- Dependencies: staff table (from migration 001 or setup)

## Notes

- Migrations are cumulative - each builds on the previous ones
- Do NOT modify existing migration files after they've been applied
- Create new migration files for schema changes
- Always test migrations on a backup database first
- All migrations check for existence before modifying schema (idempotent)

