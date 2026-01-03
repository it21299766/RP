/**
 * Sidebar Component
 * 
 * This component provides the main navigation sidebar for the application.
 * It displays navigation links, role information, and user authentication status.
 * 
 * Features:
 * - Navigation links to different pages (Dashboard, Staff Management, etc.)
 * - Role selector (only shown when not authenticated)
 * - User info display (role and registration number when authenticated)
 * - Logout functionality
 * - Radio button navigation for quick access
 * 
 * Props:
 * - onNavigate: Function to handle navigation to different pages
 * - currentPage: String indicating the currently active page
 * - userRole: String indicating user role ('Administrator' or 'Staff')
 * - onRoleChange: Function to handle role changes (deprecated, now managed by login)
 * - isAuthenticated: Boolean indicating if user is logged in
 * - registrationNumber: String containing user's registration number
 * - onLogout: Function to handle logout action
 * 
 * Navigation Items:
 * - Dashboard: Main system overview
 * - Staff Management: Manage staff members
 * - Course Management: Manage courses
 * - Task Management: Manage tasks
 * - Allocations: Workload allocation
 * - Reports: View system reports
 */
// Import React and useState hook (though useState is not used in this component)
import React, { useState } from 'react';
// Import CSS styles for sidebar component
import './Sidebar.css';

