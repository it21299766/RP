"""
Genetic Algorithm Engine V3 - Enhanced with Real-World Academic Constraints

WHAT THIS FILE DOES:
This file implements an enhanced Genetic Algorithm (GA) for workload assignment with
real-world academic constraints including:
- Subject/specialization enforcement (HARD CONSTRAINT)
- Department enforcement (HARD CONSTRAINT)
- Role-based restrictions (ADMIN/MANAGEMENT cannot teach)
- Task category awareness (Teaching vs Research vs Admin)
- Unassignable task handling (UNASSIGNED = -1)

HOW IT WORKS:
1. Start with 50 random ways to assign tasks (initial population)
2. For each assignment, calculate how "good" it is (fitness function)
3. Keep the best assignments and use them to create new ones (selection + crossover)
4. Add some randomness to explore new possibilities (mutation)
5. Repeat for 100 generations, getting better each time
6. Return the best assignment found (or failure reason if unassignable)

ENHANCEMENTS OVER V2:
- Centralized eligibility function (is_staff_eligible_for_task)
- Hard department matching for teaching tasks
- Hard specialization matching for teaching tasks
- Role-based restrictions (ADMIN/MANAGEMENT cannot teach)
- Task category awareness (Teaching/Research/Admin)
- UNASSIGNED task handling with clear failure reasons
- Success/failure reporting in GAResult
"""

import random
import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum


# -------------------------------------------
# Constants
# -------------------------------------------

# Qualification hierarchy: PhD > MSc > BSc
QUAL_RANK = {"BSc": 1, "MSc": 2, "PhD": 3}

# Special constant for unassignable tasks
UNASSIGNED = -1

# Task categories
TASK_CATEGORY_TEACHING = "Teaching"
TASK_CATEGORY_RESEARCH = "Research"
TASK_CATEGORY_ADMIN = "Admin"

# Staff roles
ROLE_ACADEMIC = "ACADEMIC"
ROLE_ADMIN = "ADMIN"
ROLE_MANAGEMENT = "MANAGEMENT"


# -------------------------------------------
# Configuration Dataclass
# -------------------------------------------
@dataclass
class GAConfig:
    """
    Configuration for GA optimization.
    
    This class stores all the "settings" for the genetic algorithm.
    You can adjust these to change how the algorithm behaves.
    """
    # Evolution parameters
    generations: int = 100
    pop_size: int = 50
    crossover_rate: float = 0.8
    mutation_rate: float = 0.05
    tournament_k: int = 3
    elitism_count: int = 2
    seed: Optional[int] = None
    enforce_hard_constraints: bool = True
    early_stopping_generations: int = 20
    
    # Fitness weights
    stdev_weight: float = 1.0
    overload_multiplier: float = 5.0
    hard_penalty: float = 100.0
    soft_penalty: float = 1.0
    match_bonus_specialty: float = 3.0
    match_bonus_skill: float = 2.0
    match_bonus_experience: float = 1.0
    unassigned_penalty: float = 1000.0  # Very high penalty for UNASSIGNED tasks
    
    def __post_init__(self):
        """Validate configuration."""
        if self.pop_size < 2:
            raise ValueError("pop_size must be >= 2")
        if not (0 <= self.crossover_rate <= 1):
            raise ValueError("crossover_rate must be in [0, 1]")
        if not (0 <= self.mutation_rate <= 1):
            raise ValueError("mutation_rate must be in [0, 1]")
        if self.tournament_k < 2:
            raise ValueError("tournament_k must be >= 2")
        if self.elitism_count > self.pop_size // 2:
            raise ValueError("elitism_count must be <= pop_size // 2")


