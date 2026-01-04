/**
 * Axios Instance Configuration
 * 
 * This file creates a configured axios instance for making API requests to the backend.
 * 
 * Features:
 * - Base URL: Points to backend server (http://localhost:8000)
 * - Request Interceptor: Automatically adds JWT token to all requests
 * 
 * Usage:
 *   import axios from './api/axios';
 *   const response = await axios.get('/api/staff');
 *   // Token is automatically added to the request header
 */

import axios from "axios";

// Create axios instance with base URL
// All requests using this instance will be prefixed with this URL
const instance = axios.create({
  baseURL: "http://localhost:8000",  // Backend API server URL
});

/**
 * Request Interceptor
 * 
 * Automatically adds JWT token to Authorization header for all requests.
 * This ensures authenticated requests include the token without manually
 * adding it to each API call.
 * 
 * How it works:
 * 1. Before each request, this interceptor runs
 * 2. Gets token from localStorage
 * 3. If token exists, adds "Authorization: Bearer <token>" header
 * 4. Request proceeds with authentication header
 */
instance.interceptors.request.use((config) => {
  // Get stored JWT token from localStorage
  const token = localStorage.getItem("token");
  
  // If token exists, add it to request headers
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Return modified config (request proceeds with auth header)
  return config;
});

// Export configured axios instance
// Use this instead of default axios for all API calls
export default instance;
