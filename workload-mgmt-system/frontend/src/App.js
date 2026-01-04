/**
 * Main App Component
 * 
 * This is the root component of the application. It:
 * 1. Manages routing between different pages (dashboard, staff, courses, etc.)
 * 2. Handles authentication (shows login if not authenticated)
 * 3. Provides navigation via Sidebar component
 * 4. Maps backend roles to frontend role names
 * 
 * Page Structure:
 * - If not authenticated: Shows Login component
 * - If authenticated: Shows Sidebar + current page content
 */

import React, { useState, useEffect, useContext } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import StaffManagement from './components/StaffManagement';
import CourseManagement from './components/CourseManagement';
import TaskManagement from './components/TaskManagement';
import WorkloadAllocation from './components/WorkloadAllocation';
import ReportsDashboard from './components/ReportsDashboard';
import Login from './components/Login';
import { AuthContext } from './context/AuthContext';
import Swal from 'sweetalert2';

function App() {
  // Get authentication state and functions from AuthContext
  const { token, user, isAuthenticated, loading, login, logout } = useContext(AuthContext);
  
  // Current page state: determines which component to render
  const [currentPage, setCurrentPage] = useState('dashboard');
  
  // Current user email/identifier (used for filtering staff view)
  const [currentUserEmail, setCurrentUserEmail] = useState('');

  /**
   * Map backend role to frontend role name
   * 
   * Backend uses: ADMIN, ACADEMIC, MANAGEMENT
   * Frontend displays: Administrator, Staff
   * 
   * @returns {string} Frontend role name
   */
  const getUserRole = () => {
    if (!user) return 'Administrator';
    const roleMap = {
      'ADMIN': 'Administrator',
      'ACADEMIC': 'Staff',
      'MANAGEMENT': 'Administrator'
    };
    return roleMap[user.role] || 'Staff';
  };

  const userRole = getUserRole();

  /**
   * Handle successful login
   * Called by Login component after successful authentication
   */
  const handleLogin = () => {
    // Login is handled by Login component, just navigate to dashboard
    setCurrentPage('dashboard');
  };

  /**
   * Handle logout
   * Clears authentication state and shows success message
   */
  const handleLogout = async () => {
    // Clear authentication (removes token, user, sets isAuthenticated to false)
    logout();
    
    // Reset to dashboard page
    setCurrentPage('dashboard');
    setCurrentUserEmail('');

    // Show success notification
    await Swal.fire({
      icon: 'success',
      title: 'Logged Out Successfully',
      showConfirmButton: false,
      timer: 1600,
      timerProgressBar: true,
    });
  };

  /**
   * Effect: Set current user email when role changes
   * 
   * For Staff role, sets the current user's name/email for filtering.
   * For Administrator role, clears it (can view all staff).
   */
  useEffect(() => {
    if (userRole === 'Staff' && user) {
      // For staff, we can use their name or staff_id
      setCurrentUserEmail(user.name || '');
    } else {
      // Administrator can view all staff, no filtering needed
      setCurrentUserEmail('');
    }
  }, [userRole, user]);

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading...</p>
      </div>
    );
  }

  /**
   * Render the current page based on currentPage state
   * 
   * Routes:
   * - dashboard: Main dashboard with metrics
   * - staff-management: Staff CRUD operations
   * - course-management: Course/program/module management
   * - task-management: Task template and instance management
   * - allocations: Workload allocation and optimization
   * - reports: Reports and analytics
   * - my-workload: Personal workload view (coming soon)
   * 
   * @returns {JSX.Element} The component for the current page
   */
  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'staff-management':
        return <StaffManagement userRole={userRole} currentUserEmail={currentUserEmail} />;
      case 'course-management':
        return <CourseManagement userRole={userRole} />;
      case 'task-management':
        return <TaskManagement userRole={userRole} />;
      case 'allocations':
        return <WorkloadAllocation />;
      case 'reports':
        return <ReportsDashboard userRole={userRole} />;
      case 'my-workload':
        return <div className="page-placeholder">My Workload - Coming Soon</div>;
      default:
        return <Dashboard />;
    }
  };

  // If not authenticated, show login page
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  /**
   * Main application layout (authenticated users only)
   * 
   * Structure:
   * - Sidebar: Navigation menu on the left
   * - Main content: Current page component on the right
   */
  return (
    <div className="App">
      {/* Sidebar navigation component */}
      <Sidebar 
        onNavigate={setCurrentPage}        // Function to change pages
        currentPage={currentPage}          // Current page identifier
        userRole={userRole}                 // User's role (Administrator/Staff)
        onRoleChange={null}                 // Not used (legacy prop)
        isAuthenticated={isAuthenticated}   // Authentication status
        registrationNumber={user?.staff_id?.toString() || ''}  // User's staff ID
        onLogout={handleLogout}             // Logout handler
      />
      
      {/* Main content area: renders current page */}
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
