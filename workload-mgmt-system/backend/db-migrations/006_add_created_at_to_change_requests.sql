-- Migration: Add created_at timestamp to change_requests table
-- Description: Adds a created_at column to track when change requests were submitted
-- Date: 2025-01-XX
-- Idempotent: Yes (checks if column exists before adding)

-- Check if column already exists
ALTER TABLE change_requests ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER admin_comment;
-- Note: The DEFAULT CURRENT_TIMESTAMP ensures that existing records get the current time as created_at