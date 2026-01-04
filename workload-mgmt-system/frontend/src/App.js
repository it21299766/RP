import React, { useState, useEffect, useContext } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import StaffManagement from './components/StaffManagement';
import CourseManagement from './components/CourseManagement';
import TaskManagement from './components/TaskManagement';
import WorkloadAllocation from './components/WorkloadAllocation';
import ReportsDashboard from './components/ReportsDashboard';
import MyWorkload from './components/MyWorkload';
import MyProfile from './components/MyProfile';
import ChangeRequest from './components/ChangeRequest';
import Login from './components/Login';
import { AuthContext } from './context/AuthContext';
import Swal from 'sweetalert2';

function App() {
  const { token, user, isAuthenticated, loading, login, logout } = useContext(AuthContext);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [currentUserEmail, setCurrentUserEmail] = useState('');

  // Map backend role to frontend role
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

  const handleLogin = () => {
    // Login is handled by Login component, just navigate to dashboard
    setCurrentPage('dashboard');
  };

  const handleLogout = async () => {
    logout();
    setCurrentPage('dashboard');
    setCurrentUserEmail('');

    await Swal.fire({
      icon: 'success',
      title: 'Logged Out Successfully',
      showConfirmButton: false,
      timer: 1600,
      timerProgressBar: true,
    });
  };

  // Set current user email when role changes to Staff
  useEffect(() => {
    if (userRole === 'Staff' && user) {
      // For staff, we can use their name or staff_id
      setCurrentUserEmail(user.name || '');
    } else {
      setCurrentUserEmail('');
    }
  }, [userRole, user]);

  // Show loading state
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Loading...</p>
      </div>
    );
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard userRole={userRole} />;
      case 'staff-management':
        return <StaffManagement userRole={userRole} currentUserEmail={currentUserEmail} />;
      case 'course-management':
        return <CourseManagement userRole={userRole} />;
      case 'task-management':
        return <TaskManagement userRole={userRole} />;
      case 'allocations':
        return <WorkloadAllocation userRole={userRole} />;
      case 'reports':
        return <ReportsDashboard userRole={userRole} />;
      case 'my-workload':
        return <MyWorkload />;
      case 'my-profile':
        return <MyProfile />;
      case 'view-staff':
        return <StaffManagement userRole={userRole} currentUserEmail={currentUserEmail} />;
      case 'change-request':
        return <ChangeRequest />;
      default:
        return <Dashboard />;
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <Sidebar 
        onNavigate={setCurrentPage} 
        currentPage={currentPage}
        userRole={userRole}
        onRoleChange={null}
        isAuthenticated={isAuthenticated}
        registrationNumber={user?.staff_id?.toString() || ''}
        onLogout={handleLogout}
      />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
