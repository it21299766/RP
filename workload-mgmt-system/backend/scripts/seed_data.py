"""
Seed Data Script for WAM System

This script populates the database with test data including:
- Staff members with auto-generated usernames and passwords
- Designation workload policies
- Domains, Programs, Program Sections
- Task Templates and Task Instances
- Sample Assignments and Staff Availability

Usage:
    python scripts/seed_data.py
"""

import sys
import os
from datetime import date, timedelta
from sqlalchemy import text

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db_url
from app.models.staff import Staff
from app.models.designation_workload_policy import DesignationWorkloadPolicy
from app.models.domain import Domain
from app.models.program import Program
from app.models.program_section import ProgramSection
from app.models.task_template import TaskTemplate
from app.models.task_instance import TaskInstance
from app.models.assignment import Assignment
from app.models.staff_availability import StaffAvailability
from app.utils.username_generator import generate_username
from app.utils.security import hash_password


def seed_designation_policies(db: Session):
    """Seed designation workload policies."""
    print("Seeding designation workload policies...")
    
    policies = [
        {'designation': 'Professor', 'max_hours_per_week': 20.0, 'min_hours_per_week': 10.0, 'description': 'Full-time professor workload'},
        {'designation': 'Senior Professor', 'max_hours_per_week': 18.0, 'min_hours_per_week': 10.0, 'description': 'Senior professor workload'},
        {'designation': 'Associate Professor', 'max_hours_per_week': 20.0, 'min_hours_per_week': 12.0, 'description': 'Associate professor workload'},
        {'designation': 'Senior Lecturer I', 'max_hours_per_week': 22.0, 'min_hours_per_week': 12.0, 'description': 'Senior lecturer I workload'},
        {'designation': 'Senior Lecturer II', 'max_hours_per_week': 22.0, 'min_hours_per_week': 12.0, 'description': 'Senior lecturer II workload'},
        {'designation': 'Lecturer', 'max_hours_per_week': 24.0, 'min_hours_per_week': 14.0, 'description': 'Lecturer workload'},
        {'designation': 'Probationary Lecturer', 'max_hours_per_week': 20.0, 'min_hours_per_week': 12.0, 'description': 'Probationary lecturer workload'},
        {'designation': 'Temporary Lecturer', 'max_hours_per_week': 18.0, 'min_hours_per_week': 10.0, 'description': 'Temporary lecturer workload'},
        {'designation': 'Instructor', 'max_hours_per_week': 20.0, 'min_hours_per_week': 12.0, 'description': 'Instructor workload'},
        {'designation': 'Head of Department', 'max_hours_per_week': 15.0, 'min_hours_per_week': 8.0, 'description': 'HOD workload with administrative duties'},
    ]
    
    for policy_data in policies:
        existing = db.query(DesignationWorkloadPolicy).filter(
            DesignationWorkloadPolicy.designation == policy_data['designation']
        ).first()
        if not existing:
            policy = DesignationWorkloadPolicy(**policy_data)
            db.add(policy)
    
    db.commit()
    print(f"  [OK] Added {len(policies)} designation policies")


