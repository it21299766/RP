/**
 * Authentication Context
 * 
 * This context provides authentication state and functions to the entire application.
 * It manages:
 * - User login state (token, user data, authentication status)
 * - Login/logout functions
 * - Automatic token validation on app load
 * 
 * Components can access authentication via: useContext(AuthContext)
 */

import { createContext, useState, useEffect } from "react";
import { getCurrentUser } from "../api/authApi";

// Create the authentication context
// This will hold: { token, user, isAuthenticated, loading, login, logout }
export const AuthContext = createContext();

/**
 * AuthProvider Component
 * 
 * Wraps the application and provides authentication state to all child components.
 * 
 * State Management:
 * - token: JWT token stored in localStorage
 * - user: Current user object (staff information)
 * - isAuthenticated: Boolean indicating if user is logged in
 * - loading: Boolean indicating if authentication check is in progress
 * 
 * @param {ReactNode} children - Child components that will have access to auth context
 */
export const AuthProvider = ({ children }) => {
  // Initialize token from localStorage (persists across page refreshes)
  const [token, setToken] = useState(localStorage.getItem("token"));
  
  // Initialize user from localStorage (persists across page refreshes)
  // Uses lazy initialization function to parse JSON only once
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");
    return savedUser ? JSON.parse(savedUser) : null;
  });
  
  // Authentication status: true if token exists, false otherwise
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  
  // Loading state: true while checking if stored token is still valid
  const [loading, setLoading] = useState(true);

  /**
   * Effect: Validate token and load user on component mount
   * 
   * When the app loads, if a token exists in localStorage, this effect:
   * 1. Calls the API to validate the token and get current user
   * 2. If valid: Updates user state and sets authenticated to true
   * 3. If invalid: Clears token and user data (token expired or invalid)
   * 
   * This ensures that stored tokens are validated on every app load.
   */
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          // Validate token by fetching current user from API
          // If token is valid, API returns user data
          const userData = await getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (err) {
          // Token is invalid or expired - clear all auth data
          console.error("Failed to load user:", err);
          localStorage.removeItem("token");
          localStorage.removeItem("user");
          setToken(null);
          setUser(null);
          setIsAuthenticated(false);
        }
      }
      // Mark loading as complete (whether token existed or not)
      setLoading(false);
    };
    loadUser();
  }, [token]);

  /**
   * Login Function
   * 
   * Stores authentication token and user data, and updates authentication state.
   * Called after successful login API call.
   * 
   * @param {string} newToken - JWT token received from login API
   * @param {object} userData - User object (staff information) from login API
   */
  const login = (newToken, userData) => {
    // Persist token and user to localStorage (survives page refresh)
    localStorage.setItem("token", newToken);
    localStorage.setItem("user", JSON.stringify(userData));
    
    // Update state (triggers re-render of components using auth context)
    setToken(newToken);
    setUser(userData);
    setIsAuthenticated(true);
  };

  /**
   * Logout Function
   * 
   * Clears all authentication data from localStorage and state.
   * Called when user clicks logout or token expires.
   */
  const logout = () => {
    // Remove persisted data
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    
    // Clear state (triggers re-render, shows login page)
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  /**
   * Provide authentication context to all child components
   * 
   * Any component in the tree can access these values via:
   * const { token, user, isAuthenticated, login, logout } = useContext(AuthContext);
   */
  return (
    <AuthContext.Provider value={{ 
      token,        // JWT token for API requests
      user,         // Current user object (staff information)
      isAuthenticated, // Boolean: is user logged in?
      loading,      // Boolean: is auth check in progress?
      login,        // Function to log in (sets token and user)
      logout        // Function to log out (clears token and user)
    }}>
      {children}
    </AuthContext.Provider>
  );
};
