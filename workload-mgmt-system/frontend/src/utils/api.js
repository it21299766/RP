/**
 * API Utility Functions
 * 
 * This file provides helper functions for making HTTP requests to the backend API.
 * It handles:
 * - Adding authentication tokens to requests
 * - Error handling and response parsing
 * - Standard HTTP methods (GET, POST, PUT, DELETE)
 * 
 * All functions automatically include JWT token from localStorage in request headers.
 */

// Base URL for API requests
// Can be overridden via REACT_APP_API_BASE environment variable
const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

/**
 * Get authentication headers with JWT token
 * 
 * Creates headers object with Content-Type and Authorization (if token exists).
 * Used by all API request functions to include authentication.
 * 
 * @returns {object} Headers object with Content-Type and optional Authorization
 */
function getAuthHeaders() {
  // Get stored JWT token from localStorage
  const token = localStorage.getItem('token');
  
  // Base headers (always include Content-Type)
  const headers = {
    'Content-Type': 'application/json',
  };
  
  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

/**
 * Handle HTTP response
 * 
 * Processes API responses, handles errors, and parses JSON.
 * 
 * Error Handling:
 * - If response is not OK (status >= 400), extracts error message
 * - Tries to get error message from JSON response (FastAPI format)
 * - Falls back to response text or status text if JSON parsing fails
 * - Throws error with status code attached
 * 
 * Success Handling:
 * - Returns null for 204 No Content responses
 * - Returns parsed JSON for other successful responses
 * 
 * @param {Response} res - Fetch API Response object
 * @returns {Promise<object|null>} Parsed JSON data or null for 204 responses
 * @throws {Error} If response is not OK, throws error with message and status
 */
async function handleResponse(res) {
  // Check if response indicates an error (status >= 400)
  if (!res.ok) {
    let errorMessage = res.statusText;
    
    try {
      // Try to extract error message from JSON response (FastAPI format)
      const errorData = await res.json();
      // FastAPI uses 'detail' field for error messages
      errorMessage = errorData.detail || errorData.message || res.statusText;
    } catch (e) {
      // If response is not JSON, try to get text
      const text = await res.text();
      errorMessage = text || res.statusText;
    }
    
    // Create error with message and status code
    const error = new Error(errorMessage);
    error.status = res.status;
    throw error;
  }
  
  // 204 No Content: Return null (no body to parse)
  if (res.status === 204) return null;
  
  // Parse and return JSON response
  return res.json();
}

/**
 * GET Request
 * 
 * Makes a GET request to the API endpoint.
 * 
 * @param {string} path - API endpoint path (e.g., '/api/staff')
 * @returns {Promise<object>} Parsed JSON response
 * 
 * Example:
 *   const staff = await get('/api/staff');
 */
export async function get(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: getAuthHeaders(),  // Includes Authorization token
  });
  return handleResponse(res);
}

/**
 * POST Request
 * 
 * Makes a POST request to create a new resource.
 * 
 * @param {string} path - API endpoint path (e.g., '/api/staff')
 * @param {object} body - Request body object (will be JSON stringified)
 * @returns {Promise<object>} Parsed JSON response
 * 
 * Example:
 *   const newStaff = await post('/api/staff', { name: 'John', ... });
 */
export async function post(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: getAuthHeaders(),  // Includes Authorization token
    body: JSON.stringify(body),  // Convert object to JSON string
  });
  return handleResponse(res);
}

/**
 * PUT Request
 * 
 * Makes a PUT request to update an existing resource.
 * 
 * @param {string} path - API endpoint path (e.g., '/api/staff/1')
 * @param {object} body - Request body object with fields to update
 * @returns {Promise<object>} Parsed JSON response
 * 
 * Example:
 *   const updated = await put('/api/staff/1', { designation: 'Professor' });
 */
export async function put(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'PUT',
    headers: getAuthHeaders(),  // Includes Authorization token
    body: JSON.stringify(body),  // Convert object to JSON string
  });
  return handleResponse(res);
}

/**
 * DELETE Request
 * 
 * Makes a DELETE request to remove a resource.
 * 
 * @param {string} path - API endpoint path (e.g., '/api/staff/1')
 * @returns {Promise<object|null>} Parsed JSON response or null for 204
 * 
 * Example:
 *   await del('/api/staff/1');
 */
export async function del(path) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),  // Includes Authorization token
  });
  return handleResponse(res);
}

// Export all functions as default object for convenience
export default { get, post, put, del };
