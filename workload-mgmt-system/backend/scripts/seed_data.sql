-- ============================================
-- Seed Data Script for WAM System
-- ============================================
-- This script populates the database with test data
-- Run this after creating tables and running the username migration

USE wam_db;

-- ============================================
-- 1. Designation Workload Policies
-- ============================================
INSERT INTO designation_workload_policies (designation, max_hours_per_week, min_hours_per_week, description) VALUES
('Professor', 20.0, 10.0, 'Full-time professor workload'),
('Senior Professor', 18.0, 10.0, 'Senior professor workload'),
('Associate Professor', 20.0, 12.0, 'Associate professor workload'),
('Senior Lecturer I', 22.0, 12.0, 'Senior lecturer I workload'),
('Senior Lecturer II', 22.0, 12.0, 'Senior lecturer II workload'),
('Lecturer', 24.0, 14.0, 'Lecturer workload'),
('Probationary Lecturer', 20.0, 12.0, 'Probationary lecturer workload'),
('Temporary Lecturer', 18.0, 10.0, 'Temporary lecturer workload'),
('Instructor', 20.0, 12.0, 'Instructor workload'),
('Head of Department', 15.0, 8.0, 'HOD workload with administrative duties');

-- ============================================
-- 2. Staff Members
-- ============================================
-- Note: Usernames will be auto-generated as sf1, sf2, adm1, etc.
-- Passwords are set to username by default

INSERT INTO staff (name, designation, qualification, specialization, department, role, experience_years, skills, available, max_hours, is_active) VALUES
-- Academic Staff (ACADEMIC role)
('Dr. John Smith', 'Professor', 'PhD', 'Computer Science', 'Computer Science', 'ACADEMIC', 15, '["Python", "Machine Learning", "Data Science"]', TRUE, 20.0, TRUE),
('Dr. Sarah Johnson', 'Associate Professor', 'PhD', 'Software Engineering', 'Computer Science', 'ACADEMIC', 12, '["Java", "OOP", "Software Architecture"]', TRUE, 20.0, TRUE),
('Dr. Michael Williams', 'Senior Lecturer I', 'PhD', 'Networks', 'Computer Science', 'ACADEMIC', 8, '["Networking", "Cybersecurity", "Linux"]', TRUE, 22.0, TRUE),
('Dr. Emily Brown', 'Lecturer', 'MSc', 'Database Systems', 'Computer Science', 'ACADEMIC', 5, '["SQL", "Database Design", "MySQL"]', TRUE, 24.0, TRUE),
('Dr. David Davis', 'Senior Lecturer II', 'PhD', 'Artificial Intelligence', 'Computer Science', 'ACADEMIC', 10, '["AI", "Deep Learning", "Python"]', TRUE, 22.0, TRUE),
('Dr. Lisa Anderson', 'Lecturer', 'MSc', 'Web Development', 'Computer Science', 'ACADEMIC', 4, '["JavaScript", "React", "Node.js"]', TRUE, 24.0, TRUE),
('Dr. Robert Taylor', 'Professor', 'PhD', 'Mathematics', 'Mathematics', 'ACADEMIC', 18, '["Calculus", "Linear Algebra", "Statistics"]', TRUE, 20.0, TRUE),
('Dr. Maria Garcia', 'Associate Professor', 'PhD', 'Physics', 'Physics', 'ACADEMIC', 14, '["Quantum Physics", "Mechanics", "Thermodynamics"]', TRUE, 20.0, TRUE),
-- Admin Staff (ADMIN role)
('Admin User', 'Head of Department', 'MSc', 'Administration', 'Computer Science', 'ADMIN', 10, '["Management", "Administration"]', TRUE, 15.0, TRUE),
-- Management Staff (MANAGEMENT role)
('Management User', 'Head of Department', 'PhD', 'Management', 'Computer Science', 'MANAGEMENT', 12, '["Strategic Planning", "Leadership"]', TRUE, 15.0, TRUE);

