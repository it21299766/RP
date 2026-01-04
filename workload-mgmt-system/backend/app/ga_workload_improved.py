"""
Improved Genetic Algorithm for Workload Assignment (WAM System)

WHAT THIS FILE DOES:
This file implements a Genetic Algorithm (GA) to automatically assign teaching tasks to staff members.
Think of it as an "intelligent assignment system" that tries many different ways to assign tasks
and finds the best one by evolving better and better solutions over time.

HOW IT WORKS (Simple Explanation):
1. Start with 50 random ways to assign tasks (initial population)
2. For each assignment, calculate how "good" it is (fitness function)
3. Keep the best assignments and use them to create new ones (selection + crossover)
4. Add some randomness to explore new possibilities (mutation)
5. Repeat for 100 generations, getting better each time
6. Return the best assignment found

Features:
  - Hard constraint enforcement (qualification levels) - PhD can teach MSc tasks, but BSc cannot
  - Configurable fitness weights - adjust what matters most (balance vs. skill matching)
  - Seed support for reproducibility - same input = same output (for testing)
  - Early stopping and convergence monitoring - stops early if no improvement
  - Robust edge-case handling - handles empty lists, single tasks, etc.
  - Type hints and comprehensive docstrings - makes code easier to understand
"""

import random  # For generating random numbers (initial population, mutations, etc.)
import statistics  # For calculating standard deviation (workload balance)
from dataclasses import dataclass, field  # For creating data structures (Staff, Task, etc.)
from typing import List, Dict, Tuple, Optional  # For type hints (makes code clearer)
from enum import Enum  # For creating qualification levels


# -------------------------------------------
# Enums and Constants
# -------------------------------------------

# Qualification hierarchy: PhD > MSc > BSc
# This enum defines the levels, but we use QUAL_RANK dictionary for quick lookups
class QualificationLevel(Enum):
    BSC = 1  # Bachelor's degree (lowest level)
    MSC = 2  # Master's degree (middle level)
    PHD = 3  # Doctorate (highest level)

# Dictionary to quickly check if someone's qualification is high enough
# Example: If task requires MSc (2), someone with PhD (3) can do it (3 >= 2) ✅
#          But someone with BSc (1) cannot (1 < 2) ❌
QUAL_RANK = {"BSc": 1, "MSc": 2, "PhD": 3}


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
    generations: int = 100  # How many times to evolve (100 = run for 100 generations)
    pop_size: int = 50  # How many solutions in each generation (50 = try 50 different assignments)
    crossover_rate: float = 0.8  # Probability of combining parents (0.8 = 80% chance)
    mutation_rate: float = 0.05  # Probability of random changes (0.05 = 5% chance per gene)
    tournament_k: int = 3  # How many solutions compete in tournament selection (3 = pick best of 3)
    elitism_count: int = 2  # How many best solutions to always keep (2 = always keep top 2)
    seed: Optional[int] = None  # Random seed for reproducibility (None = different each time)
    enforce_hard_constraints: bool = True  # Whether to only assign eligible staff (True = yes)
    early_stopping_generations: int = 20  # Stop early if no improvement (20 = stop if no improvement for 20 generations)
    
    # Fitness weights - These control how much different things matter
    stdev_weight: float = 1.0  # How much to penalize unbalanced workloads (higher = more balance important)
    overload_multiplier: float = 5.0  # How much to penalize overloading (squared penalty)
    hard_penalty: float = 100.0  # How much to penalize qualification mismatches (very high - this is a "must not happen")
    soft_penalty: float = 1.0  # How much to penalize specialty/skill mismatches (small - this is a "nice to have")
    match_bonus_specialty: float = 3.0  # Reward for matching specialty (higher = more important)
    match_bonus_skill: float = 2.0  # Reward per matching skill (higher = more important)
    match_bonus_experience: float = 1.0  # Reward for having enough experience (higher = more important)
    
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
    """Represents a staff member with qualifications and capacity."""
    staff_id: int
    max_hours: float
    qualification: str  # "BSc", "MSc", "PhD"
    specialty: str
    skills: List[str] = field(default_factory=list)
    experience: int = 0
    available: bool = True
    
    def __post_init__(self):
        """Validate staff data."""
        if self.qualification not in QUAL_RANK:
            raise ValueError(f"Invalid qualification: {self.qualification}")
        if self.max_hours <= 0:
            raise ValueError("max_hours must be > 0")
        if self.experience < 0:
            raise ValueError("experience must be >= 0")
    
    def meets_requirement(self, required_qual: str) -> bool:
        """Check if staff meets minimum qualification requirement."""
        return QUAL_RANK[self.qualification] >= QUAL_RANK[required_qual]


