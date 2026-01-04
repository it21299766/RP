import React, { useState } from 'react';
import './Sidebar.css';

const Sidebar = ({ onNavigate, currentPage, userRole, onRoleChange, isAuthenticated, registrationNumber, onLogout }) => {
  const selectedNav = currentPage || 'dashboard';

  const navItems = [
    { id: 'allocations', label: 'Allocations', icon: '📄' },
    { id: 'course-management', label: 'Course Management', icon: '📚' },
    { id: 'task-management', label: 'Task Management', icon: '✅' },
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
    { id: 'my-workload', label: 'My Workload', icon: '👤' },
    { id: 'reports', label: 'Reports', icon: '📊' },
    { id: 'staff-management', label: 'Staff Management', icon: '👥' }
  ];

  const radioNavItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
    { id: 'staff-management', label: 'Staff Management', icon: '👥' },
    { id: 'course-management', label: 'Course Management', icon: '📚' },
    { id: 'task-management', label: 'Task Management', icon: '✅' },
    { id: 'allocations', label: 'Allocations', icon: '📄' },
    { id: 'reports', label: 'Reports', icon: '📊' }
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-content">
        <div className="sidebar-section">
          <div className="nav-links">
            <div className="nav-section-label">main</div>
            {navItems.map(item => (
              <a
                key={item.id}
                href="#"
                className={`nav-link ${selectedNav === item.id ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  if (onNavigate) {
                    onNavigate(item.id);
                  }
                }}
              >
                {item.label}
              </a>
            ))}
          </div>
        </div>

        <div className="sidebar-section">
          <div className="workload-management-header">
            <span className="workload-icon">📊</span>
            <h2>Workload Management</h2>
          </div>
        </div>

        <div className="sidebar-section">
          {isAuthenticated ? (
            <div className="role-selector">
              <label>Logged in</label>
              <div className="role-badge">
                <div className="role-badge-line">
                  <span className="role-badge-label">Role:</span> {userRole || 'Administrator'}
                </div>
                <div className="role-badge-line">
                  <span className="role-badge-label">Reg No:</span> {registrationNumber || '—'}
                </div>
              </div>
              <button
                type="button"
                className="logout-button"
                onClick={() => {
                  if (onLogout) onLogout();
                }}
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="role-selector">
              <label htmlFor="role-select">Select Role</label>
              <select
                id="role-select"
                className="role-dropdown"
                value={userRole || 'Administrator'}
                onChange={(e) => {
                  if (onRoleChange) {
                    onRoleChange(e.target.value);
                  }
                }}
              >
                <option value="Administrator">Administrator</option>
                <option value="Staff">Staff</option>
              </select>
            </div>
          )}
        </div>

        <div className="sidebar-section">
          <div className="radio-nav">
            {radioNavItems.map(item => (
              <label
                key={item.id}
                className={`radio-nav-item ${selectedNav === item.id ? 'selected' : ''}`}
              >
                <input
                  type="radio"
                  name="nav-radio"
                  value={item.id}
                  checked={selectedNav === item.id}
                  onChange={() => {
                    if (onNavigate) {
                      onNavigate(item.id);
                    }
                  }}
                />
                <span className="radio-icon">{item.icon}</span>
                <span className="radio-label">{item.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;

