"""
Dashboard API Routes

RESTful endpoints for dashboard metrics and statistics.
Access: All authenticated users can view dashboard
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.utils.auth_guard import get_current_user
from app.models.staff import Staff
from app.models.task_instance import TaskInstance
from app.models.assignment import Assignment
from app.repositories.staff_repository import StaffRepository
from app.repositories.task_instance_repository import TaskInstanceRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.models.designation_workload_policy import DesignationWorkloadPolicy
from typing import List, Dict

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: Staff = Depends(get_current_user)
):
    """
    Get dashboard metrics and statistics.
    
    WHAT THIS DOES: Returns key metrics for the dashboard including:
    - Total staff count (ADMIN: all staff, ACADEMIC: only self)
    - Total task instances (courses) count (ADMIN: all, ACADEMIC: only assigned to self)
    - Total assignments count (ADMIN: all, ACADEMIC: only own assignments)
    - Assignment rate (percentage of tasks assigned)
    - Workload distribution by staff (ADMIN: all staff, ACADEMIC: only self)
    - Workload fairness data
    
    RETRIEVES FROM DB:
    - Staff table (count of staff - filtered by role)
    - TaskInstance table (count of task instances - filtered by role)
    - Assignment table (count of assignments - filtered by role)
    - Assignment table with staff (for workload distribution - filtered by role)
    
    ROLE-BASED FILTERING:
    - ADMIN/MANAGEMENT: See all data (university-wide)
    - ACADEMIC: See only own data (own assignments, own workload)
    
    Args:
        db: Database session
        current_user: Currently authenticated user (used for role-based filtering)
    
    Returns:
        Dictionary with metrics, workloadDistribution, and workloadFairness
    """
    # ROLE-BASED FILTERING: ACADEMIC sees only own data, ADMIN/MANAGEMENT sees all
    is_academic = current_user.role == "ACADEMIC"
    
    if is_academic:
        # ACADEMIC STAFF: Filter to show only own data
        # Get own assignments only
        all_assignments = AssignmentRepository.get_all(db)
        own_assignments = [a for a in all_assignments if a.staff_id == current_user.staff_id]
        
        # Get own task instances (task instances assigned to this staff)
        assigned_task_instance_ids = {a.task_instance_id for a in own_assignments if a.task_instance_id}
        all_task_instances = TaskInstanceRepository.get_all(db)
        own_task_instances = [ti for ti in all_task_instances if ti.id in assigned_task_instance_ids]
        
        # For staff count, only show self (1 staff)
        all_staff = [current_user]
        
        # Calculate assignment rate (percentage of own task instances assigned - should be 100% or less)
        total_courses = len(own_task_instances)
        total_assignments = len(own_assignments)
        assignment_rate = 100.0 if total_courses > 0 else 0.0  # All own tasks are assigned
        unassigned = 0  # Staff doesn't see unassigned tasks
        
        # Workload distribution: Only show own workload
        workload_distribution = []
        staff_workloads = {}
        
        for assignment in own_assignments:
            if assignment.task_instance_id:
                task_instance = TaskInstanceRepository.get_by_id(db, assignment.task_instance_id)
                if task_instance:
                    hours = task_instance.effective_hours
                    if assignment.staff_id not in staff_workloads:
                        staff_workloads[assignment.staff_id] = 0.0
                    staff_workloads[assignment.staff_id] += hours
        
        # Build workload distribution (only self)
        workload = staff_workloads.get(current_user.staff_id, 0.0)
        
        # Get max hours from designation workload policy
        policy = db.query(DesignationWorkloadPolicy).filter(
            DesignationWorkloadPolicy.designation == current_user.designation
        ).first()
        
        if policy:
            capacity = policy.max_hours_per_week
        elif current_user.max_hours:
            capacity = current_user.max_hours
        else:
            capacity = 20.0  # Default fallback
        
        workload_distribution.append({
            "name": current_user.name,
            "workload": round(workload, 2),
            "capacity": capacity
        })
        
    else:
        # ADMIN/MANAGEMENT: See all data (university-wide)
        # Get total staff count
        all_staff = StaffRepository.get_all(db)
        total_staff = len(all_staff)
        
        # Get total task instances count (these are the "courses" in the system)
        all_task_instances = TaskInstanceRepository.get_all(db)
        total_courses = len(all_task_instances)
        
        # Get total assignments count
        all_assignments = AssignmentRepository.get_all(db)
        total_assignments = len(all_assignments)
        
        # Calculate assignment rate (percentage of task instances that are assigned)
        assignment_rate = 0.0
        unassigned = total_courses
        if total_courses > 0:
            # Count how many task instances have assignments
            assigned_task_ids = set()
            for assignment in all_assignments:
                if assignment.task_instance_id:
                    assigned_task_ids.add(assignment.task_instance_id)
            
            assigned_count = len(assigned_task_ids)
            unassigned = total_courses - assigned_count
            assignment_rate = (assigned_count / total_courses) * 100
        
        # Get workload distribution data
        # This calculates total hours assigned to each staff member
        workload_distribution = []
        
        # Group assignments by staff_id and sum hours
        staff_workloads = {}
        for assignment in all_assignments:
            if assignment.staff_id and assignment.task_instance_id:
                # Get task instance to get hours
                task_instance = TaskInstanceRepository.get_by_id(db, assignment.task_instance_id)
                if task_instance:
                    hours = task_instance.effective_hours
                    if assignment.staff_id not in staff_workloads:
                        staff_workloads[assignment.staff_id] = 0.0
                    staff_workloads[assignment.staff_id] += hours
        
        # Build workload distribution array
        for staff in all_staff:
            staff_id = staff.staff_id
            workload = staff_workloads.get(staff_id, 0.0)
            
            # Get max hours from designation workload policy
            policy = db.query(DesignationWorkloadPolicy).filter(
                DesignationWorkloadPolicy.designation == staff.designation
            ).first()
            
            if policy:
                capacity = policy.max_hours_per_week
            elif staff.max_hours:
                capacity = staff.max_hours
            else:
                capacity = 20.0  # Default fallback
            
            workload_distribution.append({
                "name": staff.name,
                "workload": round(workload, 2),
                "capacity": capacity
            })
    
    # Get workload fairness data (same as distribution but simplified)
    workload_fairness = [
        {
            "name": item["name"],
            "value": item["workload"]
        }
        for item in workload_distribution
    ]
    
    # Prepare metrics (handle both academic and admin cases)
    if is_academic:
        metrics = {
            "totalStaff": 1,  # Only self
            "totalCourses": total_courses,  # Own task instances
            "totalAssignments": total_assignments,  # Own assignments
            "assignmentRate": round(assignment_rate, 1),
            "unassigned": unassigned
        }
    else:
        metrics = {
            "totalStaff": total_staff,
            "totalCourses": total_courses,
            "totalAssignments": total_assignments,
            "assignmentRate": round(assignment_rate, 1),
            "unassigned": unassigned
        }
    
    return {
        "metrics": metrics,
        "workloadDistribution": workload_distribution,
        "workloadFairness": workload_fairness
    }