# -------------------------------------------
# Data Classes
# -------------------------------------------
@dataclass
class Staff:
    """
    Represents a staff member with qualifications, department, and role.
    
    NEW FIELDS IN V3:
    - department: Academic department (e.g., "Computer Science", "Physics")
    - role: Staff role (ACADEMIC, ADMIN, MANAGEMENT)
    """
    staff_id: int
    max_hours: float
    qualification: str  # "BSc", "MSc", "PhD"
    specialty: str  # Field of expertise (e.g., "Computer Science", "Physics")
    skills: List[str] = field(default_factory=list)
    experience: int = 0
    available: bool = True
    department: str = ""  # NEW: Academic department
    role: str = ROLE_ACADEMIC  # NEW: Staff role (ACADEMIC, ADMIN, MANAGEMENT)
    
    def __post_init__(self):
        """Validate staff data."""
        if self.qualification not in QUAL_RANK:
            raise ValueError(f"Invalid qualification: {self.qualification}")
        if self.max_hours <= 0:
            raise ValueError("max_hours must be > 0")
        if self.experience < 0:
            raise ValueError("experience must be >= 0")
        if self.role not in [ROLE_ACADEMIC, ROLE_ADMIN, ROLE_MANAGEMENT]:
            raise ValueError(f"Invalid role: {self.role}")
    
    def meets_requirement(self, required_qual: str) -> bool:
        """Check if staff meets minimum qualification requirement."""
        return QUAL_RANK[self.qualification] >= QUAL_RANK[required_qual]


@dataclass
class Task:
    """
    Represents a workload task with requirements.
    
    NEW FIELDS IN V3:
    - department: Department this task belongs to
    - category: Task category (Teaching, Research, Admin)
    """
    task_id: int
    tariff_hours: float
    required_qualification: str  # "BSc", "MSc", "PhD"
    required_specialty: str  # Preferred specialty
    required_skills: List[str] = field(default_factory=list)
    required_experience: int = 0
    department: str = ""  # NEW: Department this task belongs to
    category: str = TASK_CATEGORY_TEACHING  # NEW: Task category (Teaching, Research, Admin)
    
    def __post_init__(self):
        """Validate task data."""
        if self.required_qualification not in QUAL_RANK:
            raise ValueError(f"Invalid qualification: {self.required_qualification}")
        if self.tariff_hours <= 0:
            raise ValueError("tariff_hours must be > 0")
        if self.required_experience < 0:
            raise ValueError("required_experience must be >= 0")
        if self.category not in [TASK_CATEGORY_TEACHING, TASK_CATEGORY_RESEARCH, TASK_CATEGORY_ADMIN]:
            raise ValueError(f"Invalid category: {self.category}")


@dataclass
class GAResult:
    """
    Result of GA optimization run.
    
    NEW FIELDS IN V3:
    - success: Whether all tasks were successfully assigned
    - reason: Failure reason if success=False
    """
    best_chromosome: List[int]
    best_fitness: float
    workloads: Dict[int, float]
    generations_run: int
    converged: bool
    fitness_history: List[float] = field(default_factory=list)
    assignment_details: List[Tuple[int, int, float]] = field(default_factory=list)
    constraint_violations: int = 0
    success: bool = True  # NEW: Whether optimization succeeded
    reason: Optional[str] = None  # NEW: Failure reason if success=False


# -------------------------------------------
# Eligibility Function (NEW - CENTRALIZED)
# -------------------------------------------
def is_staff_eligible_for_task(staff: Staff, task: Task) -> bool:
    """
    Centralized eligibility check for staff-task assignment.
    
    WHAT THIS DOES: Checks if a staff member can be assigned to a task based on
    ALL hard constraints: availability, qualification, department, specialty, role.
    
    HARD CONSTRAINTS (all must pass):
    1. Staff must be available
    2. Staff qualification must meet task requirement
    3. For Teaching tasks:
       - Staff department must match task department
       - Staff specialty must match task required_specialty
       - Staff role must be ACADEMIC (ADMIN/MANAGEMENT cannot teach)
    4. For non-Teaching tasks:
       - Role restrictions don't apply (ADMIN/MANAGEMENT can do admin/research)
    
    EXAMPLE 1: Teaching Task
    - Task: Teaching, CS department, requires MSc, CS specialty
    - Staff: ACADEMIC, CS department, MSc, CS specialty, available=True
    - Result: ✅ Eligible (all checks pass)
    
    EXAMPLE 2: Teaching Task, Wrong Department
    - Task: Teaching, CS department, requires MSc
    - Staff: ACADEMIC, Physics department, PhD, Physics specialty, available=True
    - Result: ❌ Not eligible (department mismatch)
    
    EXAMPLE 3: Teaching Task, Admin Role
    - Task: Teaching, CS department, requires MSc
    - Staff: ADMIN, CS department, PhD, CS specialty, available=True
    - Result: ❌ Not eligible (ADMIN cannot teach)
    
    EXAMPLE 4: Admin Task, Admin Role
    - Task: Admin, any department
    - Staff: ADMIN, any department, available=True
    - Result: ✅ Eligible (non-teaching tasks don't require ACADEMIC role)
    
    Args:
        staff: Staff member to check
        task: Task to check eligibility for
    
    Returns:
        True if staff is eligible, False otherwise
    """
    # 1. Availability check (HARD CONSTRAINT)
    if not staff.available:
        return False
    
    # 2. Qualification check (HARD CONSTRAINT)
    if not staff.meets_requirement(task.required_qualification):
        return False
    
    # 3. Task category-specific checks
    if task.category == TASK_CATEGORY_TEACHING:
        # Teaching tasks have strict requirements:
        # - Department must match (HARD CONSTRAINT)
        if staff.department != task.department:
            return False
        
        # - Specialty must match (HARD CONSTRAINT)
        if staff.specialty != task.required_specialty:
            return False
        
        # - Only ACADEMIC role can teach (HARD CONSTRAINT)
        if staff.role != ROLE_ACADEMIC:
            return False
    
    # For Research and Admin tasks, department/specialty matching is not required
    # (they can be assigned across departments if needed)
    # Role restrictions also don't apply (ADMIN/MANAGEMENT can do admin/research)
    
    return True


