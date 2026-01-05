"""
Report Service - Business logic for generating reports

This service executes SQL queries for various workload reports.
All queries use the current database schema with task_instances and task_templates.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Optional, Any


class ReportService:
    """
    Service class for report generation business logic.
    
    This class executes SQL queries to generate various workload reports.
    All queries are defined in report_queries.sql and are executed using raw SQL.
    """
    
    @staticmethod
    def _execute_query(db: Session, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Helper method to execute SQL query and return results as list of dicts.
        
        Args:
            db: Database session
            query: SQL query string
            params: Query parameters dictionary
            
        Returns:
            List of dictionaries (one per row)
        """
        if params is None:
            params = {}
        result = db.execute(text(query), params)
        columns = result.keys()
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    
    @staticmethod
    def get_staff_workload_summary(
        db: Session,
        semester: Optional[str] = None,
        department: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get staff workload summary report.
        
        BUSINESS LOGIC:
        - Calculates total assigned hours per staff
        - Determines overload/underload status
        - Uses DesignationWorkloadPolicy for max hours
        
        RETRIEVES FROM DB:
        - staff table
        - assignments table
        - task_instances table
        - designation_workload_policies table
        
        Args:
            db: Database session
            semester: Optional semester filter (e.g., "2025S1")
            department: Optional department filter
            
        Returns:
            List of dictionaries with staff workload data
        """
        where_clauses = ["s.role = 'ACADEMIC'"]
        params = {}
        
        if department:
            where_clauses.append("s.department = :department")
            params['department'] = department
        
        where_sql = " AND ".join(where_clauses)
        
        semester_condition = "AND ti.semester = :semester" if semester else ""
        if semester:
            params['semester'] = semester
        
        query = f"""
            SELECT
                s.staff_id,
                s.name AS full_name,
                s.designation,
                s.department,
                COALESCE(SUM(ti.effective_hours), 0) AS total_assigned_hours,
                COUNT(DISTINCT a.assignment_id) AS total_assignments,
                CASE
                    WHEN COALESCE(SUM(ti.effective_hours), 0) > COALESCE(dwp.max_hours_per_week, s.max_hours, 20.0) THEN 'OVERLOADED'
                    WHEN COALESCE(SUM(ti.effective_hours), 0) < COALESCE(dwp.max_hours_per_week, s.max_hours, 20.0) * 0.5 THEN 'UNDERLOADED'
                    ELSE 'BALANCED'
                END AS workload_status,
                COALESCE(dwp.max_hours_per_week, s.max_hours, 20.0) AS max_hours_per_week
            FROM staff s
            LEFT JOIN assignments a
                ON s.staff_id = a.staff_id
                AND a.status IN ('assigned', 'completed')
            LEFT JOIN task_instances ti
                ON a.task_instance_id = ti.id
                {semester_condition}
            LEFT JOIN designation_workload_policies dwp
                ON s.designation = dwp.designation
            WHERE {where_sql}
            GROUP BY s.staff_id, s.name, s.designation, s.department, dwp.max_hours_per_week, s.max_hours
            ORDER BY s.name
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_workload_by_task_type(
        db: Session,
        staff_id: Optional[int] = None,
        semester: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get workload breakdown by task type (teaching, admin, research).
        
        Args:
            db: Database session
            staff_id: Optional staff ID filter
            semester: Optional semester filter
            
        Returns:
            List of dictionaries with workload by task type
        """
        where_clauses = ["s.role = 'ACADEMIC'"]
        params = {}
        
        if staff_id:
            where_clauses.append("s.staff_id = :staff_id")
            params['staff_id'] = staff_id
            
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                s.staff_id,
                s.name AS full_name,
                tt.task_type,
                COALESCE(SUM(ti.effective_hours), 0) AS type_hours,
                COUNT(DISTINCT a.assignment_id) AS task_count
            FROM staff s
            LEFT JOIN assignments a
                ON s.staff_id = a.staff_id
                AND a.status IN ('assigned', 'completed')
            LEFT JOIN task_instances ti
                ON a.task_instance_id = ti.id
            LEFT JOIN task_templates tt
                ON ti.task_template_id = tt.id
            WHERE {where_sql}
            GROUP BY s.staff_id, s.name, tt.task_type
            ORDER BY s.name, tt.task_type
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_workload_by_domain(
        db: Session,
        staff_id: Optional[int] = None,
        semester: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get workload breakdown by domain.
        
        Args:
            db: Database session
            staff_id: Optional staff ID filter
            semester: Optional semester filter
            
        Returns:
            List of dictionaries with workload by domain
        """
        where_clauses = ["s.role = 'ACADEMIC'"]
        params = {}
        
        if staff_id:
            where_clauses.append("s.staff_id = :staff_id")
            params['staff_id'] = staff_id
            
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                s.staff_id,
                s.name AS full_name,
                d.name AS domain_name,
                COALESCE(SUM(ti.effective_hours), 0) AS domain_hours,
                COUNT(DISTINCT a.assignment_id) AS task_count
            FROM staff s
            LEFT JOIN assignments a
                ON s.staff_id = a.staff_id
                AND a.status IN ('assigned', 'completed')
            LEFT JOIN task_instances ti
                ON a.task_instance_id = ti.id
            LEFT JOIN domains d
                ON ti.domain_id = d.domain_id
            WHERE {where_sql}
            GROUP BY s.staff_id, s.name, d.domain_id, d.name
            ORDER BY s.name, d.name
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_department_average_workload(
        db: Session,
        semester: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get average workload per department.
        
        Args:
            db: Database session
            semester: Optional semester filter
            
        Returns:
            List of dictionaries with department average workload
        """
        where_clause = ""
        params = {}
        
        if semester:
            where_clause = "AND ti.semester = :semester"
            params['semester'] = semester
        
        query = f"""
            SELECT
                s.department,
                COUNT(DISTINCT s.staff_id) AS total_staff,
                ROUND(AVG(total_hours), 2) AS average_hours_per_staff,
                ROUND(SUM(total_hours), 2) AS total_department_hours
            FROM (
                SELECT
                    s.staff_id,
                    s.department,
                    COALESCE(SUM(ti.effective_hours), 0) AS total_hours
                FROM staff s
                LEFT JOIN assignments a
                    ON s.staff_id = a.staff_id
                    AND a.status IN ('assigned', 'completed')
                LEFT JOIN task_instances ti
                    ON a.task_instance_id = ti.id
                    {where_clause}
                WHERE s.role = 'ACADEMIC'
                GROUP BY s.staff_id, s.department
            ) AS staff_workloads
            GROUP BY s.department
            ORDER BY s.department
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_program_teaching_load(
        db: Session,
        semester: Optional[str] = None,
        program_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get program teaching load report.
        
        Args:
            db: Database session
            semester: Optional semester filter
            program_id: Optional program ID filter
            
        Returns:
            List of dictionaries with program teaching load
        """
        where_clauses = ["ti.status = 'approved'"]
        params = {}
        
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
            
        if program_id:
            where_clauses.append("p.program_id = :program_id")
            params['program_id'] = program_id
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                p.program_id,
                p.code AS program_code,
                p.name AS program_name,
                d.name AS domain_name,
                COUNT(DISTINCT ti.id) AS total_task_instances,
                COUNT(DISTINCT a.assignment_id) AS assigned_tasks,
                COUNT(DISTINCT ti.id) - COUNT(DISTINCT a.assignment_id) AS unassigned_tasks,
                COALESCE(SUM(ti.effective_hours), 0) AS total_program_hours,
                COALESCE(SUM(CASE WHEN a.assignment_id IS NOT NULL THEN ti.effective_hours ELSE 0 END), 0) AS assigned_hours
            FROM programs p
            LEFT JOIN domains d
                ON p.domain_id = d.domain_id
            LEFT JOIN task_instances ti
                ON p.program_id = ti.program_id
            LEFT JOIN assignments a
                ON ti.id = a.task_instance_id
                AND a.status IN ('assigned', 'completed')
            WHERE {where_sql}
            GROUP BY p.program_id, p.code, p.name, d.name
            ORDER BY d.name, p.code
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_unassigned_tasks(
        db: Session,
        semester: Optional[str] = None,
        program_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get unassigned tasks report (critical for admin).
        
        Args:
            db: Database session
            semester: Optional semester filter
            program_id: Optional program ID filter
            
        Returns:
            List of dictionaries with unassigned tasks
        """
        where_clauses = [
            "a.assignment_id IS NULL",
            "ti.status = 'approved'"
        ]
        params = {}
        
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
            
        if program_id:
            where_clauses.append("p.program_id = :program_id")
            params['program_id'] = program_id
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                ti.id AS task_instance_id,
                tt.name AS task_name,
                tt.task_type,
                ti.effective_hours,
                d.name AS domain_name,
                p.code AS program_code,
                p.name AS program_name,
                ps.section_code,
                ti.semester,
                ti.academic_year,
                ti.status AS task_status
            FROM task_instances ti
            INNER JOIN task_templates tt
                ON ti.task_template_id = tt.id
            LEFT JOIN domains d
                ON ti.domain_id = d.domain_id
            LEFT JOIN programs p
                ON ti.program_id = p.program_id
            LEFT JOIN program_sections ps
                ON ti.program_section_id = ps.section_id
            LEFT JOIN assignments a
                ON ti.id = a.task_instance_id
                AND a.status IN ('assigned', 'completed')
            WHERE {where_sql}
            ORDER BY d.name, p.code, ti.semester
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_overload_underload_distribution(
        db: Session,
        semester: Optional[str] = None,
        department: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get overload/underload distribution (for charts).
        
        Args:
            db: Database session
            semester: Optional semester filter
            department: Optional department filter
            
        Returns:
            List of dictionaries with workload status distribution
        """
        where_clauses = ["s.role = 'ACADEMIC'"]
        params = {}
        
        if semester:
            params['semester'] = semester
            
        if department:
            where_clauses.append("s.department = :department")
            params['department'] = department
        
        where_sql = " AND ".join(where_clauses)
        semester_join = "AND ti.semester = :semester" if semester else ""
        
        query = f"""
            SELECT
                workload_status,
                COUNT(*) AS staff_count
            FROM (
                SELECT
                    s.staff_id,
                    CASE
                        WHEN COALESCE(SUM(ti.effective_hours), 0) > COALESCE(dwp.max_hours_per_week, s.max_hours, 20.0) THEN 'OVERLOADED'
                        WHEN COALESCE(SUM(ti.effective_hours), 0) < COALESCE(dwp.max_hours_per_week, s.max_hours, 20.0) * 0.5 THEN 'UNDERLOADED'
                        ELSE 'BALANCED'
                    END AS workload_status
                FROM staff s
                LEFT JOIN assignments a
                    ON s.staff_id = a.staff_id
                    AND a.status IN ('assigned', 'completed')
                LEFT JOIN task_instances ti
                    ON a.task_instance_id = ti.id
                    {semester_join}
                LEFT JOIN designation_workload_policies dwp
                    ON s.designation = dwp.designation
                WHERE {where_sql}
                GROUP BY s.staff_id, dwp.max_hours_per_week, s.max_hours
            ) AS workload_summary
            GROUP BY workload_status
            ORDER BY 
                CASE workload_status
                    WHEN 'OVERLOADED' THEN 1
                    WHEN 'BALANCED' THEN 2
                    WHEN 'UNDERLOADED' THEN 3
                END
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_ga_input_snapshot(
        db: Session,
        semester: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get GA optimization input snapshot (unassigned approved tasks).
        
        Args:
            db: Database session
            semester: Optional semester filter
            
        Returns:
            List of dictionaries with unassigned tasks for GA
        """
        where_clauses = [
            "ti.status = 'approved'",
            "ti.id NOT IN (SELECT task_instance_id FROM assignments WHERE status IN ('assigned', 'completed'))"
        ]
        params = {}
        
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                ti.id AS task_instance_id,
                ti.effective_hours,
                tt.required_qualification_level,
                tt.required_specialization,
                tt.required_experience_years,
                tt.required_skills,
                tt.task_type,
                d.name AS domain_name,
                p.code AS program_code
            FROM task_instances ti
            INNER JOIN task_templates tt
                ON ti.task_template_id = tt.id
            LEFT JOIN domains d
                ON ti.domain_id = d.domain_id
            LEFT JOIN programs p
                ON ti.program_id = p.program_id
            WHERE {where_sql}
            ORDER BY d.name, p.code
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_ga_result_summary(
        db: Session,
        semester: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get GA optimization result summary.
        
        Args:
            db: Database session
            semester: Optional semester filter
            
        Returns:
            Dictionary with GA result summary
        """
        where_clause = ""
        params = {}
        
        if semester:
            where_clause = "AND ti.semester = :semester"
            params['semester'] = semester
        
        query = f"""
            SELECT
                COUNT(DISTINCT a.assignment_id) AS total_assigned_tasks,
                COUNT(DISTINCT a.staff_id) AS total_staff_with_assignments,
                COUNT(DISTINCT ti.id) AS total_task_instances,
                COALESCE(SUM(ti.effective_hours), 0) AS total_assigned_hours,
                ROUND(AVG(ti.effective_hours), 2) AS average_hours_per_task,
                COUNT(DISTINCT CASE WHEN a.assigned_by = 'SYSTEM' THEN a.assignment_id END) AS system_assignments,
                COUNT(DISTINCT CASE WHEN a.assigned_by = 'ADMIN' THEN a.assignment_id END) AS admin_assignments
            FROM assignments a
            INNER JOIN task_instances ti
                ON a.task_instance_id = ti.id
                {where_clause}
            WHERE a.status IN ('assigned', 'completed')
        """
        
        result = ReportService._execute_query(db, query, params)
        return result[0] if result else {}
    
    @staticmethod
    def get_change_request_summary(
        db: Session
    ) -> List[Dict[str, Any]]:
        """
        Get change request summary report.
        
        Args:
            db: Database session
            
        Returns:
            List of dictionaries with change request summary
        """
        query = """
            SELECT
                cr.status,
                COUNT(*) AS total_requests,
                COUNT(DISTINCT cr.staff_id) AS unique_staff_count
            FROM change_requests cr
            GROUP BY cr.status
            ORDER BY 
                CASE cr.status
                    WHEN 'PENDING' THEN 1
                    WHEN 'APPROVED' THEN 2
                    WHEN 'REJECTED' THEN 3
                    ELSE 4
                END
        """
        
        return ReportService._execute_query(db, query)
    
    @staticmethod
    def get_staff_detailed_workload(
        db: Session,
        staff_id: int,
        semester: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get detailed workload report for a specific staff member.
        
        Args:
            db: Database session
            staff_id: Staff ID to get report for
            semester: Optional semester filter
            
        Returns:
            List of dictionaries with detailed staff workload
        """
        where_clauses = ["s.staff_id = :staff_id", "a.status IN ('assigned', 'completed')"]
        params = {'staff_id': staff_id}
        
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                s.staff_id,
                s.name AS staff_name,
                s.designation,
                s.department,
                tt.name AS task_name,
                tt.task_type,
                ti.effective_hours,
                d.name AS domain_name,
                p.code AS program_code,
                p.name AS program_name,
                ps.section_code,
                ti.semester,
                ti.academic_year,
                a.status AS assignment_status,
                a.assigned_by,
                a.override
            FROM staff s
            INNER JOIN assignments a
                ON s.staff_id = a.staff_id
            INNER JOIN task_instances ti
                ON a.task_instance_id = ti.id
            INNER JOIN task_templates tt
                ON ti.task_template_id = tt.id
            LEFT JOIN domains d
                ON ti.domain_id = d.domain_id
            LEFT JOIN programs p
                ON ti.program_id = p.program_id
            LEFT JOIN program_sections ps
                ON ti.program_section_id = ps.section_id
            WHERE {where_sql}
            ORDER BY s.name, d.name, p.code, ti.semester
        """
        
        return ReportService._execute_query(db, query, params)
    
    @staticmethod
    def get_program_section_workload(
        db: Session,
        semester: Optional[str] = None,
        program_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get workload breakdown by program section.
        
        Args:
            db: Database session
            semester: Optional semester filter
            program_id: Optional program ID filter
            
        Returns:
            List of dictionaries with program section workload
        """
        where_clauses = ["ti.status = 'approved'"]
        params = {}
        
        if semester:
            where_clauses.append("ti.semester = :semester")
            params['semester'] = semester
            
        if program_id:
            where_clauses.append("p.program_id = :program_id")
            params['program_id'] = program_id
        
        where_sql = " AND ".join(where_clauses)
        
        query = f"""
            SELECT
                p.code AS program_code,
                p.name AS program_name,
                ps.section_code,
                ps.academic_year,
                COUNT(DISTINCT ti.id) AS total_tasks,
                COUNT(DISTINCT a.assignment_id) AS assigned_tasks,
                COALESCE(SUM(ti.effective_hours), 0) AS total_hours,
                COALESCE(SUM(CASE WHEN a.assignment_id IS NOT NULL THEN ti.effective_hours ELSE 0 END), 0) AS assigned_hours,
                COUNT(DISTINCT a.staff_id) AS assigned_staff_count
            FROM programs p
            INNER JOIN program_sections ps
                ON p.program_id = ps.program_id
            LEFT JOIN task_instances ti
                ON ps.section_id = ti.program_section_id
            LEFT JOIN assignments a
                ON ti.id = a.task_instance_id
                AND a.status IN ('assigned', 'completed')
            WHERE {where_sql}
            GROUP BY p.program_id, p.code, p.name, ps.section_code, ps.academic_year
            ORDER BY p.code, ps.section_code, ps.academic_year
        """
        
        return ReportService._execute_query(db, query, params)
