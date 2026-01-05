-- ============================================================================
-- Migration 003: Add Unique Index on Username Column
-- ============================================================================
-- Description: Adds a unique index on the username column in the staff table.
-- 
-- Idempotent: YES - Safe to run multiple times
-- Dependencies: Migration 001 (username column must exist)
-- 
-- What this does:
--   1. Checks if unique index on username exists
--   2. Creates unique index if it doesn't exist
-- ============================================================================

USE wam_db;

-- Check if unique index exists, if not create it
SET @dbname = DATABASE();
SET @tablename = 'staff';
SET @indexname = 'idx_staff_username';

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND INDEX_NAME = @indexname) > 0,
    'SELECT "Index idx_staff_username already exists" AS message',
    CONCAT('CREATE UNIQUE INDEX ', @indexname, ' ON ', @tablename, '(username)')
));

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT 'Migration 003 completed successfully' AS status;

