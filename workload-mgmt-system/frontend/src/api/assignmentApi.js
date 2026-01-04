/**
 * Assignment API
 * 
 * Functions for making API calls related to task assignments.
 * Assignments link staff members to task instances (who teaches what).
 * 
 * Endpoints:
 * - GET /api/assignments - Get all assignments
 * - GET /api/assignments/{id} - Get assignment by ID
 * - POST /api/assignments - Create new assignment
 * - PUT /api/assignments/{id} - Update assignment
 * - DELETE /api/assignments/{id} - Delete assignment
 */

import { get, post, put, del } from '../utils/api';

/**
 * Assignment API object with CRUD operations
 */
export const assignmentApi = {
  /**
   * Get all task assignments
   * 
   * @returns {Promise<Array>} Array of assignment objects
   */
  getAll: () => get('/api/assignments'),
  
  /**
   * Get assignment by ID
   * 
   * @param {number} assignmentId - Assignment ID
   * @returns {Promise<object>} Assignment object
   */
  getById: (assignmentId) => get(`/api/assignments/${assignmentId}`),
  
  /**
   * Create new assignment (assign staff to task instance)
   * 
   * @param {object} assignmentData - Assignment data (staff_id, task_instance_id, etc.)
   * @returns {Promise<object>} Created assignment object
   */
  create: (assignmentData) => post('/api/assignments', assignmentData),
  
  /**
   * Update existing assignment
   * 
   * @param {number} assignmentId - Assignment ID to update
   * @param {object} assignmentData - Fields to update
   * @returns {Promise<object>} Updated assignment object
   */
  update: (assignmentId, assignmentData) => put(`/api/assignments/${assignmentId}`, assignmentData),
  
  /**
   * Delete assignment (unassign staff from task)
   * 
   * @param {number} assignmentId - Assignment ID to delete
   * @returns {Promise<object|null>} Response or null
   */
  delete: (assignmentId) => del(`/api/assignments/${assignmentId}`),
};