def seed_staff(db: Session):
    """Seed staff members."""
    print("Seeding staff members...")
    
    # Check if staff table has required columns
    try:
        result = db.execute(text("SHOW COLUMNS FROM staff LIKE 'designation'"))
        if not result.fetchone():
            print("  [WARNING] designation column not found. Please run add_staff_columns.py migration first.")
            return
    except Exception as e:
        print(f"  [WARNING] Could not check columns: {e}")
        return
    
    staff_data = [
        # Academic Staff
        {'name': 'Dr. John Smith', 'designation': 'Professor', 'qualification': 'PhD', 'specialization': 'Computer Science', 
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 15, 
         'skills': ['Python', 'Machine Learning', 'Data Science'], 'available': True, 'max_hours': 20.0},
        {'name': 'Dr. Sarah Johnson', 'designation': 'Associate Professor', 'qualification': 'PhD', 'specialization': 'Software Engineering',
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 12,
         'skills': ['Java', 'OOP', 'Software Architecture'], 'available': True, 'max_hours': 20.0},
        {'name': 'Dr. Michael Williams', 'designation': 'Senior Lecturer I', 'qualification': 'PhD', 'specialization': 'Networks',
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 8,
         'skills': ['Networking', 'Cybersecurity', 'Linux'], 'available': True, 'max_hours': 22.0},
        {'name': 'Dr. Emily Brown', 'designation': 'Lecturer', 'qualification': 'MSc', 'specialization': 'Database Systems',
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 5,
         'skills': ['SQL', 'Database Design', 'MySQL'], 'available': True, 'max_hours': 24.0},
        {'name': 'Dr. David Davis', 'designation': 'Senior Lecturer II', 'qualification': 'PhD', 'specialization': 'Artificial Intelligence',
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 10,
         'skills': ['AI', 'Deep Learning', 'Python'], 'available': True, 'max_hours': 22.0},
        {'name': 'Dr. Lisa Anderson', 'designation': 'Lecturer', 'qualification': 'MSc', 'specialization': 'Web Development',
         'department': 'Computer Science', 'role': 'ACADEMIC', 'experience_years': 4,
         'skills': ['JavaScript', 'React', 'Node.js'], 'available': True, 'max_hours': 24.0},
        {'name': 'Dr. Robert Taylor', 'designation': 'Professor', 'qualification': 'PhD', 'specialization': 'Mathematics',
         'department': 'Mathematics', 'role': 'ACADEMIC', 'experience_years': 18,
         'skills': ['Calculus', 'Linear Algebra', 'Statistics'], 'available': True, 'max_hours': 20.0},
        {'name': 'Dr. Maria Garcia', 'designation': 'Associate Professor', 'qualification': 'PhD', 'specialization': 'Physics',
         'department': 'Physics', 'role': 'ACADEMIC', 'experience_years': 14,
         'skills': ['Quantum Physics', 'Mechanics', 'Thermodynamics'], 'available': True, 'max_hours': 20.0},
        # Admin Staff
        {'name': 'Admin User', 'designation': 'Head of Department', 'qualification': 'MSc', 'specialization': 'Administration',
         'department': 'Computer Science', 'role': 'ADMIN', 'experience_years': 10,
         'skills': ['Management', 'Administration'], 'available': True, 'max_hours': 15.0},
        # Management Staff
        {'name': 'Management User', 'designation': 'Head of Department', 'qualification': 'PhD', 'specialization': 'Management',
         'department': 'Computer Science', 'role': 'MANAGEMENT', 'experience_years': 12,
         'skills': ['Strategic Planning', 'Leadership'], 'available': True, 'max_hours': 15.0},
    ]
    
    created_count = 0
    for data in staff_data:
        # Check if staff already exists
        existing = db.query(Staff).filter(Staff.name == data['name']).first()
        if existing:
            print(f"  - Staff {data['name']} already exists, skipping...")
            continue
        
        staff = Staff(**data)
        staff.is_active = True
        db.add(staff)
        db.flush()  # Get staff_id
        
        # Generate username first
        staff.username = generate_username(staff.role, staff.staff_id, db)
        db.flush()  # Save username
        
        # Then set password (default password = username)
        if staff.username:
            staff.password_hash = hash_password(staff.username)
        
        created_count += 1
        print(f"  [OK] Created {staff.name} - Username: {staff.username}, Password: {staff.username}")
    
    db.commit()
    print(f"  [OK] Added {created_count} staff members")


def seed_domains(db: Session):
    """Seed domains."""
    print("Seeding domains...")
    
    domains = [
        {'name': 'Computing', 'description': 'Computer Science and IT related programs'},
        {'name': 'Engineering', 'description': 'Engineering programs'},
        {'name': 'Business', 'description': 'Business and Management programs'},
        {'name': 'Science', 'description': 'Natural Sciences programs'},
    ]
    
    for domain_data in domains:
        existing = db.query(Domain).filter(Domain.name == domain_data['name']).first()
        if not existing:
            domain = Domain(**domain_data)
            db.add(domain)
    
    db.commit()
    print(f"  [OK] Added {len(domains)} domains")


