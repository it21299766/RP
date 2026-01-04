import React, { useState, useEffect, useContext } from 'react';
import './ChangeRequest.css';
import { changeRequestApi } from '../api/changeRequestApi';
import { workloadApi } from '../api/workloadApi';
import { AuthContext } from '../context/AuthContext';
import PopupMessage from './PopupMessage';

const ChangeRequest = () => {
  const { user: currentUser } = useContext(AuthContext);
  const [assignments, setAssignments] = useState([]);
  const [changeRequests, setChangeRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [reason, setReason] = useState('');
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // Load assignments and change requests in parallel
      const [assignmentsData, requestsData] = await Promise.all([
        workloadApi.getMyAssignments(),
        changeRequestApi.getAll()
      ]);
      setAssignments(assignmentsData);
      setChangeRequests(requestsData || []);
    } catch (error) {
      console.error('Error loading data:', error);
      setPopup({
        show: true,
        message: `Error loading data: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitRequest = async (e) => {
    e.preventDefault();
    
    if (!selectedAssignment || !reason.trim()) {
      setPopup({
        show: true,
        message: 'Please select an assignment and provide a reason',
        type: 'error'
      });
      return;
    }

    setSubmitting(true);
    try {
      // Find the assignment_id from the selected assignment
      // Note: We need assignment_id, but workloadApi returns task_instance_id
      // We need to find the assignment by task_instance_id
      // For now, we'll need to get assignments from a different endpoint
      // Let's use the assignments API
      const assignmentId = selectedAssignment.assignment_id;
      
      await changeRequestApi.create({
        assignment_id: assignmentId,
        requested_by_staff_id: currentUser.staff_id,
        reason: reason.trim()
      });
      
      setPopup({
        show: true,
        message: 'Change request submitted successfully!',
        type: 'success'
      });
      
      // Reset form
      setSelectedAssignment(null);
      setReason('');
      setShowForm(false);
      
      // Reload data
      await loadData();
    } catch (error) {
      console.error('Error submitting change request:', error);
      setPopup({
        show: true,
        message: `Error submitting request: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setSubmitting(false);
    }
  };

  // Get assignments with change request status
  const getAssignmentWithRequest = (assignment) => {
    const request = changeRequests.find(
      req => req.assignment_id === assignment.assignment_id && req.status === 'PENDING'
    );
    return { ...assignment, hasPendingRequest: !!request, request: request || null };
  };

  const assignmentsWithStatus = assignments.map(getAssignmentWithRequest);

  // Filter assignments - only show assigned tasks
  const assignedTasks = assignmentsWithStatus.filter(a => a.status === 'assigned');

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'PENDING':
        return 'status-pending';
      case 'APPROVED':
        return 'status-approved';
      case 'REJECTED':
        return 'status-rejected';
      default:
        return 'status-unknown';
    }
  };

  return (
    <div className="change-request">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}

      <div className="change-request-header">
        <span className="change-request-icon">📝</span>
        <h1>Change Request</h1>
        <p className="change-request-subtitle">Request changes to your assigned tasks</p>
      </div>

      {loading ? (
        <div className="loading-message">Loading assignments...</div>
      ) : (
        <>
          {/* Request Form */}
          {showForm && (
            <div className="request-form-container">
              <h2>Submit Change Request</h2>
              <form onSubmit={handleSubmitRequest} className="request-form">
                <div className="form-group">
                  <label htmlFor="assignment">Select Assignment *</label>
                  <select
                    id="assignment"
                    className="form-select"
                    value={selectedAssignment?.assignment_id || ''}
                    onChange={(e) => {
                      const assignmentId = parseInt(e.target.value);
                      const assignment = assignedTasks.find(a => a.assignment_id === assignmentId);
                      setSelectedAssignment(assignment || null);
                    }}
                    required
                  >
                    <option value="">-- Select an assignment --</option>
                    {assignedTasks
                      .filter(a => !a.hasPendingRequest)
                      .map(assignment => (
                        <option key={assignment.assignment_id} value={assignment.assignment_id}>
                          {assignment.task_name} - {assignment.program_name} {assignment.section || ''} ({assignment.hours}h)
                        </option>
                      ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="reason">Reason for Change Request *</label>
                  <textarea
                    id="reason"
                    className="form-textarea"
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    placeholder="Please explain why you need this change (e.g., schedule conflict, workload issue, preference, etc.)"
                    rows="5"
                    required
                  />
                </div>

                <div className="form-actions">
                  <button
                    type="submit"
                    className="btn-submit"
                    disabled={submitting}
                  >
                    {submitting ? 'Submitting...' : 'Submit Request'}
                  </button>
                  <button
                    type="button"
                    className="btn-cancel"
                    onClick={() => {
                      setShowForm(false);
                      setSelectedAssignment(null);
                      setReason('');
                    }}
                    disabled={submitting}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Request List Button */}
          {!showForm && (
            <div className="action-bar">
              <button
                className="btn-primary"
                onClick={() => setShowForm(true)}
                disabled={assignedTasks.filter(a => !a.hasPendingRequest).length === 0}
              >
                + New Change Request
              </button>
            </div>
          )}

          {/* My Change Requests */}
          <div className="requests-section">
            <h2>My Change Requests</h2>
            {changeRequests.length > 0 ? (
              <div className="requests-table-container">
                <table className="requests-table">
                  <thead>
                    <tr>
                      <th>Task</th>
                      <th>Program</th>
                      <th>Hours</th>
                      <th>Reason</th>
                      <th>Status</th>
                      <th>Admin Comment</th>
                      <th>Submitted Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {changeRequests.map((request) => {
                      const assignment = assignments.find(a => a.assignment_id === request.assignment_id);
                      return (
                        <tr key={request.request_id}>
                          <td>{assignment?.task_name || 'N/A'}</td>
                          <td>{assignment?.program_name || 'N/A'} {assignment?.section || ''}</td>
                          <td>{assignment?.hours || 'N/A'}h</td>
                          <td className="reason-cell">{request.reason}</td>
                          <td>
                            <span className={`status-badge ${getStatusBadgeClass(request.status)}`}>
                              {request.status}
                            </span>
                          </td>
                          <td className="comment-cell">{request.admin_comment || '—'}</td>
                          <td>—</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">📋</div>
                <p className="empty-state-message">No change requests submitted yet.</p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default ChangeRequest;