# -------------------------------------------
# GA Helper Functions
# -------------------------------------------
def get_eligible_staff(task: Task, staff_map: Dict[int, Staff]) -> List[int]:
    """
    Get list of staff IDs eligible for a task using centralized eligibility function.
    
    WHAT THIS DOES: Finds all staff who CAN do a task using is_staff_eligible_for_task.
    
    Args:
        task: Task to find eligible staff for
        staff_map: Dictionary mapping staff_id → Staff object
    
    Returns:
        List of eligible staff IDs (empty if none eligible)
    """
    eligible = []
    for staff_id, staff in staff_map.items():
        if is_staff_eligible_for_task(staff, task):
            eligible.append(staff_id)
    return eligible


def generate_initial_population_eligible(
    tasks: List[Task],
    staff_list: List[Staff],
    pop_size: int = 50,
    allow_overload: bool = True,
    enforce_hard_constraints: bool = True
) -> List[List[int]]:
    """
    Generate initial population respecting eligibility constraints.
    
    WHAT THIS DOES: Creates the first generation of random solutions (assignments).
    Uses UNASSIGNED = -1 when no eligible staff exists for a task.
    
    EXAMPLE OUTPUT:
    [
        [1, 2, -1, 3, 2],  # Task 3 has no eligible staff (UNASSIGNED = -1)
        [2, 1, 3, 1, 2],  # All tasks assigned
        [1, -1, 2, 2, 1],  # Task 2 unassignable
        # ... more solutions
    ]
    
    Args:
        tasks: List of tasks to assign
        staff_list: List of available staff
        pop_size: Population size
        allow_overload: If False, try to stay within max_hours
        enforce_hard_constraints: If True, only assign eligible staff
    
    Returns:
        Population of chromosomes (list of solutions, each solution is a list of staff IDs or UNASSIGNED)
    """
    staff_map = {s.staff_id: s for s in staff_list}
    staff_ids = list(staff_map.keys())
    population = []
    
    if not staff_ids:
        raise ValueError("No staff available for assignment")
    if not tasks:
        raise ValueError("No tasks to assign")
    
    for _ in range(pop_size):
        chromosome = []
        remaining_capacity = {s.staff_id: s.max_hours for s in staff_list}
        
        for task in tasks:
            if enforce_hard_constraints:
                eligible = get_eligible_staff(task, staff_map)
                if not eligible:
                    # No eligible staff - assign UNASSIGNED
                    pick = UNASSIGNED
                else:
                    # Pick from eligible; optionally respect remaining capacity
                    if not allow_overload:
                        candidates = [sid for sid in eligible if remaining_capacity[sid] >= task.tariff_hours]
                        pick = random.choice(candidates) if candidates else random.choice(eligible)
                    else:
                        pick = random.choice(eligible)
            else:
                pick = random.choice(staff_ids)
            
            chromosome.append(pick)
            if pick != UNASSIGNED:
                remaining_capacity[pick] -= task.tariff_hours
        
        population.append(chromosome)
    
    return population