def seed_programs(db: Session):
    """Seed programs."""
    print("Seeding programs...")
    
    programs = [
        {'name': 'Bachelor of Science in Computer Science', 'code': 'BSCS', 'domain_id': 1},
        {'name': 'Bachelor of Science in Software Engineering', 'code': 'BSSE', 'domain_id': 1},
        {'name': 'Master of Science in Computer Science', 'code': 'MSCS', 'domain_id': 1},
        {'name': 'Bachelor of Science in Information Technology', 'code': 'BSIT', 'domain_id': 1},
        {'name': 'Bachelor of Engineering', 'code': 'BE', 'domain_id': 2},
        {'name': 'Bachelor of Business Administration', 'code': 'BBA', 'domain_id': 3},
    ]
    
    for program_data in programs:
        existing = db.query(Program).filter(Program.code == program_data['code']).first()
        if not existing:
            program = Program(**program_data)
            db.add(program)
    
    db.commit()
    print(f"  [OK] Added {len(programs)} programs")


def seed_program_sections(db: Session):
    """Seed program sections."""
    print("Seeding program sections...")
    
    sections = [
        {'program_id': 1, 'section_code': 'A', 'student_count': 50, 'academic_year': '2024-2025'},
        {'program_id': 1, 'section_code': 'B', 'student_count': 45, 'academic_year': '2024-2025'},
        {'program_id': 1, 'section_code': 'C', 'student_count': 48, 'academic_year': '2024-2025'},
        {'program_id': 2, 'section_code': 'A', 'student_count': 40, 'academic_year': '2024-2025'},
        {'program_id': 2, 'section_code': 'B', 'student_count': 42, 'academic_year': '2024-2025'},
        {'program_id': 3, 'section_code': 'A', 'student_count': 25, 'academic_year': '2024-2025'},
        {'program_id': 4, 'section_code': 'A', 'student_count': 35, 'academic_year': '2024-2025'},
        {'program_id': 4, 'section_code': 'B', 'student_count': 38, 'academic_year': '2024-2025'},
    ]
    
    for section_data in sections:
        existing = db.query(ProgramSection).filter(
            ProgramSection.program_id == section_data['program_id'],
            ProgramSection.section_code == section_data['section_code'],
            ProgramSection.academic_year == section_data['academic_year']
        ).first()
        if not existing:
            section = ProgramSection(**section_data)
            db.add(section)
    
    db.commit()
    print(f"  [OK] Added {len(sections)} program sections")


