-- ============================================================================
-- Migration 004: Add task_instance_id Column to Assignments Table
-- ============================================================================
-- Description: Adds task_instance_id column to the assignments table and makes
--              task_id nullable for backward compatibility.
-- 
-- Idempotent: YES - Safe to run multiple times
-- Dependencies: assignments table must exist, task_instances table must exist
-- 
-- What this does:
--   1. Makes task_id column nullable (for backward compatibility)
--   2. Adds task_instance_id column (INT NULL)
--   3. Adds foreign key constraint to task_instances table
-- ============================================================================

USE wam_db;

-- Make task_id nullable if it's not already nullable
SET @dbname = DATABASE();
SET @tablename = 'assignments';
SET @columnname = 'task_id';

SET @sql = (SELECT IF(
    (SELECT IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) = 'YES',
    'SELECT "Column task_id is already nullable" AS message',
    CONCAT('ALTER TABLE ', @tablename, ' MODIFY COLUMN ', @columnname, ' INT NULL')
));

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add task_instance_id column if it doesn't exist
SET @columnname = 'task_instance_id';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND COLUMN_NAME = @columnname) > 0,
    'SELECT "Column task_instance_id already exists" AS message',
    CONCAT('ALTER TABLE ', @tablename, ' ADD COLUMN ', @columnname, ' INT NULL')
));

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add foreign key constraint if it doesn't exist
SET @constraintname = 'fk_assignments_task_instance';
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
     WHERE TABLE_SCHEMA = @dbname 
     AND TABLE_NAME = @tablename 
     AND CONSTRAINT_NAME = @constraintname) > 0,
    'SELECT "Foreign key constraint fk_assignments_task_instance already exists" AS message',
    CONCAT('ALTER TABLE ', @tablename, ' ADD CONSTRAINT ', @constraintname, 
           ' FOREIGN KEY (task_instance_id) REFERENCES task_instances(id)')
));

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT 'Migration 004 completed successfully' AS status;