@dataclass
class Task:
    """
    Represents a workload task with requirements.
    
    This is like a "job description" for a task - what qualifications, skills,
    and experience are needed, and how many hours it takes.
    """
    task_id: int  # Unique identifier (101, 102, etc.)
    tariff_hours: float  # How many hours this task takes (2.0, 4.0, etc.)
    required_qualification: str  # Minimum qualification needed ("BSc", "MSc", "PhD") - HARD CONSTRAINT
    required_specialty: str  # Preferred specialty ("Computer Science", etc.) - SOFT CONSTRAINT
    required_skills: List[str] = field(default_factory=list)  # Skills needed (["Python", "SQL"]) - SOFT CONSTRAINT
    required_experience: int = 0  # Minimum years of experience needed (3, 5, etc.) - SOFT CONSTRAINT
    
    def __post_init__(self):
        """Validate task data."""
        if self.required_qualification not in QUAL_RANK:
            raise ValueError(f"Invalid qualification: {self.required_qualification}")
        if self.tariff_hours <= 0:
            raise ValueError("tariff_hours must be > 0")
        if self.required_experience < 0:
            raise ValueError("required_experience must be >= 0")


@dataclass
class GAResult:
    """Result of GA optimization run."""
    best_chromosome: List[int]
    best_fitness: float
    workloads: Dict[int, float]
    generations_run: int
    converged: bool
    fitness_history: List[float] = field(default_factory=list)
    assignment_details: List[Tuple[int, int, float]] = field(default_factory=list)
    constraint_violations: int = 0
    

