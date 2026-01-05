/**
 * Login Component
 * 
 * This component handles user authentication for the Staff Workload System.
 * Users log in using their registration number and password.
 * 
 * Features:
 * - Registration number validation (must start with "Ad" for Admin or "St" for Staff)
 * - Password input (currently accepts any password for demo purposes)
 * - Role derivation from registration number prefix
 * - Success notifications using SweetAlert2
 * - Background image with transparent card overlay
 * - Real-time role detection as user types registration number
 * 
 * Props:
 * - onLogin: Function called on successful login, receives { role, registrationNumber }
 * 
 * Role Derivation:
 * - Registration numbers starting with "Ad" (case-insensitive) → Administrator role
 * - Registration numbers starting with "St" (case-insensitive) → Staff role
 * - Other prefixes → Invalid (shows error message)
 * 
 * Dependencies:
 * - SweetAlert2: For styled success pop-up messages
 * - Background image: Located at /public/images/SLIIT login.jpg
 */
import React, { useMemo, useState } from 'react';
import './Login.css';
import Swal from 'sweetalert2';

/**
 * Utility: normalizeRegNo
 * Trims whitespace from registration number input
 * @param {string} value - Raw registration number input
 * @returns {string} - Normalized registration number
 */
const normalizeRegNo = (value) => (value || '').trim();

/**
 * Utility: getRoleFromRegNo
 * Derives user role from registration number prefix
 * @param {string} regNo - Registration number
 * @returns {string|null} - 'Administrator', 'Staff', or null if invalid
 */
const getRoleFromRegNo = (regNo) => {
  const v = normalizeRegNo(regNo);
  if (v.toLowerCase().startsWith('ad')) return 'Administrator';
  if (v.toLowerCase().startsWith('st')) return 'Staff';
  return null;
};

/**
 * Utility: getSuccessMessage
 * Returns appropriate success message based on user role
 * @param {string} role - User role ('Administrator' or 'Staff')
 * @returns {string} - Success message text
 */
const getSuccessMessage = (role) => {
  if (role === 'Administrator') return 'Admin successfully logged';
  if (role === 'Staff') return 'Staff successfully logged';
  return 'Successfully logged';
};

const Login = ({ onLogin }) => {
  /**
   * State: registrationNumber
   * Stores the user's registration number input
   */
  const [registrationNumber, setRegistrationNumber] = useState('');

  /**
   * State: password
   * Stores the user's password input
   * Note: Currently accepts any password (no validation for demo purposes)
   */
  const [password, setPassword] = useState('');

  /**
   * State: error
   * Stores error messages to display to the user
   */
  const [error, setError] = useState('');

  /**
   * Derived State: derivedRole
   * Automatically determines role from registration number as user types
   * Uses useMemo to avoid recalculating on every render
   */
  const derivedRole = useMemo(() => getRoleFromRegNo(registrationNumber), [registrationNumber]);

  /**
   * Handler: handleSubmit
   * Processes login form submission
   * Validates inputs, derives role, shows success message, and calls onLogin callback
   * @param {Event} e - Form submit event
   */
  const handleSubmit = async (e) => {
    // Prevent default form submission behavior (page refresh)
    e.preventDefault();
    // Clear any previous error messages
    setError('');

    // Normalize registration number (trim whitespace)
    const regNo = normalizeRegNo(registrationNumber);
    // Validate that registration number is not empty
    if (!regNo) {
      // Set error message for empty registration number
      setError('Please enter your registration number.');
      // Exit function early if validation fails
      return;
    }
    // Validate that password is not empty
    if (!password) {
      // Set error message for empty password
      setError('Please enter your password.');
      // Exit function early if validation fails
      return;
    }

    // Validate registration number format and derive role from prefix
    const role = getRoleFromRegNo(regNo);
    // Check if role was successfully derived (valid prefix)
    if (!role) {
      // Set error message for invalid registration number format
      setError('Registration number must start with "Ad" (Admin) or "St" (Staff).');
      // Exit function early if validation fails
      return;
    }

    /**
     * Show Success Notification
     * Uses SweetAlert2 to display a styled success pop-up with:
     * - Green check icon
     * - Role-specific success message
     * - Auto-dismiss after 1.6 seconds
     * - Progress bar for visual feedback
     */
    // Wait for SweetAlert2 popup to display and auto-dismiss
    await Swal.fire({
      icon: 'success', // Green checkmark icon
      title: getSuccessMessage(role), // Role-specific success message
      showConfirmButton: false, // Hide OK button (auto-dismiss)
      timer: 1600, // Auto-dismiss after 1.6 seconds
      timerProgressBar: true, // Show progress bar during countdown
    });
    // After popup dismisses, call onLogin callback if provided
    if (onLogin) {
      // Pass role and normalized registration number to parent component
      onLogin({ role, registrationNumber: regNo });
    }
  };

  /**
   * Render: Login Page
   * Displays a centered login card with:
   * - Background image (SLIIT login.jpg) with reduced opacity overlay
   * - Transparent card with backdrop blur effect
   * - Registration number input with real-time role detection
   * - Password input
   * - Error message display
   * - Login button
   */
  return (
    <div
      className="login-page"
      style={{
        /**
         * Background Image Styling
         * Uses inline style to properly resolve image path from public folder
         * Includes gradient overlay to reduce opacity while maintaining image visibility
         */
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
            <label htmlFor="regNo">Registration Number</label>
            <input
              id="regNo"
              type="text"
              value={registrationNumber}
              onChange={(e) => setRegistrationNumber(e.target.value)}
              placeholder='e.g. "Ad12345" or "St12345"'
              autoComplete="username"
            />
            {/* Role Detection Hint */}
            {/* Displays detected role in real-time as user types registration number */}
            {derivedRole && (
              <div className="login-hint">
                Detected role: <strong>{derivedRole}</strong>
              </div>
            )}
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
            />
          </div>

          {error ? <div className="login-error">{error}</div> : null}

          <button className="login-button" type="submit">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;


