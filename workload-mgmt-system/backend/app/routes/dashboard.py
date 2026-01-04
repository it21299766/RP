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
    - Total staff count
    - Total task instances (courses) count
    - Total assignments count
    - Assignment rate (percentage of tasks assigned)
    - Workload distribution by staff
    - Workload fairness data
    
    RETRIEVES FROM DB:
    - Staff table (count of all staff)
    - TaskInstance table (count of all task instances)
    - Assignment table (count of all assignments)
    - Assignment table with staff (for workload distribution)
    
    Args:
        db: Database session
        current_user: Currently authenticated user
    
    Returns:
        Dictionary with metrics, workloadDistribution, and workloadFairness
    """
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
    
    return {
        "metrics": {
            "totalStaff": total_staff,
            "totalCourses": total_courses,
            "totalAssignments": total_assignments,
            "assignmentRate": round(assignment_rate, 1),
            "unassigned": unassigned
        },
        "workloadDistribution": workload_distribution,
        "workloadFairness": workload_fairness
    }