# -------------------------------------------
# GA Helper Functions
# -------------------------------------------
def get_eligible_staff(task: Task, staff_map: Dict[int, Staff]) -> List[int]:
    """
    Get list of staff IDs eligible for a task based on hard constraints.
    
    WHAT THIS DOES: Finds all staff who CAN do a task (hard constraint: qualification must match).
    
    STEP-BY-STEP:
    1. Loop through all staff
    2. Skip if staff is not available
    3. Check if staff's qualification is high enough
    4. If yes, add their ID to the eligible list
    
    EXAMPLE:
    - Task requires: MSc
    - Staff 1: PhD ✅ (can do it - 3 >= 2)
    - Staff 2: MSc ✅ (can do it - 2 >= 2)
    - Staff 3: BSc ❌ (cannot do it - 1 < 2)
    - Returns: [1, 2]
    """
    eligible = []
    for staff_id, staff in staff_map.items():
        # Skip unavailable staff
        if not staff.available:
            continue
        # Check if qualification is high enough (HARD CONSTRAINT)
        if staff.meets_requirement(task.required_qualification):
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
    Each solution is a chromosome - a list showing which staff does which task.
    
    EXAMPLE OUTPUT:
    [
        [1, 2, 1, 3, 2],  # Solution 1: Task 1→Staff1, Task 2→Staff2, Task 3→Staff1, etc.
        [2, 1, 3, 1, 2],  # Solution 2: Different random assignment
        [1, 3, 2, 2, 1],  # Solution 3: Another random assignment
        # ... 47 more solutions
    ]
    
    Args:
        tasks: List of tasks to assign
        staff_list: List of available staff
        pop_size: Population size (how many random solutions to create)
        allow_overload: If False, try to stay within max_hours (soft constraint)
        enforce_hard_constraints: If True, only assign eligible staff (respects qualifications)
    
    Returns:
        Population of chromosomes (list of solutions, each solution is a list of staff IDs)
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
                    # Fallback: assign to random staff (will be penalized)
                    pick = random.choice(staff_ids)
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
    
    EXAMPLE:
    - Chromosome: [1, 2, 1, 3, 2]  (which staff does which task)
    - Tasks: [Task(2hrs), Task(3hrs), Task(4hrs), Task(2hrs), Task(3hrs)]
    - Result: {1: 6.0, 2: 6.0, 3: 2.0}
      - Staff 1: 2 + 4 = 6 hours
      - Staff 2: 3 + 3 = 6 hours
      - Staff 3: 2 hours
    
    Args:
        chromosome: List of staff IDs (one per task)
        tasks: List of tasks with their hours
    
    Returns:
        Dictionary mapping staff_id → total_hours
    """


def compute_fitness(
    chromosome: List[int],
    tasks: List[Task],
    staff_map: Dict[int, Staff],
    config: GAConfig
) -> float:
    """
    Compute fitness score (lower is better).
    
    WHAT THIS DOES: This is the "judge" that evaluates how good a solution is.
    It calculates a number - lower numbers mean better solutions.
    
    THE FITNESS FUNCTION HAS 5 COMPONENTS:
      1. Workload balance (std dev penalty) - Penalizes unbalanced workloads
      2. Overload penalty (squared hours over max) - Heavily penalizes overloading
      3. Hard constraint violations (qualification mismatch) - Huge penalty for wrong qualifications
      4. Soft constraint penalties (specialty, skills, experience) - Small penalties for mismatches
      5. Soft bonuses (matches) - Rewards for matching specialty, skills, experience
    
    HOW IT WORKS:
    - Good things (matches) SUBTRACT from fitness (make it lower = better)
    - Bad things (violations, overloads) ADD to fitness (make it higher = worse)
    
    EXAMPLE:
    - Perfect solution: Fitness = -10.5 (very good!)
    - Bad solution: Fitness = 450.2 (very bad - has violations)
    
    Args:
        chromosome: The solution to evaluate (list of staff IDs)
        tasks: List of tasks
        staff_map: Dictionary mapping staff_id → Staff object
        config: GA configuration (weights, penalties, etc.)
    
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
    # 3. Qualification, Specialty, Skills, Experience
    # --------------------------
    match_bonus = 0.0
    hard_penalty = 0.0
    soft_penalty = 0.0
    
    for gene, task in zip(chromosome, tasks):
        staff = staff_map[gene]
        
        # Hard qualification mismatch (scaled by task hours)
        if not staff.meets_requirement(task.required_qualification):
            hard_penalty += config.hard_penalty * task.tariff_hours
        
        # Specialty match
        if staff.specialty == task.required_specialty:
            match_bonus += config.match_bonus_specialty * task.tariff_hours
        else:
            soft_penalty += config.soft_penalty * task.tariff_hours
        
        # Skill match
        skill_matches = len(set(staff.skills) & set(task.required_skills))
        match_bonus += skill_matches * config.match_bonus_skill * task.tariff_hours
        if skill_matches == 0 and task.required_skills:
            soft_penalty += config.soft_penalty * task.tariff_hours
        
        # Experience match
        if staff.experience >= task.required_experience:
            match_bonus += config.match_bonus_experience * task.tariff_hours
        else:
            gap = task.required_experience - staff.experience
            soft_penalty += gap * config.soft_penalty * task.tariff_hours
    
    # Final fitness (lower is better)
    fitness_score = stdev_penalty + overload_penalty + hard_penalty + soft_penalty - match_bonus
    return fitness_score


def tournament_select(
    population: List[List[int]],
    fitnesses: List[float],
    k: int = 3
) -> List[int]:
    """
    Select a chromosome via tournament selection.
    
    WHAT THIS DOES: Picks a chromosome (solution) for reproduction using tournament selection.
    Think of it like a mini-competition - randomly pick k solutions, the best one wins.
    
    STEP-BY-STEP:
    1. Randomly pick k chromosomes (default: 3)
    2. Compare their fitness scores
    3. Return the one with LOWEST fitness (best solution)
    
    EXAMPLE:
    - Population: [Solution1, Solution2, Solution3, Solution4, Solution5]
    - Fitnesses: [15.2, 45.8, 8.3, 22.1, 18.5]
    - Randomly pick 3: Solution1 (15.2), Solution3 (8.3), Solution5 (18.5)
    - Best: Solution3 (8.3) ✅
    - Return: Solution3
    
    WHY TOURNAMENT SELECTION?
    - Gives good solutions a better chance, but not guaranteed
    - Allows some "underdogs" to win occasionally (maintains diversity)
    - Prevents one super-good solution from dominating
    
    Args:
        population: Current population (all solutions)
        fitnesses: Fitness scores for each solution (lower is better)
        k: Tournament size (how many to compete)
    
    Returns:
        Selected chromosome (the winner of the tournament)
    """
    # Make sure k doesn't exceed population size
    k = min(k, len(population))
    # Pair each chromosome with its fitness score
    items = list(zip(population, fitnesses))
    # Randomly select k items for the tournament
    selected = random.sample(items, k)
    # Sort by fitness (lower is better), so best is first
    selected.sort(key=lambda x: x[1])
    # Return the winner (first one after sorting)
    return selected[0][0]


