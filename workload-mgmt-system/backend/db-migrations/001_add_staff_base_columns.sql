-- ============================================================================
-- Migration 001: Add Base Staff Columns
-- ============================================================================
-- Description: Adds designation, specialization, experience_years, and username
--              columns to the staff table.
-- 
-- Idempotent: YES - Safe to run multiple times
-- Dependencies: None (staff table must exist)
-- 
-- What this does:
--   1. Adds designation column (VARCHAR(50) NULL)
--   2. Adds specialization column (VARCHAR(100) NULL)
--   3. Adds experience_years column (INT DEFAULT 0)
--   4. Adds username column (VARCHAR(20) NULL)
-- ============================================================================

USE wam_db;

-- Add designation column if it doesn't exist
SET @dbname = DATABASE();
SET @tablename = 'staff';
SET @columnname = 'designation';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column designation already exists" AS message',
    'ALTER TABLE staff ADD COLUMN designation VARCHAR(50) NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add specialization column if it doesn't exist
SET @columnname = 'specialization';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column specialization already exists" AS message',
    'ALTER TABLE staff ADD COLUMN specialization VARCHAR(100) NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add experience_years column if it doesn't exist
SET @columnname = 'experience_years';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column experience_years already exists" AS message',
    'ALTER TABLE staff ADD COLUMN experience_years INT DEFAULT 0'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add username column if it doesn't exist
SET @columnname = 'username';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column username already exists" AS message',
    'ALTER TABLE staff ADD COLUMN username VARCHAR(20) NULL'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Set default values for existing rows (idempotent - only updates NULL values)
UPDATE staff SET experience_years = 0 WHERE experience_years IS NULL;

SELECT 'Migration 001 completed successfully' AS status;