-- Update usernames for staff (they should be auto-generated, but we'll set them explicitly)
UPDATE staff SET username = 'sf1', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 1; -- password: sf1
UPDATE staff SET username = 'sf2', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 2; -- password: sf2
UPDATE staff SET username = 'sf3', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 3; -- password: sf3
UPDATE staff SET username = 'sf4', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 4; -- password: sf4
UPDATE staff SET username = 'sf5', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 5; -- password: sf5
UPDATE staff SET username = 'sf6', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 6; -- password: sf6
UPDATE staff SET username = 'sf7', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 7; -- password: sf7
UPDATE staff SET username = 'sf8', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 8; -- password: sf8
UPDATE staff SET username = 'adm1', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 9; -- password: adm1
UPDATE staff SET username = 'adm2', password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqZqZqZqZq' WHERE staff_id = 10; -- password: adm2

-- ============================================
-- 3. Domains
-- ============================================
INSERT INTO domains (name, description) VALUES
('Computing', 'Computer Science and IT related programs'),
('Engineering', 'Engineering programs'),
('Business', 'Business and Management programs'),
('Science', 'Natural Sciences programs');

-- ============================================
-- 4. Programs
-- ============================================
INSERT INTO programs (name, code, domain_id) VALUES
('Bachelor of Science in Computer Science', 'BSCS', 1),
('Bachelor of Science in Software Engineering', 'BSSE', 1),
('Master of Science in Computer Science', 'MSCS', 1),
('Bachelor of Science in Information Technology', 'BSIT', 1),
('Bachelor of Engineering', 'BE', 2),
('Bachelor of Business Administration', 'BBA', 3);

-- ============================================
-- 5. Program Sections
-- ============================================
INSERT INTO program_sections (program_id, section_code, student_count, academic_year) VALUES
(1, 'A', 50, '2024-2025'),
(1, 'B', 45, '2024-2025'),
(1, 'C', 48, '2024-2025'),
(2, 'A', 40, '2024-2025'),
(2, 'B', 42, '2024-2025'),
(3, 'A', 25, '2024-2025'),
(4, 'A', 35, '2024-2025'),
(4, 'B', 38, '2024-2025');

-- ============================================
-- 6. Task Templates
-- ============================================
INSERT INTO task_templates (name, task_type, default_hours, required_qualification_level, required_specialization, required_skills, required_experience_years, is_active) VALUES
('Database Management Systems Lecture', 'lecture', 2.0, 'MSc', 'Computer Science', '["SQL", "Database Design"]', 3, TRUE),
('Database Management Systems Lab', 'lab', 2.0, 'MSc', 'Computer Science', '["SQL", "MySQL"]', 2, TRUE),
('Software Engineering Lecture', 'lecture', 2.0, 'PhD', 'Software Engineering', '["OOP", "Software Architecture"]', 5, TRUE),
('Software Engineering Lab', 'lab', 2.0, 'MSc', 'Software Engineering', '["Java", "OOP"]', 3, TRUE),
('Machine Learning Lecture', 'lecture', 2.0, 'PhD', 'Computer Science', '["Python", "Machine Learning"]', 5, TRUE),
('Web Development Lecture', 'lecture', 2.0, 'MSc', 'Computer Science', '["JavaScript", "React"]', 3, TRUE),
('Web Development Lab', 'lab', 2.0, 'MSc', 'Computer Science', '["JavaScript", "React", "Node.js"]', 2, TRUE),
('Networks Lecture', 'lecture', 2.0, 'PhD', 'Computer Science', '["Networking", "Cybersecurity"]', 5, TRUE),
('Final Exam Evaluation', 'exam', 8.0, 'MSc', NULL, '[]', 2, TRUE),
('Midterm Exam Evaluation', 'exam', 4.0, 'MSc', NULL, '[]', 1, TRUE),
('Course Material Preparation', 'admin', 5.0, 'MSc', NULL, '[]', 2, TRUE),
('Research Supervision', 'research', 3.0, 'PhD', NULL, '[]', 5, TRUE);

-- ============================================
-- 7. Task Instances
-- ============================================
INSERT INTO task_instances (task_template_id, domain_id, program_id, program_section_id, semester, academic_year, week_number, month, effective_hours, status) VALUES
-- Semester 1, 2024-2025
(1, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(2, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(1, 1, 1, 2, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(2, 1, 1, 2, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(3, 1, 2, 4, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(4, 1, 2, 4, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(5, 1, 3, 6, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(6, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(7, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
(8, 1, 1, 3, '2025S1', '2024-2025', NULL, NULL, 2.0, 'approved'),
-- Draft tasks
(1, 1, 4, 7, '2025S1', '2024-2025', NULL, NULL, 2.0, 'draft'),
(2, 1, 4, 7, '2025S1', '2024-2025', NULL, NULL, 2.0, 'draft'),
-- Exam tasks
(9, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 8.0, 'approved'),
(10, 1, 1, 1, '2025S1', '2024-2025', NULL, NULL, 4.0, 'approved'),
-- Admin tasks
(11, 1, 1, NULL, '2025S1', '2024-2025', NULL, NULL, 5.0, 'approved'),
-- Research tasks
(12, 1, 3, NULL, '2025S1', '2024-2025', NULL, NULL, 3.0, 'approved');

-- ============================================
-- 8. Assignments (Sample)
-- ============================================
INSERT INTO assignments (staff_id, task_instance_id, assigned_by, override, status) VALUES
(1, 1, 'SYSTEM', FALSE, 'assigned'),
(1, 2, 'SYSTEM', FALSE, 'assigned'),
(2, 3, 'SYSTEM', FALSE, 'assigned'),
(2, 4, 'SYSTEM', FALSE, 'assigned'),
(3, 5, 'SYSTEM', FALSE, 'assigned'),
(3, 6, 'SYSTEM', FALSE, 'assigned'),
(5, 7, 'SYSTEM', FALSE, 'assigned'),
(6, 8, 'SYSTEM', FALSE, 'assigned'),
(6, 9, 'SYSTEM', FALSE, 'assigned'),
(3, 10, 'SYSTEM', FALSE, 'assigned');

-- ============================================
-- 9. Staff Availability (Sample)
-- ============================================
INSERT INTO staff_availability (staff_id, start_date, end_date, availability_type, reason, is_available, status) VALUES
(1, '2025-01-15', '2025-01-20', 'leave', 'Annual leave', FALSE, 'approved'),
(2, '2025-02-10', '2025-02-12', 'sick', 'Medical leave', FALSE, 'approved'),
(4, '2025-03-01', '2025-03-05', 'leave', 'Personal leave', FALSE, 'approved');

-- ============================================
-- End of Seed Data
-- ============================================
-- Note: Passwords in the UPDATE statements above are placeholders
-- The actual password hashes should be generated using bcrypt
-- Run the Python seed script instead for proper password hashing

