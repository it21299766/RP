-- ============================================================================
-- WAM Database Setup SQL Script
-- ============================================================================
-- This SQL script creates all tables and sets up the database schema.
-- Use this if you prefer SQL over Python, or for manual database setup.
--
-- Usage:
--   mysql -u root -p wam_db < backend/scripts/setup_database.sql
--   OR execute in MySQL Workbench
-- ============================================================================

-- Set database
USE wam_db;

-- Disable foreign key checks temporarily to avoid dependency issues
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================================
-- STEP 1: Create Core Tables (without foreign keys first)
-- ============================================================================

-- Domains Table
CREATE TABLE IF NOT EXISTS domains (
    domain_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    INDEX idx_domain_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Programs Table
CREATE TABLE IF NOT EXISTS programs (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    domain_id INT NOT NULL,
    INDEX idx_program_code (code),
    INDEX idx_program_domain (domain_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Program Sections Table
CREATE TABLE IF NOT EXISTS program_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    section_code VARCHAR(10) NOT NULL,
    student_count INT NOT NULL,
    academic_year VARCHAR(15) NOT NULL,
    INDEX idx_section_program (program_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Designation Workload Policies Table
CREATE TABLE IF NOT EXISTS designation_workload_policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    designation VARCHAR(50) NOT NULL UNIQUE,
    max_hours_per_week FLOAT NOT NULL,
    min_hours_per_week FLOAT,
    description VARCHAR(255),
    INDEX idx_designation (designation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Staff Table
CREATE TABLE IF NOT EXISTS staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    name VARCHAR(100) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    qualification VARCHAR(10) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    experience_years INT DEFAULT 0,
    skills JSON,
    max_hours FLOAT,
    available BOOLEAN DEFAULT TRUE,
    password_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_staff_username (username),
    INDEX idx_staff_department (department),
    INDEX idx_staff_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Task Templates Table
CREATE TABLE IF NOT EXISTS task_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    task_type VARCHAR(20) NOT NULL,
    default_hours FLOAT NOT NULL,
    required_qualification_level VARCHAR(10) NOT NULL,
    required_specialization VARCHAR(100),
    required_skills JSON,
    required_experience_years INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_template_type (task_type),
    INDEX idx_template_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Task Instances Table
CREATE TABLE IF NOT EXISTS task_instances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_template_id INT NOT NULL,
    domain_id INT NOT NULL,
    program_id INT NOT NULL,
    program_section_id INT,
    semester VARCHAR(20) NOT NULL,
    academic_year VARCHAR(10) NOT NULL,
    week_number INT,
    month INT,
    effective_hours FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    INDEX idx_task_instance_status (status),
    INDEX idx_task_instance_semester (semester),
    INDEX idx_task_instance_template (task_template_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Assignments Table
CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT NOT NULL,
    task_instance_id INT NOT NULL,
    task_id INT NULL,
    assigned_by VARCHAR(20) DEFAULT 'SYSTEM',
    override BOOLEAN DEFAULT FALSE,
    override_reason VARCHAR(255),
    status VARCHAR(20) DEFAULT 'assigned',
    INDEX idx_assignments_staff (staff_id),
    INDEX idx_assignments_task_instance (task_instance_id),
    INDEX idx_assignments_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Staff Availability Table
CREATE TABLE IF NOT EXISTS staff_availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    availability_type VARCHAR(20) NOT NULL,
    reason TEXT,
    is_available BOOLEAN DEFAULT FALSE NOT NULL,
    status VARCHAR(20) DEFAULT 'approved' NOT NULL,
    INDEX idx_availability_staff (staff_id),
    INDEX idx_availability_dates (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Change Requests Table
CREATE TABLE IF NOT EXISTS change_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    requested_by_staff_id INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    admin_comment VARCHAR(255),
    INDEX idx_change_request_staff (requested_by_staff_id),
    INDEX idx_change_request_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Modules Table
CREATE TABLE IF NOT EXISTS modules (
    module_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    program_id INT NOT NULL,
    semester INT NOT NULL,
    credits INT NOT NULL,
    INDEX idx_module_code (code),
    INDEX idx_module_program (program_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Module Sections Table
CREATE TABLE IF NOT EXISTS module_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT NOT NULL,
    section_code VARCHAR(10) NOT NULL,
    student_count INT NOT NULL,
    INDEX idx_module_section_module (module_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tariffs Table
CREATE TABLE IF NOT EXISTS tariffs (
    tariff_id INT AUTO_INCREMENT PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    hours INT NOT NULL,
    per_unit VARCHAR(50) NOT NULL,
    INDEX idx_tariff_type (task_type),
    INDEX idx_tariff_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Legacy Tasks Table (for backward compatibility)
CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    task_type VARCHAR(20) NOT NULL,
    hours FLOAT NOT NULL,
    domain_id INT NOT NULL,
    program_id INT NOT NULL,
    program_section_id INT,
    semester VARCHAR(20) NOT NULL,
    academic_year VARCHAR(10) NOT NULL,
    INDEX idx_task_status (task_type),
    INDEX idx_task_type (task_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- STEP 2: Add Foreign Key Constraints (after all tables are created)
-- ============================================================================

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Helper procedure to add foreign key if it doesn't exist
DELIMITER $$

DROP PROCEDURE IF EXISTS add_foreign_key_if_not_exists$$
CREATE PROCEDURE add_foreign_key_if_not_exists(
    IN p_table_name VARCHAR(64),
    IN p_constraint_name VARCHAR(64),
    IN p_column_name VARCHAR(64),
    IN p_referenced_table VARCHAR(64),
    IN p_referenced_column VARCHAR(64),
    IN p_on_delete_action VARCHAR(20)
)
BEGIN
    DECLARE constraint_exists INT DEFAULT 0;
    
    SELECT COUNT(*) INTO constraint_exists
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = p_table_name
      AND CONSTRAINT_NAME = p_constraint_name
      AND CONSTRAINT_TYPE = 'FOREIGN KEY';
    
    IF constraint_exists = 0 THEN
        SET @sql = CONCAT(
            'ALTER TABLE ', p_table_name,
            ' ADD CONSTRAINT ', p_constraint_name,
            ' FOREIGN KEY (', p_column_name, ')',
            ' REFERENCES ', p_referenced_table, '(', p_referenced_column, ')',
            ' ON DELETE ', p_on_delete_action
        );
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END$$

DELIMITER ;

-- Add foreign keys to programs table
CALL add_foreign_key_if_not_exists('programs', 'fk_programs_domain', 'domain_id', 'domains', 'domain_id', 'CASCADE');

-- Add foreign keys to program_sections table
CALL add_foreign_key_if_not_exists('program_sections', 'fk_program_sections_program', 'program_id', 'programs', 'program_id', 'CASCADE');

-- Add foreign keys to task_instances table
CALL add_foreign_key_if_not_exists('task_instances', 'fk_task_instance_template', 'task_template_id', 'task_templates', 'id', 'CASCADE');
CALL add_foreign_key_if_not_exists('task_instances', 'fk_task_instance_domain', 'domain_id', 'domains', 'domain_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('task_instances', 'fk_task_instance_program', 'program_id', 'programs', 'program_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('task_instances', 'fk_task_instance_program_section', 'program_section_id', 'program_sections', 'section_id', 'SET NULL');

-- Add foreign keys to assignments table
CALL add_foreign_key_if_not_exists('assignments', 'fk_assignments_staff', 'staff_id', 'staff', 'staff_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('assignments', 'fk_assignments_task_instance', 'task_instance_id', 'task_instances', 'id', 'CASCADE');

-- Add foreign keys to staff_availability table
CALL add_foreign_key_if_not_exists('staff_availability', 'fk_staff_availability_staff', 'staff_id', 'staff', 'staff_id', 'CASCADE');

-- Add foreign keys to change_requests table
CALL add_foreign_key_if_not_exists('change_requests', 'fk_change_requests_assignment', 'assignment_id', 'assignments', 'assignment_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('change_requests', 'fk_change_requests_staff', 'requested_by_staff_id', 'staff', 'staff_id', 'CASCADE');

-- Add foreign keys to modules table
CALL add_foreign_key_if_not_exists('modules', 'fk_modules_program', 'program_id', 'programs', 'program_id', 'CASCADE');

-- Add foreign keys to module_sections table
CALL add_foreign_key_if_not_exists('module_sections', 'fk_module_sections_module', 'module_id', 'modules', 'module_id', 'CASCADE');

-- Add foreign keys to tasks table (legacy)
CALL add_foreign_key_if_not_exists('tasks', 'fk_tasks_domain', 'domain_id', 'domains', 'domain_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('tasks', 'fk_tasks_program', 'program_id', 'programs', 'program_id', 'CASCADE');
CALL add_foreign_key_if_not_exists('tasks', 'fk_tasks_program_section', 'program_section_id', 'program_sections', 'section_id', 'SET NULL');

-- Clean up the procedure
DROP PROCEDURE IF EXISTS add_foreign_key_if_not_exists;

-- ============================================================================
-- STEP 2: Add missing columns to existing tables (if any)
-- ============================================================================

-- Add columns to staff table if they don't exist
SET @dbname = DATABASE();
SET @tablename = 'staff';
SET @preparedStatement = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = @dbname AND TABLE_NAME = @tablename AND COLUMN_NAME = 'username') > 0,
    'SELECT 1',
    'ALTER TABLE staff ADD COLUMN username VARCHAR(20) UNIQUE AFTER staff_id'
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Similar for other columns (simplified - use Python script for comprehensive setup)

-- ============================================================================
-- STEP 3: Create indexes for performance
-- ============================================================================

-- Indexes are created inline with tables above
-- Additional indexes can be added here if needed

-- ============================================================================
-- STEP 4: Set default values
-- ============================================================================

-- Update existing staff records with defaults
UPDATE staff SET designation = 'Lecturer' WHERE designation IS NULL;
UPDATE staff SET qualification = 'MSc' WHERE qualification IS NULL;
UPDATE staff SET specialization = 'General' WHERE specialization IS NULL;
UPDATE staff SET department = 'General' WHERE department IS NULL;
UPDATE staff SET role = 'ACADEMIC' WHERE role IS NULL;
UPDATE staff SET experience_years = 0 WHERE experience_years IS NULL;
UPDATE staff SET available = TRUE WHERE available IS NULL;
UPDATE staff SET is_active = TRUE WHERE is_active IS NULL;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

SELECT 'Database setup completed successfully!' AS message;

