"""
Optimization Service - Business Logic for Workload Optimization

This service handles workload optimization using the Genetic Algorithm (GA).
It coordinates between the database (staff, task instances) and the GA engine.

THINK OF IT AS: The "orchestration layer" that:
1. Retrieves staff and task instances from database
2. Converts them to GA-compatible format
3. Runs the GA optimization algorithm
4. Returns optimization results

WHY THIS SERVICE?
- Separates optimization logic from API layer
- Handles data conversion (database models → GA dataclasses)
- Manages GA configuration and execution
- Provides clean interface for optimization operations
"""

from sqlalchemy.orm import Session
from app.schemas.optimization import OptimizationResponse, OptimizationSummary
from app.repositories.staff_repository import StaffRepository
from app.repositories.task_instance_repository import TaskInstanceRepository
from app.repositories.task_template_repository import TaskTemplateRepository
from app.repositories.program_repository import ProgramRepository
from app.repositories.domain_repository import DomainRepository
from app.ga_engine_v3 import run_ga, GAConfig, Staff as GAStaff, Task as GATask, UNASSIGNED, TASK_CATEGORY_TEACHING, TASK_CATEGORY_RESEARCH, TASK_CATEGORY_ADMIN
from app.models.staff import Staff as StaffModel
from app.models.task_instance import TaskInstance
from app.models.task_template import TaskTemplate
from app.models.designation_workload_policy import DesignationWorkloadPolicy
from typing import List


