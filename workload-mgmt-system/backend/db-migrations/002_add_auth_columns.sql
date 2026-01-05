-- ============================================================================
-- Migration 002: Add Authentication Columns to Staff Table
-- ============================================================================
-- Description: Adds password_hash and is_active columns to the staff table.
-- 
-- Idempotent: YES - Safe to run multiple times
-- Dependencies: Migration 001 (staff table must exist)
-- 
-- What this does:
--   1. Adds password_hash column (VARCHAR(255) NULL)
--   2. Adds is_active column (BOOLEAN NOT NULL DEFAULT TRUE)
--   3. Sets is_active = TRUE for existing rows
-- ============================================================================

USE wam_db;

-- Add password_hash column if it doesn't exist
SET @dbname = DATABASE();
SET @tablename = 'staff';
SET @columnname = 'password_hash';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column password_hash already exists" AS message',
    'ALTER TABLE staff ADD COLUMN password_hash VARCHAR(255) NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add is_active column if it doesn't exist
SET @columnname = 'is_active';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column is_active already exists" AS message',
    'ALTER TABLE staff ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Update existing rows to have is_active = TRUE (idempotent - only updates NULL values)
UPDATE staff SET is_active = TRUE WHERE is_active IS NULL;

SELECT 'Migration 002 completed successfully' AS status;

