import React, { useState, useEffect } from 'react';
import './WorkloadAllocation.css';
import PopupMessage from './PopupMessage';
import { optimizationApi } from '../api/optimizationApi';
import { staffApi } from '../api/staffApi';

const WorkloadAllocation = ({ userRole = 'Administrator' }) => {
  const isAdministrator = userRole === 'Administrator';
  const isStaff = userRole === 'Staff';
  const [activeTab, setActiveTab] = useState(isStaff ? 'allocation-results' : 'run-allocation');
  const [formData, setFormData] = useState({
    semester: '',
    department: '',
    allow_admin_override: false
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [departments, setDepartments] = useState([]);

  // Load departments from staff
  useEffect(() => {
    const loadDepartments = async () => {
      try {
        const staff = await staffApi.getAll();
        const deptSet = new Set();
        staff.forEach(s => {
          if (s.department) deptSet.add(s.department);
        });
        const deptArray = Array.from(deptSet).sort();
        setDepartments(deptArray);
        if (deptArray.length > 0 && !formData.department) {
          setFormData(prev => ({ ...prev, department: deptArray[0] }));
        }
      } catch (err) {
        console.error('Error loading departments:', err);
        setDepartments(['Computer Science', 'Mathematics', 'Physics']);
      }
    };
    loadDepartments();
  }, []);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleRunAllocation = async (e) => {
    e.preventDefault();
    
    if (!formData.semester || !formData.department) {
      setPopup({
        show: true,
        message: 'Please select both semester and department',
        type: 'error'
      });
      return;
    }

    setLoading(true);
    try {
      const response = await optimizationApi.run({
        semester: formData.semester,
        department: formData.department,
        allow_admin_override: formData.allow_admin_override
      });
      setResults(response);
      setActiveTab('allocation-results');
      setPopup({
        show: true,
        message: 'Allocation completed successfully!',
        type: 'success'
      });
    } catch (err) {
      console.error('Error running allocation:', err);
      setPopup({
        show: true,
        message: `Error: ${err.message || 'Failed to run allocation'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workload-allocation">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}
      
      <div className="allocation-header">
        <div className="allocation-header-left">
          <h1 className="allocation-title">{isStaff ? 'My Workload' : 'Workload Allocation'}</h1>
        </div>
      </div>

      <div className="allocation-tabs">
        {isAdministrator && (
          <button
            className={`allocation-tab-button ${activeTab === 'run-allocation' ? 'active' : ''}`}
            onClick={() => setActiveTab('run-allocation')}
          >
            Run Allocation
          </button>
        )}
        <button
          className={`allocation-tab-button ${activeTab === 'allocation-results' ? 'active' : ''}`}
          onClick={() => setActiveTab('allocation-results')}
        >
          Allocation Results
        </button>
      </div>

      {activeTab === 'run-allocation' && isAdministrator && (
        <div className="run-allocation-content">
          <div className="configure-allocation-section">
            <h2 className="section-title">Configure Allocation</h2>
            
            <form className="allocation-form" onSubmit={handleRunAllocation}>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="semester">
                    Semester <span className="required">*</span>
                  </label>
                  <input
                    type="text"
                    id="semester"
                    className="form-select"
                    value={formData.semester}
                    onChange={(e) => handleInputChange('semester', e.target.value)}
                    required
                    placeholder="e.g., 2025S1"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="department">
                    Department <span className="required">*</span>
                  </label>
                  <select
                    id="department"
                    className="form-select"
                    value={formData.department}
                    onChange={(e) => handleInputChange('department', e.target.value)}
                    required
                  >
                    <option value="">Select Department</option>
                    {departments.map(dept => (
                      <option key={dept} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="allow_admin_override">
                  <input
                    type="checkbox"
                    id="allow_admin_override"
                    checked={formData.allow_admin_override}
                    onChange={(e) => handleInputChange('allow_admin_override', e.target.checked)}
                  />
                  <span style={{ marginLeft: '8px' }}>Allow Admin Override</span>
                </label>
              </div>

              <div className="form-actions">
                <button 
                  type="submit" 
                  className="run-allocation-button"
                  disabled={loading}
                >
                  {loading ? 'Running...' : 'Run Allocation'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'allocation-results' && (
        <div className="allocation-results-content">
          <h2 className="section-title">Allocation Results</h2>
          {results ? (
            <div>
              <div className="results-summary">
                <h3>Summary</h3>
                <div className="summary-grid">
                  <div className="summary-item">
                    <span className="summary-label">Status:</span>
                    <span className="summary-value">{results.status}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Total Tasks:</span>
                    <span className="summary-value">{results.summary.total_tasks}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Total Staff:</span>
                    <span className="summary-value">{results.summary.total_staff}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Average Load:</span>
                    <span className="summary-value">{results.summary.avg_load.toFixed(2)}h</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Overloaded Staff:</span>
                    <span className="summary-value">{results.summary.overloaded_staff}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Underloaded Staff:</span>
                    <span className="summary-value">{results.summary.underloaded_staff}</span>
                  </div>
                </div>
              </div>

              {results.warnings && results.warnings.length > 0 && (
                <div className="warnings-section">
                  <h3>Warnings</h3>
                  <ul>
                    {results.warnings.map((warning, idx) => (
                      <li key={idx}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="assignments-section">
                <h3>Assignments ({results.assignments.length})</h3>
                <div className="assignments-table-container">
                  <table className="assignments-table">
                    <thead>
                      <tr>
                        <th>Task Instance ID</th>
                        <th>Staff ID</th>
                        <th>Hours</th>
                      </tr>
                    </thead>
                    <tbody>
                      {results.assignments.map((assignment, idx) => (
                        <tr key={idx}>
                          <td>{assignment.task_instance_id}</td>
                          <td>{assignment.staff_id}</td>
                          <td>{assignment.hours}h</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ) : (
            <div className="results-placeholder">
              <p className="info-message">
                Run an allocation to see results here.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default WorkloadAllocation;