// Component function that receives props via destructuring
const Sidebar = ({ onNavigate, currentPage, userRole, onRoleChange, isAuthenticated, registrationNumber, onLogout }) => {
  /**
   * Determine the currently selected navigation item
   * Defaults to 'dashboard' if no currentPage is provided
   */
  // Use currentPage prop or default to 'dashboard' if undefined/null
  const selectedNav = currentPage || 'dashboard';

  /**
   * Navigation Items Array
   * Defines all available navigation links with their icons and labels.
   * These are displayed as clickable links in the main navigation section.
   */
  // Array of navigation items with id, label, and emoji icon
  const navItems = [
    { id: 'allocations', label: 'Allocations', icon: '📄' }, // Document icon for allocations
    { id: 'course-management', label: 'Course Management', icon: '📚' }, // Books icon for courses
    { id: 'task-management', label: 'Task Management', icon: '✅' }, // Checkmark icon for tasks
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' }, // House icon for dashboard
    { id: 'my-workload', label: 'My Workload', icon: '👤' }, // Person icon for personal workload
    { id: 'reports', label: 'Reports', icon: '📊' }, // Chart icon for reports
    { id: 'staff-management', label: 'Staff Management', icon: '👥' } // People icon for staff
  ];

  /**
   * Radio Navigation Items Array
   * Defines navigation items displayed as radio buttons for quick access.
   * These provide an alternative navigation method with visual selection state.
   */
  // Array of navigation items for radio button navigation (subset of navItems)
  const radioNavItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' }, // House icon
    { id: 'staff-management', label: 'Staff Management', icon: '👥' }, // People icon
    { id: 'course-management', label: 'Course Management', icon: '📚' }, // Books icon
    { id: 'task-management', label: 'Task Management', icon: '✅' }, // Checkmark icon
    { id: 'allocations', label: 'Allocations', icon: '📄' }, // Document icon
    { id: 'reports', label: 'Reports', icon: '📊' } // Chart icon
  ];

  // Return JSX structure for sidebar
  return (
    // Main sidebar container div
    <div className="sidebar">
      {/* Content wrapper for sidebar sections */}
      <div className="sidebar-content">
        {/* Navigation links section */}
        <div className="sidebar-section">
          {/* Container for navigation links */}
          <div className="nav-links">
            {/* Section label text */}
            <div className="nav-section-label">main</div>
            {/* Map over navItems array to render each navigation link */}
            {navItems.map(item => (
              // Anchor tag for each navigation link
              <a
                key={item.id} // Unique key for React list rendering
                href="#" // Hash link to prevent page navigation
                className={`nav-link ${selectedNav === item.id ? 'active' : ''}`} // Add 'active' class if this item is selected
                onClick={(e) => {
                  // Prevent default anchor tag behavior (page navigation)
                  e.preventDefault();
                  // Call onNavigate callback if provided
                  if (onNavigate) {
                    // Navigate to the selected page using item id
                    onNavigate(item.id);
                  }
                }}
              >
                {/* Display the label text for this navigation item */}
                {item.label}
              </a>
            ))}
          </div>
        </div>

        {/* Workload Management header section */}
        <div className="sidebar-section">
          {/* Header container with icon and title */}
          <div className="workload-management-header">
            {/* Chart emoji icon */}
            <span className="workload-icon">📊</span>
            {/* Section heading */}
            <h2>Workload Management</h2>
          </div>
        </div>

        {/* Role/Authentication Section */}
        {/* 
          Conditionally renders based on authentication status:
          - If authenticated: Shows user info (role, registration number) and logout button
          - If not authenticated: Shows role selector dropdown
        */}
        <div className="sidebar-section">
          {/* Conditional rendering: check if user is authenticated */}
          {isAuthenticated ? (
            // Authenticated user view: show user info and logout button
            <div className="role-selector">
              {/* Label text */}
              <label>Logged in</label>
              {/* Badge container showing user information */}
              <div className="role-badge">
                {/* First line: display user role */}
                <div className="role-badge-line">
                  {/* Label text */}
                  <span className="role-badge-label">Role:</span> {/* Display role or default to 'Administrator' */}
                  {userRole || 'Administrator'}
                </div>
                {/* Second line: display registration number */}
                <div className="role-badge-line">
                  {/* Label text */}
                  <span className="role-badge-label">Reg No:</span> {/* Display registration number or dash if empty */}
                  {registrationNumber || '—'}
                </div>
              </div>
              {/* Logout button */}
              <button
                type="button" // Button type (not submit)
                className="logout-button" // CSS class for styling
                onClick={() => {
                  // Call onLogout callback if provided
                  if (onLogout) onLogout();
                }}
              >
                {/* Button text */}
                Logout
              </button>
            </div>
          ) : (
            /**
             * Role Selector (Deprecated)
             * This role selector is only shown when user is not authenticated.
             * Note: In the current implementation, role is determined by login,
             * so this selector may not be used. It's kept for backward compatibility.
             */
            // Unauthenticated user view: show role selector dropdown
            <div className="role-selector">
              {/* Label for dropdown */}
              <label htmlFor="role-select">Select Role</label>
              {/* Dropdown select element */}
              <select
                id="role-select" // ID for label association
                className="role-dropdown" // CSS class for styling
                value={userRole || 'Administrator'} // Current selected value or default
                onChange={(e) => {
                  // Call onRoleChange callback if provided
                  if (onRoleChange) {
                    // Pass selected value to callback
                    onRoleChange(e.target.value);
                  }
                }}
              >
                {/* Administrator option */}
                <option value="Administrator">Administrator</option>
                {/* Staff option */}
                <option value="Staff">Staff</option>
              </select>
            </div>
          )}
        </div>

        {/* Radio Navigation Section */}
        {/* Provides quick navigation using radio button style selection */}
        <div className="sidebar-section">
          {/* Container for radio navigation items */}
          <div className="radio-nav">
            {/* Map over radioNavItems array to render each radio button */}
            {radioNavItems.map(item => (
              // Label element wrapping radio input and text
              <label
                key={item.id} // Unique key for React list rendering
                className={`radio-nav-item ${selectedNav === item.id ? 'selected' : ''}`} // Add 'selected' class if this item is selected
              >
                {/* Radio input element */}
                <input
                  type="radio" // Radio button input type
                  name="nav-radio" // Group name (all radios in same group)
                  value={item.id} // Value for this radio option
                  checked={selectedNav === item.id} // Checked if this item matches selectedNav
                  onChange={() => {
                    // Call onNavigate callback if provided
                    if (onNavigate) {
                      // Navigate to the selected page using item id
                      onNavigate(item.id);
                    }
                  }}
                />
                {/* Icon span displaying emoji */}
                <span className="radio-icon">{item.icon}</span>
                {/* Label text span */}
                <span className="radio-label">{item.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Export component as default for use in other files
export default Sidebar;

