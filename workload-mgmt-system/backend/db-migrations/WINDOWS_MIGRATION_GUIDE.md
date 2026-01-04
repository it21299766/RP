# Windows Migration Guide

Quick guide for running migrations on Windows.

## Quick Start (Easiest Method)

### Method 1: MySQL Interactive Mode (Recommended)

1. Open Command Prompt or PowerShell
2. Navigate to your project directory:
   ```cmd
   cd C:\rahul-projects\workload-mgmt-system
   ```
3. Connect to MySQL:
   ```cmd
   mysql -u root -p wam_db
   ```
4. Enter your MySQL password when prompted
5. Run migrations (use forward slashes `/` in paths):
   ```sql
   source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/001_add_staff_base_columns.sql;
   source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/002_add_auth_columns.sql;
   source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/003_add_username_index.sql;
   source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/004_add_task_instance_id.sql;
   source C:/rahul-projects/workload-mgmt-system/backend/db-migrations/005_add_profile_picture_column.sql;
   exit;
   ```

### Method 2: PowerShell Script

1. Open PowerShell
2. Navigate to migrations folder:
   ```powershell
   cd C:\rahul-projects\workload-mgmt-system\backend\db-migrations
   ```
3. Run the script:
   ```powershell
   .\run_migrations.ps1
   ```
4. Enter MySQL password when prompted (multiple times)

### Method 3: Batch Script

1. Open Command Prompt
2. Navigate to migrations folder:
   ```cmd
   cd C:\rahul-projects\workload-mgmt-system\backend\db-migrations
   ```
3. Run the script:
   ```cmd
   run_migrations.bat
   ```
4. Enter MySQL password when prompted (multiple times)

### Method 4: PowerShell (Manual - One at a time)

1. Open PowerShell
2. Navigate to migrations folder:
   ```powershell
   cd C:\rahul-projects\workload-mgmt-system\backend\db-migrations
   ```
3. Run each migration:
   ```powershell
   Get-Content 001_add_staff_base_columns.sql | mysql -u root -p wam_db
   Get-Content 002_add_auth_columns.sql | mysql -u root -p wam_db
   Get-Content 003_add_username_index.sql | mysql -u root -p wam_db
   Get-Content 004_add_task_instance_id.sql | mysql -u root -p wam_db
   Get-Content 005_add_profile_picture_column.sql | mysql -u root -p wam_db
   ```
4. Enter MySQL password when prompted for each command

## Why Redirection Doesn't Work in Windows

In Linux/Mac, you can use:
```bash
mysql -u root -p wam_db < file.sql
```

In Windows Command Prompt, this doesn't work the same way because:
- The `<` redirection operator works differently
- Path handling is different
- Error handling is different

## Solutions for Windows

### Solution 1: Use `source` command in MySQL (Best)
- Most reliable
- Works on all Windows versions
- Easy to see errors

### Solution 2: Use PowerShell pipe (`|`)
- Works well in PowerShell
- Easy to automate

### Solution 3: Use `type` command in CMD
- Works in Command Prompt
- Similar to Linux `cat` command

## Troubleshooting

### Error: "mysql is not recognized"
**Solution**: Add MySQL to your PATH or use full path to mysql.exe
- Find MySQL installation: Usually `C:\Program Files\MySQL\MySQL Server X.X\bin`
- Add to PATH: System Properties → Environment Variables → Path → Add MySQL bin folder

### Error: "Access denied"
**Solution**: Check your MySQL username and password
- Default user: `root`
- Make sure password is correct
- Check if MySQL service is running

### Error: "Unknown database 'wam_db'"
**Solution**: Create the database first
```sql
CREATE DATABASE wam_db;
```

### Error: "Cannot connect to MySQL server"
**Solution**: 
- Make sure MySQL service is running
- Check if MySQL is listening on the correct port (default: 3306)
- Check firewall settings

## Verification

After running migrations, verify they worked:

```sql
-- Connect to MySQL
mysql -u root -p wam_db

-- Check staff table columns
DESCRIBE staff;

-- Check assignments table columns  
DESCRIBE assignments;

-- Check indexes
SHOW INDEX FROM staff;
```

You should see:
- ✅ designation, specialization, experience_years, username columns in staff
- ✅ password_hash, is_active columns in staff
- ✅ profile_picture_path column in staff
- ✅ task_instance_id column in assignments
- ✅ idx_staff_username index on staff table

