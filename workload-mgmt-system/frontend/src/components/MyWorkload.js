import React, { useState, useEffect, useContext } from 'react';
import './MyWorkload.css';
import { workloadApi } from '../api/workloadApi';
import { AuthContext } from '../context/AuthContext';
import PopupMessage from './PopupMessage';

const MyWorkload = () => {
  const { user: currentUser } = useContext(AuthContext);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [filter, setFilter] = useState('all'); // 'all', 'assigned', 'completed'

  useEffect(() => {
    loadAssignments();
  }, []);

  const loadAssignments = async () => {
    setLoading(true);
    try {
      const data = await workloadApi.getMyAssignments();
      setAssignments(data);
    } catch (error) {
      console.error('Error loading assignments:', error);
      setPopup({
        show: true,
        message: `Error loading assignments: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
      setAssignments([]);
    } finally {
      setLoading(false);
    }
  };

  // Filter assignments by status
  const filteredAssignments = filter === 'all' 
    ? assignments 
    : assignments.filter(a => a.status === filter);

  // Calculate total hours
  const totalHours = filteredAssignments.reduce((sum, assignment) => sum + assignment.hours, 0);
  const assignedCount = filteredAssignments.filter(a => a.status === 'assigned').length;
  const completedCount = filteredAssignments.filter(a => a.status === 'completed').length;

  return (
    <div className="my-workload">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}

      <div className="workload-header">
        <div className="workload-header-left">
          <span className="workload-icon">👤</span>
          <h1>My Workload</h1>
          {currentUser && (
            <p className="workload-subtitle">{currentUser.name}</p>
          )}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="workload-summary">
        <div className="summary-card">
          <div className="summary-card-icon">📋</div>
          <div className="summary-card-content">
            <div className="summary-card-value">{filteredAssignments.length}</div>
            <div className="summary-card-label">Total Tasks</div>
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-card-icon">⏱️</div>
          <div className="summary-card-content">
            <div className="summary-card-value">{totalHours.toFixed(1)}h</div>
            <div className="summary-card-label">Total Hours</div>
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-card-icon">📝</div>
          <div className="summary-card-content">
            <div className="summary-card-value">{assignedCount}</div>
            <div className="summary-card-label">Assigned</div>
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-card-icon">✅</div>
          <div className="summary-card-content">
            <div className="summary-card-value">{completedCount}</div>
            <div className="summary-card-label">Completed</div>
          </div>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="workload-filters">
        <button
          className={`filter-button ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All
        </button>
        <button
          className={`filter-button ${filter === 'assigned' ? 'active' : ''}`}
          onClick={() => setFilter('assigned')}
        >
          Assigned
        </button>
        <button
          className={`filter-button ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>

      {/* Assignments Table */}
      <div className="workload-content">
        {loading ? (
          <div className="loading-message">Loading assignments...</div>
        ) : filteredAssignments.length > 0 ? (
          <div className="assignments-table-container">
            <table className="workload-table">
              <thead>
                <tr>
                  <th>Task Name</th>
                  <th>Type</th>
                  <th>Program</th>
                  <th>Section</th>
                  <th>Semester</th>
                  <th>Academic Year</th>
                  <th>Hours</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredAssignments.map((assignment) => (
                  <tr key={assignment.assignment_id}>
                    <td>{assignment.task_name || 'N/A'}</td>
                    <td>
                      <span className={`task-type-badge task-type-${assignment.task_type?.toLowerCase() || 'unknown'}`}>
                        {assignment.task_type || 'N/A'}
                      </span>
                    </td>
                    <td>{assignment.program_name || 'N/A'}</td>
                    <td>{assignment.section || 'N/A'}</td>
                    <td>{assignment.semester || 'N/A'}</td>
                    <td>{assignment.academic_year || 'N/A'}</td>
                    <td className="hours-cell">{assignment.hours}h</td>
                    <td>
                      <span className={`status-badge status-${assignment.status}`}>
                        {assignment.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <p className="empty-state-message">
              {filter === 'all' 
                ? 'No assignments found. You currently have no tasks assigned to you.'
                : `No ${filter} assignments found.`}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MyWorkload;

