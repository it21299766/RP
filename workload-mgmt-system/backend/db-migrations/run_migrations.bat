@echo off
REM ============================================================================
REM Run Database Migrations (Windows Batch Script)
REM ============================================================================
REM This script runs all database migrations in order.
REM 
REM Usage:
REM   run_migrations.bat
REM
REM Requirements:
REM   - MySQL must be installed and in PATH
REM   - Database wam_db must exist
REM   - User must have permissions to modify schema
REM ============================================================================

echo ============================================================================
echo Running Database Migrations
echo ============================================================================
echo.

REM Set database name
set DB_NAME=wam_db

REM Set migration directory (current directory)
set MIGRATION_DIR=%~dp0

REM Run migrations in order using type command (Windows equivalent of cat)
echo Running migration 001_add_staff_base_columns.sql...
type "%MIGRATION_DIR%001_add_staff_base_columns.sql" | mysql -u root -p %DB_NAME%
if %errorlevel% neq 0 (
    echo ERROR: Migration 001 failed!
    pause
    exit /b 1
)

echo Running migration 002_add_auth_columns.sql...
type "%MIGRATION_DIR%002_add_auth_columns.sql" | mysql -u root -p %DB_NAME%
if %errorlevel% neq 0 (
    echo ERROR: Migration 002 failed!
    pause
    exit /b 1
)

echo Running migration 003_add_username_index.sql...
type "%MIGRATION_DIR%003_add_username_index.sql" | mysql -u root -p %DB_NAME%
if %errorlevel% neq 0 (
    echo ERROR: Migration 003 failed!
    pause
    exit /b 1
)

echo Running migration 004_add_task_instance_id.sql...
type "%MIGRATION_DIR%004_add_task_instance_id.sql" | mysql -u root -p %DB_NAME%
if %errorlevel% neq 0 (
    echo ERROR: Migration 004 failed!
    pause
    exit /b 1
)

echo Running migration 005_add_profile_picture_column.sql...
type "%MIGRATION_DIR%005_add_profile_picture_column.sql" | mysql -u root -p %DB_NAME%
if %errorlevel% neq 0 (
    echo ERROR: Migration 005 failed!
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo All migrations completed successfully!
echo ============================================================================
pause