def crossover(
    p1: List[int],
    p2: List[int],
    rate: float = 0.8
) -> Tuple[List[int], List[int]]:
    """
    Single-point crossover with safe handling of edge cases.
    
    WHAT THIS DOES: Combines two parent chromosomes to create two children.
    This is like mixing two good recipes to create a better one.
    
    STEP-BY-STEP:
    1. Check if crossover should happen (80% chance)
    2. Pick a random crossover point
    3. Child 1: First part from parent 1, second part from parent 2
    4. Child 2: First part from parent 2, second part from parent 1
    
    EXAMPLE:
    - Parent 1: [1, 2, 1, 3, 2]
    - Parent 2: [2, 1, 3, 1, 2]
    - Crossover point: 2
    - Child 1: [1, 2 | 3, 1, 2]  (positions 0-1 from P1, 2-4 from P2)
    - Child 2: [2, 1 | 1, 3, 2]  (positions 0-1 from P2, 2-4 from P1)
    
    WHY CROSSOVER?
    - Combines good traits from both parents
    - Like mixing two good solutions to create a better one
    - Explores new combinations that might be better than either parent
    
    Args:
        p1: Parent 1 chromosome (first parent solution)
        p2: Parent 2 chromosome (second parent solution)
        rate: Crossover probability (0.8 = 80% chance to crossover)
    
    Returns:
        Tuple of (child1, child2) - two new solutions created from parents
    """
    # If chromosome too short or random chance says no crossover, return parents unchanged
    if len(p1) < 2 or random.random() > rate:
        return p1[:], p2[:]
    
    # Pick a random point to split (between 1 and len-1)
    point = random.randint(1, len(p1) - 1)
    # Create child 1: first part from p1, second part from p2
    child1 = p1[:point] + p2[point:]
    # Create child 2: first part from p2, second part from p1
    child2 = p2[:point] + p1[point:]
    return child1, child2


def mutate(
    chromosome: List[int],
    staff_ids: List[int],
    rate: float = 0.05
) -> List[int]:
    """
    Random mutation: randomly replace genes with probability `rate`.
    
    WHAT THIS DOES: Randomly changes some genes (assignments) to add variety.
    This prevents the algorithm from getting stuck and explores new possibilities.
    
    STEP-BY-STEP:
    1. Loop through each gene (position) in chromosome
    2. 5% chance to mutate each gene
    3. If mutating, replace with random staff ID
    
    EXAMPLE:
    - Before: [1, 2, 1, 3, 2]
    - Mutation at position 2 (5% chance happened)
    - After: [1, 2, 2, 3, 2]  (gene 2 changed from 1 to 2)
    
    WHY MUTATION?
    - Prevents getting stuck in local optima (bad solutions that look good)
    - Adds new solutions that might be better
    - Like trying a random ingredient in a recipe - sometimes it works!
    - Too much mutation = chaos, too little = stuck
    
    Args:
        chromosome: Chromosome to mutate (the solution to modify)
        staff_ids: Available staff IDs to mutate to (list of possible staff)
        rate: Mutation rate (0.05 = 5% chance per gene)
    
    Returns:
        Mutated chromosome (may or may not be changed, depending on random chance)
    """
    # Loop through each position in the chromosome
    for i in range(len(chromosome)):
        # 5% chance to mutate this gene
        if random.random() < rate:
            # Replace with random staff ID
            chromosome[i] = random.choice(staff_ids)
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
    Run genetic algorithm for workload assignment.
    
    WHAT THIS DOES: This is the MAIN FUNCTION that runs the entire genetic algorithm.
    It evolves solutions over many generations to find the best way to assign tasks.
    
    THE BIG PICTURE:
    1. Create initial population (50 random solutions)
    2. For each generation (100 times):
       a. Evaluate fitness of all solutions
       b. Keep best solutions (elitism)
       c. Select parents (tournament selection)
       d. Create children (crossover)
       e. Mutate children
       f. Replace population with new generation
    3. Return the best solution found
    
    Args:
        staff_list: List of staff members (who can be assigned tasks)
        tasks: List of tasks to assign (what needs to be done)
        config: GA configuration (settings - uses default if None)
    
    Returns:
        GAResult object containing:
        - best_chromosome: The best assignment found
        - best_fitness: How good it is (lower = better)
        - workloads: How many hours each staff has
        - generations_run: How many generations it ran
        - converged: Whether it converged (stopped early)
        - fitness_history: How fitness improved over time
        - assignment_details: List of (task_id, staff_id, hours)
        - constraint_violations: How many hard constraints were violated
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
    num_tasks = len(tasks)
    
    # Validate staff availability
    available_staff = [s for s in staff_list if s.available]
    if not available_staff:
        raise ValueError("No available staff for assignment")
    
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
            
            mutate(c1, staff_ids, rate=config.mutation_rate)
            new_pop.append(c1)
            
            if len(new_pop) < config.pop_size:
                mutate(c2, staff_ids, rate=config.mutation_rate)
                new_pop.append(c2)
        
        population = new_pop[:config.pop_size]
    
    # Evaluate best
    final_fitnesses = [compute_fitness(ch, tasks, staff_map, config) for ch in population]
    best_index = final_fitnesses.index(min(final_fitnesses))
    best_chrom = population[best_index]
    best_fit = final_fitnesses[best_index]
    workloads = compute_workload(best_chrom, tasks)
    
    # Generate assignment details
    assignment_details = []
    constraint_violations = 0
    for task, staff_id in zip(tasks, best_chrom):
        staff = staff_map[staff_id]
        hours = task.tariff_hours
        assignment_details.append((task.task_id, staff_id, hours))
        if not staff.meets_requirement(task.required_qualification):
            constraint_violations += 1
    
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
        constraint_violations=constraint_violations
    )