def seed_task_templates(db: Session):
    """Seed task templates."""
    print("Seeding task templates...")
    
    templates = [
        {'name': 'Database Management Systems Lecture', 'task_type': 'lecture', 'default_hours': 2.0,
         'required_qualification_level': 'MSc', 'required_specialization': 'Computer Science',
         'required_skills': ['SQL', 'Database Design'], 'required_experience_years': 3, 'is_active': True},
        {'name': 'Database Management Systems Lab', 'task_type': 'lab', 'default_hours': 2.0,
         'required_qualification_level': 'MSc', 'required_specialization': 'Computer Science',
         'required_skills': ['SQL', 'MySQL'], 'required_experience_years': 2, 'is_active': True},
        {'name': 'Software Engineering Lecture', 'task_type': 'lecture', 'default_hours': 2.0,
         'required_qualification_level': 'PhD', 'required_specialization': 'Software Engineering',
         'required_skills': ['OOP', 'Software Architecture'], 'required_experience_years': 5, 'is_active': True},
        {'name': 'Software Engineering Lab', 'task_type': 'lab', 'default_hours': 2.0,
         'required_qualification_level': 'MSc', 'required_specialization': 'Software Engineering',
         'required_skills': ['Java', 'OOP'], 'required_experience_years': 3, 'is_active': True},
        {'name': 'Machine Learning Lecture', 'task_type': 'lecture', 'default_hours': 2.0,
         'required_qualification_level': 'PhD', 'required_specialization': 'Computer Science',
         'required_skills': ['Python', 'Machine Learning'], 'required_experience_years': 5, 'is_active': True},
        {'name': 'Web Development Lecture', 'task_type': 'lecture', 'default_hours': 2.0,
         'required_qualification_level': 'MSc', 'required_specialization': 'Computer Science',
         'required_skills': ['JavaScript', 'React'], 'required_experience_years': 3, 'is_active': True},
        {'name': 'Web Development Lab', 'task_type': 'lab', 'default_hours': 2.0,
         'required_qualification_level': 'MSc', 'required_specialization': 'Computer Science',
         'required_skills': ['JavaScript', 'React', 'Node.js'], 'required_experience_years': 2, 'is_active': True},
        {'name': 'Networks Lecture', 'task_type': 'lecture', 'default_hours': 2.0,
         'required_qualification_level': 'PhD', 'required_specialization': 'Computer Science',
         'required_skills': ['Networking', 'Cybersecurity'], 'required_experience_years': 5, 'is_active': True},
        {'name': 'Final Exam Evaluation', 'task_type': 'exam', 'default_hours': 8.0,
         'required_qualification_level': 'MSc', 'required_specialization': None,
         'required_skills': [], 'required_experience_years': 2, 'is_active': True},
        {'name': 'Midterm Exam Evaluation', 'task_type': 'exam', 'default_hours': 4.0,
         'required_qualification_level': 'MSc', 'required_specialization': None,
         'required_skills': [], 'required_experience_years': 1, 'is_active': True},
        {'name': 'Course Material Preparation', 'task_type': 'admin', 'default_hours': 5.0,
         'required_qualification_level': 'MSc', 'required_specialization': None,
         'required_skills': [], 'required_experience_years': 2, 'is_active': True},
        {'name': 'Research Supervision', 'task_type': 'research', 'default_hours': 3.0,
         'required_qualification_level': 'PhD', 'required_specialization': None,
         'required_skills': [], 'required_experience_years': 5, 'is_active': True},
    ]
    
    for template_data in templates:
        existing = db.query(TaskTemplate).filter(TaskTemplate.name == template_data['name']).first()
        if not existing:
            template = TaskTemplate(**template_data)
            db.add(template)
    
    db.commit()
    print(f"  [OK] Added {len(templates)} task templates")


