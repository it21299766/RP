/**
 * Staff API
 * 
 * Functions for making API calls related to staff management.
 * All functions automatically include authentication token.
 * 
 * Endpoints:
 * - GET /api/staff - Get all staff
 * - GET /api/staff/{id} - Get staff by ID
 * - POST /api/staff - Create new staff
 * - PUT /api/staff/{id} - Update staff
 * - DELETE /api/staff/{id} - Delete staff
 */

import { get, post, put, del } from '../utils/api';

/**
 * Staff API object with CRUD operations
 */
export const staffApi = {
  /**
   * Get all staff members
   * 
   * @returns {Promise<Array>} Array of staff objects
   */
  getAll: () => get('/api/staff'),
  
  /**
   * Get staff member by ID
   * 
   * @param {number} staffId - Staff ID
   * @returns {Promise<object>} Staff object
   */
  getById: (staffId) => get(`/api/staff/${staffId}`),
  
  /**
   * Create new staff member
   * 
   * @param {object} staffData - Staff data (name, designation, qualification, etc.)
   * @returns {Promise<object>} Created staff object
   */
  create: (staffData) => post('/api/staff', staffData),
  
  /**
   * Update existing staff member
   * 
   * @param {number} staffId - Staff ID to update
   * @param {object} staffData - Fields to update (partial update)
   * @returns {Promise<object>} Updated staff object
   */
  update: (staffId, staffData) => put(`/api/staff/${staffId}`, staffData),
  
  /**
   * Delete staff member
   * 
   * @param {number} staffId - Staff ID to delete
   * @returns {Promise<object|null>} Response or null
   */
  delete: (staffId) => del(`/api/staff/${staffId}`),
};