# -------------------------------------------
# Main (Demo)
# -------------------------------------------
if __name__ == "__main__":
    
    # --------------------------
    # SAMPLE INPUT
    # --------------------------
    # staff_list = [
    #     Staff(1, 12, "PhD", "AI", ["Python", "ML"], 5),
    #     Staff(2, 10, "MSc", "SE", ["Java", "OOP"], 3),
    #     Staff(3, 8, "BSc", "Networks", ["Networking"], 2)
    # ]
    
#     tasks = [
#         Task(101, 3, "MSc", "AI", ["Python"], 1),
#         Task(102, 2, "BSc", "SE", ["Java"], 0),
#         Task(103, 4, "PhD", "AI", ["Python", "ML"], 3),
#         Task(104, 1, "BSc", "Networks", ["Networking"], 1)
#     ]
#     staff_list = [
#     Staff(
#         staff_id=1,
#         max_hours=10,
#         qualification="MSc",
#         specialty="Physics",
#         skills=["Quantum", "Mechanics"],
#         experience=5
#     ),
#     Staff(
#         staff_id=2,
#         max_hours=10,
#         qualification="MSc",
#         specialty="Computer Science",
#         skills=["Python", "Algorithms"],
#         experience=3
#     )
# ]
    staff_list = [
    Staff(
        staff_id=1,
        max_hours=12,
        qualification="PhD",
        specialty="Physics",
        skills=["Quantum"],
        experience=10
    )
]
    tasks = [
    Task(
        task_id=202,
        tariff_hours=3,
        required_qualification="MSc",
        required_specialty="Computer Science",
        required_skills=["Python"],
        required_experience=2
    )
]

    # --------------------------
    # RUN THE GA with custom config
    # --------------------------
    config = GAConfig(
        generations=100,
        pop_size=50,
        seed=42,
        enforce_hard_constraints=True,
        early_stopping_generations=20
    )
    
    result = run_ga(staff_list, tasks, config)
    
    # --------------------------
    # OUTPUT
    # --------------------------
    print("\n===== GA RESULTS (IMPROVED) =====\n")
    
    print("Assignments (task → staff → hours):")
    for task_id, staff_id, hours in result.assignment_details:
        staff = next(s for s in staff_list if s.staff_id == staff_id)
        print(f"  Task {task_id} → Staff {staff_id} ({staff.qualification}, {staff.specialty}) : {hours} hrs")
    
    print("\nWorkload per staff:")
    for sid, load in sorted(result.workloads.items()):
        staff = next(s for s in staff_list if s.staff_id == sid)
        capacity_pct = (load / staff.max_hours) * 100
        print(f"  Staff {sid}: {load:.1f} / {staff.max_hours} hours ({capacity_pct:.1f}%)")
    
    print(f"\nFitness Score: {result.best_fitness:.2f}")
    print(f"Generations Run: {result.generations_run}")
    print(f"Converged: {result.converged}")
    print(f"Hard Constraint Violations: {result.constraint_violations}")
    
    print("\n===================================\n")
