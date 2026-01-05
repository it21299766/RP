"""
Optimization Schemas - Data Validation for GA Optimization API

These Pydantic schemas define the data structures for GA optimization API requests and responses.
They validate incoming data and serialize optimization results for API responses.

THINK OF IT AS: The "contract" between frontend and backend - defines what data is expected for optimization.
"""

from pydantic import BaseModel
from typing import List, Optional


class OptimizationRequest(BaseModel):
    """
    Schema for optimization request (input parameters for GA algorithm).
    
    WHAT: Used when POST /api/optimization/run is called (run GA optimization)
    VALIDATION: All required fields must be provided, validated by Pydantic
    
    EXAMPLE: {"semester": "2025S1", "department": "Computer Science", "allow_admin_override": False}
    
    PURPOSE: Provides filters and configuration for the optimization algorithm
    """
    # SEMESTER: Which semester to optimize for
    # WHAT: Filters task instances to optimize (only instances for this semester)
    # FORMAT: "YYYYSN" where S = S1 (Spring) or S2 (Fall), N = semester number
    # EXAMPLES: "2025S1" (Spring 2025), "2025S2" (Fall 2025)
    semester: str
    
    # DEPARTMENT: Which department to optimize for
    # WHAT: Filters staff and tasks by department
    # EXAMPLES: "Computer Science", "Mathematics", "Physics"
    # NOTE: Only staff and tasks from this department are considered
    department: str
    
    # ALLOW_ADMIN_OVERRIDE: Whether to allow admin overrides
    # WHAT: Flag to indicate if algorithm should consider override constraints
    # DEFAULT: False (strict optimization following all rules)
    # USE CASE: Allow manual adjustments after optimization
    allow_admin_override: bool = False


class OptimizedAssignment(BaseModel):
    """
    Schema for a single optimized assignment (result from GA algorithm).
    
    WHAT: Represents one assignment recommendation from the GA algorithm
    USED IN: OptimizationResponse.assignments (list of recommended assignments)
    
    NOTE: Uses task_instance_id (new system), but keeps task_id for backward compatibility
    """
    # TASK_INSTANCE_ID: Which task instance is assigned (PRIMARY - new system)
    # WHAT: Identifies the specific task instance being assigned
    # EXAMPLE: TaskInstance ID 10 = "DBMS Lecture for BSCS Section A, Fall 2025"
    task_instance_id: int
    
    # STAFF_ID: Which staff member is assigned
    # WHAT: Identifies the staff member recommended for this task
    # EXAMPLE: Staff ID 5 = "Dr. Jane Smith"
    # NOTE: Can be None if task is UNASSIGNED (no eligible staff found)
    staff_id: Optional[int]
    
    # HOURS: Number of hours for this assignment
    # WHAT: Workload hours for this specific assignment
    # EXAMPLE: 2.0 hours, 4.0 hours
    # NOTE: Usually from TaskInstance.effective_hours
    hours: float
    
    # TASK_ID: Legacy field kept for backward compatibility (DEPRECATED)
    # WHAT: Old task_id field - kept for compatibility with legacy code
    # NOTE: Should use task_instance_id instead (new system)
    task_id: Optional[int] = None


class OptimizationSummary(BaseModel):
    """
    Schema for optimization summary statistics.
    
    WHAT: Provides high-level statistics about the optimization results
    USED IN: OptimizationResponse.summary
    
    PURPOSE: Gives overview of optimization quality (balance, distribution, etc.)
    """
    # TOTAL_TASKS: Number of tasks that were optimized
    # WHAT: Count of task instances included in optimization
    # EXAMPLE: 50 tasks
    total_tasks: int
    
    # TOTAL_STAFF: Number of staff members considered
    # WHAT: Count of staff members available for assignment
    # EXAMPLE: 20 staff members
    total_staff: int
    
    # AVG_LOAD: Average workload per staff member
    # WHAT: Mean hours assigned across all staff
    # EXAMPLE: 15.5 hours (average workload)
    # CALCULATION: Sum of all assignments / number of staff
    avg_load: float
    
    # OVERLOADED_STAFF: Number of staff assigned more than 110% of average
    # WHAT: Count of staff who are overworked (more than 1.1 × avg_load)
    # EXAMPLE: 3 staff members are overloaded
    # PURPOSE: Helps identify workload imbalance
    overloaded_staff: int
    
    # UNDERLOADED_STAFF: Number of staff assigned less than 80% of average
    # WHAT: Count of staff who are underworked (less than 0.8 × avg_load)
    # EXAMPLE: 2 staff members are underloaded
    # PURPOSE: Helps identify workload imbalance
    underloaded_staff: int


class OptimizationResponse(BaseModel):
    """
    Schema for optimization API response (complete optimization results).
    
    WHAT: Used when POST /api/optimization/run returns results
    CONTAINS: Status, summary statistics, list of assignments, and any warnings
    
    PURPOSE: Returns complete optimization results from GA algorithm
    """
    # STATUS: Overall status of the optimization
    # WHAT: Indicates if optimization was successful
    # VALUES: "SUCCESS", "FAILED"
    # EXAMPLES: "SUCCESS" if optimization completed, "FAILED" if errors occurred
    status: str
    
    # SUMMARY: High-level statistics about optimization
    # WHAT: Overview of optimization quality (balance, distribution, etc.)
    # TYPE: OptimizationSummary object (total_tasks, total_staff, avg_load, etc.)
    summary: OptimizationSummary
    
    # ASSIGNMENTS: List of recommended assignments
    # WHAT: All task-staff assignments recommended by GA algorithm
    # TYPE: List of OptimizedAssignment objects
    # EXAMPLE: [{"task_instance_id": 10, "staff_id": 5, "hours": 2.0}, ...]
    assignments: List[OptimizedAssignment]
    
    # WARNINGS: Optional list of warnings or messages
    # WHAT: Additional information about optimization (warnings, notes, etc.)
    # TYPE: List of strings (optional, defaults to empty list)
    # EXAMPLES: ["Some tasks could not be assigned", "Low staff availability"]
    warnings: Optional[List[str]] = []