def seed_task_instances(db: Session):
    """Seed task instances."""
    print("Seeding task instances...")
    
    instances = [
        # Semester 1, 2024-2025 - Approved
        {'task_template_id': 1, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 2, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 1, 'domain_id': 1, 'program_id': 1, 'program_section_id': 2, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 2, 'domain_id': 1, 'program_id': 1, 'program_section_id': 2, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 3, 'domain_id': 1, 'program_id': 2, 'program_section_id': 4, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 4, 'domain_id': 1, 'program_id': 2, 'program_section_id': 4, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 5, 'domain_id': 1, 'program_id': 3, 'program_section_id': 6, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 6, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 7, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        {'task_template_id': 8, 'domain_id': 1, 'program_id': 1, 'program_section_id': 3, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'approved'},
        # Draft tasks
        {'task_template_id': 1, 'domain_id': 1, 'program_id': 4, 'program_section_id': 7, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'draft'},
        {'task_template_id': 2, 'domain_id': 1, 'program_id': 4, 'program_section_id': 7, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 2.0, 'status': 'draft'},
        # Exam tasks
        {'task_template_id': 9, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 8.0, 'status': 'approved'},
        {'task_template_id': 10, 'domain_id': 1, 'program_id': 1, 'program_section_id': 1, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 4.0, 'status': 'approved'},
        # Admin tasks
        {'task_template_id': 11, 'domain_id': 1, 'program_id': 1, 'program_section_id': None, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 5.0, 'status': 'approved'},
        # Research tasks
        {'task_template_id': 12, 'domain_id': 1, 'program_id': 3, 'program_section_id': None, 'semester': '2025S1',
         'academic_year': '2024-2025', 'week_number': None, 'month': None, 'effective_hours': 3.0, 'status': 'approved'},
    ]
    
    for instance_data in instances:
        instance = TaskInstance(**instance_data)
        db.add(instance)
    
    db.commit()
    print(f"  [OK] Added {len(instances)} task instances")


def seed_assignments(db: Session):
    """Seed sample assignments."""
    print("Seeding assignments...")
    
    # Get actual staff IDs from database
    all_staff = db.query(Staff).filter(Staff.role == 'ACADEMIC').order_by(Staff.staff_id).all()
    if len(all_staff) < 6:
        print(f"  [WARNING] Not enough staff members found ({len(all_staff)}). Skipping assignments.")
        return
    
    # Get task instances
    task_instances = db.query(TaskInstance).limit(10).all()
    if len(task_instances) < 10:
        print(f"  [WARNING] Not enough task instances found ({len(task_instances)}). Skipping assignments.")
        return
    
    assignments = [
        {'staff_id': all_staff[0].staff_id, 'task_instance_id': task_instances[0].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[0].staff_id, 'task_instance_id': task_instances[1].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[1].staff_id, 'task_instance_id': task_instances[2].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[1].staff_id, 'task_instance_id': task_instances[3].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[2].staff_id, 'task_instance_id': task_instances[4].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[2].staff_id, 'task_instance_id': task_instances[5].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[4].staff_id, 'task_instance_id': task_instances[6].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[5].staff_id, 'task_instance_id': task_instances[7].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[5].staff_id, 'task_instance_id': task_instances[8].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
        {'staff_id': all_staff[2].staff_id, 'task_instance_id': task_instances[9].id, 'assigned_by': 'SYSTEM', 'override': False, 'status': 'assigned'},
    ]
    
    for assignment_data in assignments:
        assignment = Assignment(**assignment_data)
        db.add(assignment)
    
    db.commit()
    print(f"  [OK] Added {len(assignments)} assignments")


def seed_staff_availability(db: Session):
    """Seed staff availability."""
    print("Seeding staff availability...")
    
    # Get actual staff IDs from database
    all_staff = db.query(Staff).filter(Staff.role == 'ACADEMIC').order_by(Staff.staff_id).all()
    if len(all_staff) < 3:
        print(f"  [WARNING] Not enough staff members found ({len(all_staff)}). Skipping availability.")
        return
    
    availability = [
        {'staff_id': all_staff[0].staff_id, 'start_date': date(2025, 1, 15), 'end_date': date(2025, 1, 20),
         'availability_type': 'leave', 'reason': 'Annual leave', 'is_available': False, 'status': 'approved'},
        {'staff_id': all_staff[1].staff_id, 'start_date': date(2025, 2, 10), 'end_date': date(2025, 2, 12),
         'availability_type': 'sick', 'reason': 'Medical leave', 'is_available': False, 'status': 'approved'},
        {'staff_id': all_staff[3].staff_id, 'start_date': date(2025, 3, 1), 'end_date': date(2025, 3, 5),
         'availability_type': 'leave', 'reason': 'Personal leave', 'is_available': False, 'status': 'approved'},
    ]
    
    for avail_data in availability:
        avail = StaffAvailability(**avail_data)
        db.add(avail)
    
    db.commit()
    print(f"  [OK] Added {len(availability)} staff availability records")


def main():
    """Main seeding function."""
    print("=" * 60)
    print("WAM System - Seed Data Script")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        seed_designation_policies(db)
        seed_staff(db)
        seed_domains(db)
        seed_programs(db)
        seed_program_sections(db)
        seed_task_templates(db)
        seed_task_instances(db)
        seed_assignments(db)
        seed_staff_availability(db)
        
        print()
        print("=" * 60)
        print("[SUCCESS] Seed data completed successfully!")
        print("=" * 60)
        print()
        print("Test Credentials:")
        print("  Academic Staff: sf1, sf2, sf3, sf4, sf5, sf6, sf7, sf8")
        print("  Admin: adm1")
        print("  Management: adm2")
        print("  Password for all: same as username (e.g., sf1/sf1)")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

