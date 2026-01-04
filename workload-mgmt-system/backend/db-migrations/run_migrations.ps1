# ============================================================================
# Run Database Migrations (Windows PowerShell Script)
# ============================================================================
# This script runs all database migrations in order.
# 
# Usage:
#   .\run_migrations.ps1
#
# Requirements:
#   - MySQL must be installed and in PATH
#   - Database wam_db must exist
#   - User must have permissions to modify schema
# ============================================================================

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Running Database Migrations" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

$DB_NAME = "wam_db"
$MIGRATION_DIR = $PSScriptRoot

$migrations = @(
    "001_add_staff_base_columns.sql",
    "002_add_auth_columns.sql",
    "003_add_username_index.sql",
    "004_add_task_instance_id.sql",
    "005_add_profile_picture_column.sql"
)

foreach ($migration in $migrations) {
    $migrationPath = Join-Path $MIGRATION_DIR $migration
    Write-Host "Running migration $migration..." -ForegroundColor Yellow
    
    $sqlContent = Get-Content $migrationPath -Raw
    $sqlContent | mysql -u root -p $DB_NAME
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Migration $migration failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "All migrations completed successfully!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Read-Host "Press Enter to exit"