class OptimizationService:
    """
    Service class for optimization business logic.
    
    This class contains methods that implement business rules for workload optimization.
    It uses the GA engine to optimize task assignments.
    """

    @staticmethod
    def _get_staff_max_hours(db: Session, staff: StaffModel) -> float:
        """
        Get max hours for staff from DesignationWorkloadPolicy.
        
        BUSINESS LOGIC:
        1. Look up workload policy by staff designation
        2. Return max_hours_per_week from policy if found
        3. Fall back to staff.max_hours if policy not found
        4. Fall back to default 20.0 hours if neither exists
        
        WHY THIS LOGIC:
        - New system uses DesignationWorkloadPolicy (flexible, centralized)
        - Old system used staff.max_hours (deprecated but kept for compatibility)
        - Default ensures we always have a value (safety fallback)
        
        PRIORITY: Policy > staff.max_hours > default (20.0)
        
        RETRIEVES FROM DB:
        - DesignationWorkloadPolicy table (lookup by designation)
        - Staff table (max_hours field, if policy not found)
        
        Args:
            db: Database session
            staff: Staff model object
        
        Returns:
            Maximum hours per week (float)
        """
        # STEP 1: Look up workload policy by designation
        policy = db.query(DesignationWorkloadPolicy).filter(
            DesignationWorkloadPolicy.designation == staff.designation
        ).first()
        
        # STEP 2: Return policy max hours if found
        if policy:
            return policy.max_hours_per_week
        # STEP 3: Fall back to staff.max_hours (deprecated but kept for compatibility)
        elif staff.max_hours:
            return staff.max_hours
        # STEP 4: Fall back to default (safety fallback)
        else:
            return 20.0  # Default fallback

    @staticmethod
    def _convert_staff_to_ga(staff_list: List[StaffModel], db: Session) -> List[GAStaff]:
        """
        Convert SQLAlchemy Staff models to GA Staff dataclasses.
        
        WHAT THIS DOES: Transforms database Staff models into GA-compatible Staff objects.
        The GA algorithm uses its own dataclasses (not SQLAlchemy models).
        
        CONVERSION LOGIC:
        - staff_id: Direct mapping
        - max_hours: Looked up from DesignationWorkloadPolicy (via _get_staff_max_hours)
        - qualification: Direct mapping
        - specialty: Maps from specialization (GA uses 'specialty', model uses 'specialization')
        - skills: Direct mapping (JSON field → list)
        - experience: Maps from experience_years
        - available: Direct mapping
        
        WHY CONVERSION:
        - GA algorithm uses simple dataclasses (no SQLAlchemy dependencies)
        - Separates optimization logic from database models
        - Makes GA algorithm reusable/testable without database
        
        RETRIEVES FROM DB:
        - DesignationWorkloadPolicy (for max_hours lookup)
        
        Args:
            staff_list: List of Staff SQLAlchemy models
            db: Database session (for looking up workload policies)
        
        Returns:
            List of GA Staff dataclass objects
        """
        ga_staff = []
        for staff in staff_list:
            # Get max hours from workload policy (or fallback)
            max_hours = OptimizationService._get_staff_max_hours(db, staff)
            
            # Convert to GA Staff dataclass
            ga_staff.append(GAStaff(
                staff_id=staff.staff_id,
                max_hours=max_hours,  # From policy lookup
                qualification=staff.qualification,
                specialty=staff.specialization,  # Note: GA uses 'specialty', model uses 'specialization'
                skills=staff.skills or [],
                experience=staff.experience_years,  # Maps from experience_years
                available=staff.available,
                department=staff.department,  # NEW: Department field
                role=staff.role  # NEW: Role field (ACADEMIC, ADMIN, MANAGEMENT)
            ))
        return ga_staff

    @staticmethod
    def _convert_task_instances_to_ga(
        task_instances: List[TaskInstance],
        db: Session
    ) -> List[GATask]:
        """
        Convert TaskInstance models to GA Task dataclasses.
        
        WHAT THIS DOES: Transforms database TaskInstance models into GA-compatible Task objects.
        Combines data from TaskInstance (temporal info, hours) and TaskTemplate (requirements).
        
        CONVERSION LOGIC:
        - task_id: Uses TaskInstance.id (instance ID, not template ID)
        - tariff_hours: From TaskInstance.effective_hours (actual hours for this instance)
        - required_qualification: From TaskTemplate.required_qualification_level
        - required_specialty: From TaskTemplate.required_specialization
        - required_skills: From TaskTemplate.required_skills
        - required_experience: From TaskTemplate.required_experience_years
        
        WHY COMBINE INSTANCE + TEMPLATE:
        - TaskInstance has temporal info (semester, program, hours)
        - TaskTemplate has requirements (qualification, skills, experience)
        - GA needs both: what needs to be done (template) and when/where (instance)
        
        RETRIEVES FROM DB:
        - TaskTemplate table (lookup by task_template_id)
        
        Args:
            task_instances: List of TaskInstance SQLAlchemy models
            db: Database session (for looking up task templates)
        
        Returns:
            List of GA Task dataclass objects
        
        NOTE: Skips instances if template not found (defensive programming)
        """
        ga_tasks = []
        for instance in task_instances:
            # Get template for requirements (qualification, skills, etc.)
            template = TaskTemplateRepository.get_by_id(db, instance.task_template_id)
            if not template:
                continue  # Skip if template not found (defensive)
            
            # Get program to derive department
            program = ProgramRepository.get_by_id(db, instance.program_id)
            department = ""
            if program:
                # Get domain to use as department
                domain = DomainRepository.get_by_id(db, program.domain_id)
                if domain:
                    department = domain.name
            
            # Map task_type to category
            task_type = template.task_type.lower()
            if task_type in ["lecture", "lab", "tutorial", "exam"]:
                category = TASK_CATEGORY_TEACHING
            elif task_type == "research":
                category = TASK_CATEGORY_RESEARCH
            elif task_type == "admin":
                category = TASK_CATEGORY_ADMIN
            else:
                # Default to Teaching for unknown types
                category = TASK_CATEGORY_TEACHING
            
            # Convert to GA Task dataclass (combines instance + template data)
            ga_tasks.append(GATask(
                task_id=instance.id,  # Use instance ID (not template ID)
                tariff_hours=instance.effective_hours,  # Actual hours for this instance
                required_qualification=template.required_qualification_level,
                required_specialty=template.required_specialization or "",
                required_skills=template.required_skills or [],
                required_experience=template.required_experience_years,
                department=department,  # NEW: Department from program's domain
                category=category  # NEW: Category mapped from task_type
            ))
        return ga_tasks

    @staticmethod
    def run_optimization(db: Session, data):
        """
        Run GA optimization on approved task instances.
        
        BUSINESS LOGIC:
        This method orchestrates the entire optimization process:
        1. Get available staff (filter by available and is_active)
        2. Get approved task instances (only approved instances can be assigned)
        3. Convert staff and tasks to GA format
        4. Run GA algorithm with configuration
        5. Convert results back to response format
        
        FILTERING:
        - Staff: Only available and active staff (available=True, is_active=True)
        - Tasks: Only approved task instances (status="approved")
        
        WHY APPROVED ONLY:
        - Draft instances are not yet finalized (shouldn't be assigned)
        - Completed instances are already done (shouldn't be assigned)
        - Only approved instances need assignment
        
        GA CONFIGURATION:
        - Uses default GAConfig (can be customized via data parameter)
        - Generations, population size, etc. can be adjusted
        
        RETRIEVES FROM DB:
        - Staff table (all available, active staff)
        - TaskInstance table (approved instances)
        - TaskTemplate table (for task requirements)
        - DesignationWorkloadPolicy table (for staff max hours)
        
        Args:
            db: Database session
            data: OptimizationRequest with optional filters (department, semester, etc.)
        
        Returns:
            OptimizationResponse with assignments and summary
        
        NOTE: Currently filters are not fully implemented (TODO in code)
        """
        # STEP 1: Get available staff
        # TODO: Filter by department if provided in data
        staff_list = StaffRepository.get_all(db)
        # Filter: Only available and active staff
        staff_list = [s for s in staff_list if s.available and s.is_active]
        
        # STEP 2: Get approved task instances (only approved instances can be assigned)
        task_instances = TaskInstanceRepository.get_approved(db)
        
        # STEP 3: Apply filters if provided
        if hasattr(data, 'department') and data.department:
            staff_list = [s for s in staff_list if s.department == data.department]
            # Filter task instances by department (would need to join with program)
            # For now, get all approved instances
        
        if hasattr(data, 'semester') and data.semester:
            task_instances = [ti for ti in task_instances if ti.semester == data.semester]
        
        warnings = []

        # STEP 4: Validate we have staff and tasks
        if not staff_list:
            return {"status": "FAILED", "warnings": ["No staff available"]}

        if not task_instances:
            return {"status": "FAILED", "warnings": ["No approved task instances available"]}

        # STEP 5: Convert database models to GA dataclasses
        ga_staff = OptimizationService._convert_staff_to_ga(staff_list, db)
        ga_tasks = OptimizationService._convert_task_instances_to_ga(task_instances, db)
        
        if not ga_tasks:
            return {"status": "FAILED", "warnings": ["No valid task instances found"]}

        # STEP 6: Configure GA (use default config, can be customized via data parameter)
        config = GAConfig()
        if hasattr(data, 'generations'):
            config.generations = data.generations
        if hasattr(data, 'pop_size'):
            config.pop_size = data.pop_size
        
        # STEP 7: Run GA optimization algorithm
        result = run_ga(ga_staff, ga_tasks, config)

        # STEP 8: Validate GA results
        workloads = result.workloads
        if not workloads:
            return {"status": "FAILED", "warnings": ["Optimization produced no results"]}
        
        # STEP 9: Calculate workload statistics
        avg_load = sum(workloads.values()) / len(workloads) if workloads else 0
        overloaded = sum(1 for v in workloads.values() if v > 1.1 * avg_load)  # More than 110% of average
        underloaded = sum(1 for v in workloads.values() if v < 0.8 * avg_load)  # Less than 80% of average

        # STEP 10: Convert GA results to response format (assignments)
        assignments = []
        for task_idx, staff_id in enumerate(result.best_chromosome):
            if task_idx < len(task_instances):
                instance = task_instances[task_idx]
                # Handle UNASSIGNED tasks
                if staff_id == UNASSIGNED:
                    warnings.append(f"Task {instance.id} could not be assigned (no eligible staff)")
                    assignments.append({
                        "task_instance_id": instance.id,
                        "staff_id": None,  # UNASSIGNED
                        "hours": instance.effective_hours
                    })
                else:
                    assignments.append({
                        "task_instance_id": instance.id,
                        "staff_id": staff_id,
                        "hours": instance.effective_hours
                    })
        
        # Determine status based on GA result
        status = "SUCCESS" if result.success else "PARTIAL" if len(assignments) > 0 else "FAILED"
        if not result.success and result.reason:
            warnings.append(result.reason)

        return OptimizationResponse(
            status=status,
            summary=OptimizationSummary(
                total_tasks=len(ga_tasks),
                total_staff=len(ga_staff),
                avg_load=round(avg_load, 2),
                overloaded_staff=overloaded,
                underloaded_staff=underloaded
            ),
            assignments=assignments,
            warnings=warnings
        )