def compute_workload(
    chromosome: List[int],
    tasks: List[Task]
) -> Dict[int, float]:
    """
    Compute total workload (tariff hours) assigned to each staff member.
    
    WHAT THIS DOES: Calculates total hours assigned to each staff member.
    Skips UNASSIGNED tasks (they don't contribute to workload).
    
    Args:
        chromosome: List of staff IDs (one per task, or UNASSIGNED = -1)
        tasks: List of tasks with their hours
    
    Returns:
        Dictionary mapping staff_id → total_hours
    """
    workloads = {}
    for gene, task in zip(chromosome, tasks):
        if gene != UNASSIGNED:
            if gene not in workloads:
                workloads[gene] = 0
            workloads[gene] += task.tariff_hours
    return workloads


def compute_fitness(
    chromosome: List[int],
    tasks: List[Task],
    staff_map: Dict[int, Staff],
    config: GAConfig
) -> float:
    """
    Compute fitness score (lower is better).
    
    WHAT THIS DOES: Evaluates how good a solution is.
    
    THE FITNESS FUNCTION HAS 6 COMPONENTS:
      1. Workload balance (std dev penalty)
      2. Overload penalty (squared hours over max)
      3. UNASSIGNED penalty (very high - immediate failure)
      4. Hard constraint violations (qualification, department, specialty, role)
      5. Soft constraint penalties (skill/experience mismatches)
      6. Soft bonuses (matches)
    
    NEW IN V3:
    - Immediate hard failure if UNASSIGNED exists (very high penalty)
    - Hard penalty for department/specialty mismatches in teaching tasks
    - Hard penalty for role violations (ADMIN/MANAGEMENT teaching)
    
    Args:
        chromosome: The solution to evaluate (list of staff IDs or UNASSIGNED)
        tasks: List of tasks
        staff_map: Dictionary mapping staff_id → Staff object
        config: GA configuration
    
    Returns:
        Fitness score (float) - lower is better
    """
    workloads = compute_workload(chromosome, tasks)
    all_staff_ids = set(staff_map.keys())
    
    # Ensure all staff appear in workload dict (for stdev calculation)
    for sid in all_staff_ids:
        if sid not in workloads:
            workloads[sid] = 0
    
    # --------------------------
    # 1. Workload balance (stdev penalty)
    # --------------------------
    loads = list(workloads.values())
    if len(loads) > 1:
        stdev = statistics.pstdev(loads)
    else:
        stdev = 0
    stdev_penalty = stdev * config.stdev_weight
    
    # --------------------------
    # 2. Overload penalty
    # --------------------------
    overload_penalty = 0.0
    for staff_id, load in workloads.items():
        max_hours = staff_map[staff_id].max_hours
        if load > max_hours:
            excess = load - max_hours
            overload_penalty += (excess ** 2) * config.overload_multiplier
    
    # --------------------------
    # 3. UNASSIGNED penalty (NEW - IMMEDIATE FAILURE)
    # --------------------------
    unassigned_penalty = 0.0
    unassigned_count = 0
    for gene in chromosome:
        if gene == UNASSIGNED:
            unassigned_count += 1
            unassigned_penalty += config.unassigned_penalty
    
    # --------------------------
    # 4. Hard constraint violations (qualification, department, specialty, role)
    # --------------------------
    hard_penalty = 0.0
    match_bonus = 0.0
    soft_penalty = 0.0
    
    for gene, task in zip(chromosome, tasks):
        if gene == UNASSIGNED:
            continue  # Skip UNASSIGNED (already penalized)
        
        staff = staff_map[gene]
        
        # Hard qualification mismatch (scaled by task hours)
        if not staff.meets_requirement(task.required_qualification):
            hard_penalty += config.hard_penalty * task.tariff_hours
        
        # For Teaching tasks: department and specialty are HARD constraints
        if task.category == TASK_CATEGORY_TEACHING:
            # Department mismatch (HARD CONSTRAINT)
            if staff.department != task.department:
                hard_penalty += config.hard_penalty * task.tariff_hours
            
            # Specialty mismatch (HARD CONSTRAINT)
            if staff.specialty != task.required_specialty:
                hard_penalty += config.hard_penalty * task.tariff_hours
            
            # Role violation (ADMIN/MANAGEMENT cannot teach) (HARD CONSTRAINT)
            if staff.role != ROLE_ACADEMIC:
                hard_penalty += config.hard_penalty * task.tariff_hours
        else:
            # For non-Teaching tasks: specialty matching is soft (bonus/penalty)
            if staff.specialty == task.required_specialty:
                match_bonus += config.match_bonus_specialty * task.tariff_hours
            else:
                soft_penalty += config.soft_penalty * task.tariff_hours
        
        # Skill match (soft constraint)
        skill_matches = len(set(staff.skills) & set(task.required_skills))
        match_bonus += skill_matches * config.match_bonus_skill * task.tariff_hours
        if skill_matches == 0 and task.required_skills:
            soft_penalty += config.soft_penalty * task.tariff_hours
        
        # Experience match (soft constraint)
        if staff.experience >= task.required_experience:
            match_bonus += config.match_bonus_experience * task.tariff_hours
        else:
            gap = task.required_experience - staff.experience
            soft_penalty += gap * config.soft_penalty * task.tariff_hours
    
    # Final fitness (lower is better)
    fitness_score = stdev_penalty + overload_penalty + unassigned_penalty + hard_penalty + soft_penalty - match_bonus
    return fitness_score


