import React, { useState, useEffect } from 'react';
import './AdminChangeRequest.css';
import { changeRequestApi } from '../api/changeRequestApi';
import PopupMessage from './PopupMessage';

const AdminChangeRequest = () => {
  const [changeRequests, setChangeRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [filterStatus, setFilterStatus] = useState('all'); // all, PENDING, APPROVED, REJECTED
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [adminComment, setAdminComment] = useState('');
  const [actionType, setActionType] = useState(null); // 'approve' or 'reject'
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    loadChangeRequests();
  }, []);

  const loadChangeRequests = async () => {
    setLoading(true);
    try {
      const requests = await changeRequestApi.getAll();
      setChangeRequests(requests || []);
    } catch (error) {
      console.error('Error loading change requests:', error);
      setPopup({
        show: true,
        message: `Error loading change requests: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = (request) => {
    setSelectedRequest(request);
    setActionType('approve');
    setAdminComment('');
  };

  const handleReject = (request) => {
    setSelectedRequest(request);
    setActionType('reject');
    setAdminComment('');
  };

  const handleCancelAction = () => {
    setSelectedRequest(null);
    setActionType(null);
    setAdminComment('');
  };

  const handleConfirmAction = async () => {
    if (!selectedRequest || !actionType) return;

    if (actionType === 'approve' && !adminComment.trim()) {
      const confirmed = window.confirm(
        'You are about to approve this request and unassign the task. ' +
        'The assignment will be removed. Continue without a comment?'
      );
      if (!confirmed) return;
    }

    if (actionType === 'reject' && !adminComment.trim()) {
      setPopup({
        show: true,
        message: 'Please provide a reason for rejection',
        type: 'error'
      });
      return;
    }

    setProcessing(true);
    try {
      if (actionType === 'approve') {
        await changeRequestApi.approve(selectedRequest.request_id, adminComment.trim());
        setPopup({
          show: true,
          message: 'Change request approved successfully. Assignment has been removed.',
          type: 'success'
        });
      } else {
        await changeRequestApi.reject(selectedRequest.request_id, adminComment.trim());
        setPopup({
          show: true,
          message: 'Change request rejected successfully.',
          type: 'success'
        });
      }
      
      handleCancelAction();
      await loadChangeRequests();
    } catch (error) {
      console.error(`Error ${actionType}ing change request:`, error);
      setPopup({
        show: true,
        message: `Error ${actionType === 'approve' ? 'approving' : 'rejecting'} request: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setProcessing(false);
    }
  };

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

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      return dateString;
    }
  };

  const filteredRequests = filterStatus === 'all' 
    ? changeRequests 
    : changeRequests.filter(req => req.status === filterStatus);

  const pendingCount = changeRequests.filter(req => req.status === 'PENDING').length;

  return (
    <div className="admin-change-request">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}

      <div className="admin-change-request-header">
        <span className="admin-change-request-icon">📋</span>
        <h1>Change Request Management</h1>
        <p className="admin-change-request-subtitle">Review and manage staff change requests</p>
      </div>

      {loading ? (
        <div className="loading-message">Loading change requests...</div>
      ) : (
        <>
          {/* Filters */}
          <div className="filter-section">
            <div className="filter-buttons">
              <button
                className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
                onClick={() => setFilterStatus('all')}
              >
                All ({changeRequests.length})
              </button>
              <button
                className={`filter-btn ${filterStatus === 'PENDING' ? 'active' : ''}`}
                onClick={() => setFilterStatus('PENDING')}
              >
                Pending {pendingCount > 0 && <span className="badge">{pendingCount}</span>}
              </button>
              <button
                className={`filter-btn ${filterStatus === 'APPROVED' ? 'active' : ''}`}
                onClick={() => setFilterStatus('APPROVED')}
              >
                Approved
              </button>
              <button
                className={`filter-btn ${filterStatus === 'REJECTED' ? 'active' : ''}`}
                onClick={() => setFilterStatus('REJECTED')}
              >
                Rejected
              </button>
            </div>
          </div>

          {/* Action Modal */}
          {selectedRequest && actionType && (
            <div className="modal-overlay" onClick={handleCancelAction}>
              <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                  <h2>{actionType === 'approve' ? 'Approve' : 'Reject'} Change Request</h2>
                  <button className="modal-close" onClick={handleCancelAction}>×</button>
                </div>
                <div className="modal-body">
                  <div className="request-details">
                    <p><strong>Request ID:</strong> {selectedRequest.request_id}</p>
                    <p><strong>Assignment ID:</strong> {selectedRequest.assignment_id}</p>
                    <p><strong>Reason:</strong> {selectedRequest.reason}</p>
                    {actionType === 'approve' && (
                      <div className="warning-box">
                        ⚠️ <strong>Warning:</strong> Approving this request will unassign the task. 
                        The assignment will be removed from the staff member.
                      </div>
                    )}
                  </div>
                  <div className="form-group">
                    <label htmlFor="adminComment">
                      Admin Comment {actionType === 'reject' && <span className="required">*</span>}
                    </label>
                    <textarea
                      id="adminComment"
                      className="form-textarea"
                      value={adminComment}
                      onChange={(e) => setAdminComment(e.target.value)}
                      placeholder={actionType === 'approve' 
                        ? 'Optional: Add a comment explaining the approval...'
                        : 'Required: Explain why this request is being rejected...'}
                      rows="5"
                      required={actionType === 'reject'}
                    />
                  </div>
                </div>
                <div className="modal-actions">
                  <button
                    className="btn-cancel"
                    onClick={handleCancelAction}
                    disabled={processing}
                  >
                    Cancel
                  </button>
                  <button
                    className={actionType === 'approve' ? 'btn-approve' : 'btn-reject'}
                    onClick={handleConfirmAction}
                    disabled={processing}
                  >
                    {processing 
                      ? `${actionType === 'approve' ? 'Approving' : 'Rejecting'}...` 
                      : `${actionType === 'approve' ? 'Approve' : 'Reject'} Request`}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Change Requests Table */}
          <div className="requests-section">
            {filteredRequests.length > 0 ? (
              <div className="requests-table-container">
                <table className="requests-table">
                  <thead>
                    <tr>
                      <th>Request ID</th>
                      <th>Assignment ID</th>
                      <th>Staff ID</th>
                      <th>Reason</th>
                      <th>Status</th>
                      <th>Submitted Date</th>
                      <th>Admin Comment</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRequests.map((request) => (
                      <tr key={request.request_id}>
                        <td>{request.request_id}</td>
                        <td>{request.assignment_id}</td>
                        <td>{request.requested_by_staff_id}</td>
                        <td className="reason-cell">{request.reason}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(request.status)}`}>
                            {request.status}
                          </span>
                        </td>
                        <td>{formatDate(request.created_at)}</td>
                        <td className="comment-cell">{request.admin_comment || '—'}</td>
                        <td>
                          {request.status === 'PENDING' && (
                            <div className="action-buttons">
                              <button
                                className="btn-approve-small"
                                onClick={() => handleApprove(request)}
                                title="Approve and unassign task"
                              >
                                ✓ Approve
                              </button>
                              <button
                                className="btn-reject-small"
                                onClick={() => handleReject(request)}
                                title="Reject request"
                              >
                                ✗ Reject
                              </button>
                            </div>
                          )}
                          {request.status !== 'PENDING' && (
                            <span className="no-action">—</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">📋</div>
                <p className="empty-state-message">
                  {filterStatus === 'all' 
                    ? 'No change requests found.'
                    : `No ${filterStatus.toLowerCase()} change requests found.`}
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default AdminChangeRequest;

