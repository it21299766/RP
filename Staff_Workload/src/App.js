import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import StaffManagement from './components/StaffManagement';
import CourseManagement from './components/CourseManagement';
import TaskManagement from './components/TaskManagement';
import WorkloadAllocation from './components/WorkloadAllocation';
import ReportsDashboard from './components/ReportsDashboard';
import Login from './components/Login';
import Swal from 'sweetalert2';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [userRole, setUserRole] = useState('Administrator');
  const [currentUserEmail, setCurrentUserEmail] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [registrationNumber, setRegistrationNumber] = useState('');

  // Load auth state from localStorage
  useEffect(() => {
    try {
      const savedIsAuth = localStorage.getItem('isAuthenticated');
      const savedRole = localStorage.getItem('userRole');
      const savedRegNo = localStorage.getItem('registrationNumber');

      if (savedIsAuth === 'true' && (savedRole === 'Administrator' || savedRole === 'Staff')) {
        setIsAuthenticated(true);
        setUserRole(savedRole);
        setRegistrationNumber(savedRegNo || '');
      }
    } catch (e) {
      // ignore
    }
  }, []);

  const handleLogin = ({ role, registrationNumber: regNo }) => {
    setIsAuthenticated(true);
    setUserRole(role);
    setRegistrationNumber(regNo || '');
    setCurrentPage('dashboard');
    try {
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('userRole', role);
      localStorage.setItem('registrationNumber', regNo || '');
    } catch (e) {
      // ignore
    }
  };

  const handleLogout = async () => {
    setIsAuthenticated(false);
    setRegistrationNumber('');
    setUserRole('Administrator');
    setCurrentUserEmail('');
    setCurrentPage('dashboard');
    try {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userRole');
      localStorage.removeItem('registrationNumber');
    } catch (e) {
      // ignore
    }

    await Swal.fire({
      icon: 'success',
      title: 'User Logged Out Success',
      showConfirmButton: false,
      timer: 1600,
      timerProgressBar: true,
    });
  };

  // Set current user email when role changes to Staff
  useEffect(() => {
    if (userRole === 'Staff') {
      try {
        const savedStaff = localStorage.getItem('staffMembers');
        if (savedStaff) {
          const parsedStaff = JSON.parse(savedStaff);
          if (parsedStaff.length > 0) {
            // Use first staff member's email as default if not set
            const firstStaffEmail = parsedStaff[0].email;
            if (currentUserEmail !== firstStaffEmail) {
              setCurrentUserEmail(firstStaffEmail);
            }
          }
        }
      } catch (error) {
        console.error('Error loading staff data:', error);
      }
    } else {
      // Clear current user email when role is Administrator
      if (currentUserEmail) {
        setCurrentUserEmail('');
      }
    }
  }, [userRole, currentUserEmail]);

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
        registrationNumber={registrationNumber}
        onLogout={handleLogout}
      />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