def tournament_select(
    population: List[List[int]],
    fitnesses: List[float],
    k: int = 3
) -> List[int]:
    """
    Select a chromosome via tournament selection.
    
    WHAT THIS DOES: Picks a chromosome for reproduction using tournament selection.
    
    Args:
        population: Current population
        fitnesses: Fitness scores (lower is better)
        k: Tournament size
    
    Returns:
        Selected chromosome
    """
    k = min(k, len(population))
    items = list(zip(population, fitnesses))
    selected = random.sample(items, k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]


def crossover(
    p1: List[int],
    p2: List[int],
    rate: float = 0.8
) -> Tuple[List[int], List[int]]:
    """
    Single-point crossover with safe handling of edge cases.
    
    WHAT THIS DOES: Combines two parent chromosomes to create two children.
    
    Args:
        p1: Parent 1 chromosome
        p2: Parent 2 chromosome
        rate: Crossover probability
    
    Returns:
        Tuple of (child1, child2)
    """
    if len(p1) < 2 or random.random() > rate:
        return p1[:], p2[:]
    
    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2


def mutate(
    chromosome: List[int],
    tasks: List[Task],
    staff_map: Dict[int, Staff],
    rate: float = 0.05
) -> List[int]:
    """
    Random mutation with eligibility-aware replacement.
    
    WHAT THIS DOES: Randomly changes some genes (assignments) to add variety.
    When mutating, tries to assign eligible staff (or UNASSIGNED if none).
    
    NEW IN V3: Mutation respects eligibility constraints.
    
    Args:
        chromosome: Chromosome to mutate
        tasks: List of tasks (needed for eligibility check)
        staff_map: Dictionary mapping staff_id → Staff object
        rate: Mutation rate
    
    Returns:
        Mutated chromosome
    """
    staff_ids = list(staff_map.keys())
    
    for i in range(len(chromosome)):
        if random.random() < rate:
            task = tasks[i]
            # Try to assign eligible staff
            eligible = get_eligible_staff(task, staff_map)
            if eligible:
                chromosome[i] = random.choice(eligible)
            else:
                # No eligible staff - assign UNASSIGNED
                chromosome[i] = UNASSIGNED
    
    return chromosome


