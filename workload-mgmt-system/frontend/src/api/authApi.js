/**
 * Authentication API
 * 
 * Functions for authentication-related API calls:
 * - Login: Authenticate user and receive JWT token
 * - Get Current User: Validate token and get user information
 * - Logout: Clear local authentication data (client-side only)
 */

import axios from "./axios";

/**
 * Login Function
 * 
 * Sends username and password to backend, receives JWT token and user data.
 * 
 * @param {string} username - User's username (e.g., "sf1", "adm1")
 * @param {string} password - User's password
 * @returns {Promise<object>} Response data containing:
 *   - access_token: JWT token for authenticated requests
 *   - user: User object (staff information)
 * 
 * @throws {Error} If credentials are invalid (401 Unauthorized)
 * 
 * Example:
 *   const { access_token, user } = await login("sf1", "sf1");
 */
export const login = async (username, password) => {
  // POST request to login endpoint
  // Backend validates credentials and returns token + user data
  const res = await axios.post("/api/auth/login", {
    username: username,
    password: password
  });
  return res.data;
};

/**
 * Get Current User
 * 
 * Validates the stored JWT token and retrieves current user information.
 * Used to check if token is still valid and get updated user data.
 * 
 * @returns {Promise<object>} User object (staff information)
 * 
 * @throws {Error} If token is invalid or expired (401 Unauthorized)
 * 
 * Note: Token is automatically added by axios interceptor
 * 
 * Example:
 *   const user = await getCurrentUser();
 *   // Returns: { staff_id: 1, name: "Dr. John Smith", role: "ACADEMIC", ... }
 */
export const getCurrentUser = async () => {
  // GET request to /api/auth/me
  // Backend validates token from Authorization header and returns user data
  const res = await axios.get("/api/auth/me");
  return res.data;
};

/**
 * Logout Function (Client-side only)
 * 
 * Clears authentication data from localStorage.
 * Note: This is client-side only. Backend doesn't need to be notified
 * because JWT tokens are stateless (no server-side session to invalidate).
 * 
 * To fully logout:
 * 1. Clear localStorage (this function)
 * 2. Clear React state (handled by AuthContext.logout())
 * 
 * Example:
 *   logout();
 *   // Token and user data removed from localStorage
 */
export const logout = () => {
  // Remove stored authentication data
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};