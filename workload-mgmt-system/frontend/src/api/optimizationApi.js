/**
 * Optimization API
 * 
 * Functions for making API calls related to workload optimization.
 * The optimization endpoint runs the genetic algorithm to automatically
 * assign tasks to staff members based on constraints and preferences.
 * 
 * Endpoints:
 * - POST /api/optimization/run - Run workload optimization algorithm
 */

import { post } from '../utils/api';

/**
 * Optimization API object
 */
export const optimizationApi = {
  /**
   * Run workload optimization algorithm
   * 
   * Triggers the genetic algorithm (GA) to automatically assign tasks to staff.
   * The algorithm considers:
   * - Hard constraints (qualification requirements, availability)
   * - Soft constraints (specialization match, experience, skills)
   * - Workload balance and fairness
   * 
   * @param {object} optimizationData - Optimization parameters:
   *   - semester: Semester to optimize (e.g., "2025S1")
   *   - academic_year: Academic year (e.g., "2024-2025")
   *   - options: Algorithm options (population size, generations, etc.)
   * @returns {Promise<object>} Optimization result with assignments and statistics
   * 
   * Example:
   *   const result = await optimizationApi.run({
   *     semester: "2025S1",
   *     academic_year: "2024-2025"
   *   });
   */
  run: (optimizationData) => post('/api/optimization/run', optimizationData),
};