# -------------------------------------------
# GA RUNNER
# -------------------------------------------
def run_ga(
    staff_list: List[Staff],
    tasks: List[Task],
    config: GAConfig = None
) -> GAResult:
    """
    Run genetic algorithm for workload assignment with enhanced constraints.
    
    WHAT THIS DOES: Main function that runs the entire genetic algorithm.
    
    THE BIG PICTURE:
    1. Create initial population (50 random solutions)
    2. For each generation (100 times):
       a. Evaluate fitness of all solutions
       b. Keep best solutions (elitism)
       c. Select parents (tournament selection)
       d. Create children (crossover)
       e. Mutate children (with eligibility awareness)
       f. Replace population with new generation
    3. Return the best solution found (or failure reason)
    
    NEW IN V3:
    - Checks for unassignable tasks before/after optimization
    - Sets success=False and reason if tasks remain UNASSIGNED
    - Mutation uses eligibility function
    
    Args:
        staff_list: List of staff members
        tasks: List of tasks to assign
        config: GA configuration (uses default if None)
    
    Returns:
        GAResult object with success/reason fields
    """
    if config is None:
        config = GAConfig()
    
    if config.seed is not None:
        random.seed(config.seed)
    
    if not staff_list:
        raise ValueError("staff_list cannot be empty")
    if not tasks:
        raise ValueError("tasks cannot be empty")
    
    staff_map = {s.staff_id: s for s in staff_list}
    staff_ids = [s.staff_id for s in staff_list]
    
    # Validate staff availability
    available_staff = [s for s in staff_list if s.available]
    if not available_staff:
        raise ValueError("No available staff for assignment")
    
    # Check for unassignable tasks BEFORE optimization
    unassignable_tasks = []
    for task in tasks:
        eligible = get_eligible_staff(task, staff_map)
        if not eligible:
            unassignable_tasks.append(task.task_id)
    
    # 1. Initial population
    population = generate_initial_population_eligible(
        tasks,
        staff_list,
        pop_size=config.pop_size,
        enforce_hard_constraints=config.enforce_hard_constraints
    )
    
    best_fitness_overall = float('inf')
    generations_without_improvement = 0
    fitness_history = []
    
    # 2. Evolution loop
    for gen in range(config.generations):
        fitnesses = [compute_fitness(ch, tasks, staff_map, config) for ch in population]
        
        # Track best
        best_fit_gen = min(fitnesses)
        fitness_history.append(best_fit_gen)
        
        if best_fit_gen < best_fitness_overall:
            best_fitness_overall = best_fit_gen
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        
        # Early stopping
        if generations_without_improvement >= config.early_stopping_generations:
            break
        
        # Elitism: keep top N
        elite_indices = sorted(
            range(len(fitnesses)),
            key=lambda i: fitnesses[i]
        )[:config.elitism_count]
        new_pop = [population[i][:] for i in elite_indices]
        
        # Generate rest
        while len(new_pop) < config.pop_size:
            p1 = tournament_select(population, fitnesses, k=config.tournament_k)
            p2 = tournament_select(population, fitnesses, k=config.tournament_k)
            c1, c2 = crossover(p1, p2, rate=config.crossover_rate)
            
            mutate(c1, tasks, staff_map, rate=config.mutation_rate)
            new_pop.append(c1)
            
            if len(new_pop) < config.pop_size:
                mutate(c2, tasks, staff_map, rate=config.mutation_rate)
                new_pop.append(c2)
        
        population = new_pop[:config.pop_size]
    
    # Evaluate best
    final_fitnesses = [compute_fitness(ch, tasks, staff_map, config) for ch in population]
    best_index = final_fitnesses.index(min(final_fitnesses))
    best_chrom = population[best_index]
    best_fit = final_fitnesses[best_index]
    workloads = compute_workload(best_chrom, tasks)
    
    # Generate assignment details and check for UNASSIGNED
    assignment_details = []
    constraint_violations = 0
    unassigned_tasks = []
    
    for task, staff_id in zip(tasks, best_chrom):
        if staff_id == UNASSIGNED:
            unassigned_tasks.append(task.task_id)
            assignment_details.append((task.task_id, UNASSIGNED, task.tariff_hours))
        else:
            staff = staff_map[staff_id]
            hours = task.tariff_hours
            assignment_details.append((task.task_id, staff_id, hours))
            
            # Check for constraint violations
            if not is_staff_eligible_for_task(staff, task):
                constraint_violations += 1
    
    # Determine success and reason
    success = len(unassigned_tasks) == 0 and constraint_violations == 0
    reason = None
    
    if not success:
        if unassigned_tasks:
            if len(unassigned_tasks) == len(tasks):
                reason = "No eligible staff found for any task"
            else:
                reason = f"No eligible staff found for {len(unassigned_tasks)} task(s): {unassigned_tasks}"
        elif constraint_violations > 0:
            reason = f"{constraint_violations} constraint violation(s) in best solution"
    
    # Convergence check
    converged = (generations_without_improvement < config.early_stopping_generations)
    
    return GAResult(
        best_chromosome=best_chrom,
        best_fitness=best_fit,
        workloads=workloads,
        generations_run=gen + 1,
        converged=converged,
        fitness_history=fitness_history,
        assignment_details=assignment_details,
        constraint_violations=constraint_violations,
        success=success,
        reason=reason
    )

