/**
 * Login Component
 * 
 * Displays the login form and handles user authentication.
 * 
 * Features:
 * - Username and password input fields
 * - Form validation
 * - API authentication
 * - Error handling and display
 * - Success notification
 * - Loading state during authentication
 * 
 * @param {function} onLogin - Callback function called after successful login
 */

import React, { useState, useContext } from 'react';
import './Login.css';
import Swal from 'sweetalert2';
import { login as loginApi } from '../api/authApi';
import { AuthContext } from '../context/AuthContext';

const Login = ({ onLogin }) => {
  // Get login function from authentication context
  const { login } = useContext(AuthContext);
  
  // Form state: username and password inputs
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // UI state: error message and loading indicator
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handle form submission (login attempt)
   * 
   * Process:
   * 1. Validate username and password are provided
   * 2. Call login API with credentials
   * 3. On success: Update auth context, show success message, call onLogin callback
   * 4. On error: Display error message to user
   * 
   * @param {Event} e - Form submit event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent default form submission
    setError('');        // Clear previous errors
    setLoading(true);    // Show loading state

    // Validate inputs: username and password must be provided
    if (!username.trim()) {
      setError('Please enter your username.');
      setLoading(false);
      return;
    }
    if (!password) {
      setError('Please enter your password.');
      setLoading(false);
      return;
    }

    try {
      // Call login API with username and password
      // API returns: { access_token, token_type, user }
      const response = await loginApi(username.trim(), password);
      
      // Update authentication context with token and user data
      // This sets isAuthenticated=true and makes user data available app-wide
      login(response.access_token, response.user);

      // Show success notification
      await Swal.fire({
        icon: 'success',
        title: 'Login Successful',
        text: `Welcome, ${response.user.name}!`,
        showConfirmButton: false,
        timer: 1600,
        timerProgressBar: true,
      });

      // Call onLogin callback if provided (navigates to dashboard)
      if (onLogin) {
        onLogin();
      }
    } catch (err) {
      // Handle login errors
      // Extract error message from API response or use generic message
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed. Please try again.';
      setError(errorMessage);
      
      // Show error notification
      await Swal.fire({
        icon: 'error',
        title: 'Login Failed',
        text: errorMessage,
        confirmButtonText: 'OK'
      });
    } finally {
      // Always reset loading state (whether success or error)
      setLoading(false);
    }
  };

  return (
    <div
      className="login-page"
      style={{
        backgroundImage: `linear-gradient(135deg, rgba(15, 23, 42, 0.35), rgba(30, 41, 59, 0.35)), url("${encodeURI(
          `${process.env.PUBLIC_URL}/images/SLIIT login.jpg`
        )}")`,
      }}
    >
      <div className="login-card">
        <div className="login-header">
          <div className="login-title">Staff Workload System</div>
          <div className="login-subtitle">Sign in to continue</div>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username (e.g., sf1, adm1)"
              autoComplete="username"
              disabled={loading}
            />
          </div>

          <div className="login-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          {error ? <div className="login-error">{error}</div> : null}

          <button 
            className="login-button" 
            type="submit"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;


