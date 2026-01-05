-- ============================================================================
-- Migration 005: Add Profile Picture Column to Staff Table
-- ============================================================================
-- Description: Adds profile_picture_path column to the staff table for storing
--              profile picture file paths.
-- 
-- Idempotent: YES - Safe to run multiple times
-- Dependencies: Migration 001 (staff table must exist)
-- 
-- What this does:
--   1. Adds profile_picture_path column (VARCHAR(255) NULL)
-- ============================================================================

USE wam_db;

-- Add profile_picture_path column if it doesn't exist
SET @dbname = DATABASE();
SET @tablename = 'staff';
SET @columnname = 'profile_picture_path';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column profile_picture_path already exists" AS message',
    CONCAT('ALTER TABLE ', @tablename, ' ADD COLUMN ', @columnname, ' VARCHAR(255) NULL')
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT 'Migration 005 completed successfully' AS status;

