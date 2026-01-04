import React, { useState, useEffect } from 'react';
import './TaskManagement.css';
import PopupMessage from './PopupMessage';
import { taskInstanceApi } from '../api/taskInstanceApi';
import { taskTemplateApi } from '../api/taskTemplateApi';
import { domainApi } from '../api/domainApi';
import { programApi } from '../api/programApi';

const TaskInstanceManagement = ({ userRole = 'Administrator' }) => {
  const [activeTab, setActiveTab] = useState('view-instances');
  const [instances, setInstances] = useState([]);
  const [filteredInstances, setFilteredInstances] = useState([]);
  const [editingInstance, setEditingInstance] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Dropdown data
  const [templates, setTemplates] = useState([]);
  const [domains, setDomains] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [programSections, setProgramSections] = useState([]);
  
  const isAdministrator = userRole === 'Administrator';
  
  const [formData, setFormData] = useState({
    task_template_id: '',
    domain_id: '',
    program_id: '',
    program_section_id: '',
    semester: '',
    academic_year: '',
    week_number: '',
    month: '',
    effective_hours: 0,
    status: 'draft'
  });

  // Load initial data
  useEffect(() => {
    loadInstances();
    loadTemplates();
    loadDomains();
    loadPrograms();
  }, []);

  useEffect(() => {
    setFilteredInstances(instances);
  }, [instances]);

  const loadInstances = async () => {
    setLoading(true);
    try {
      const data = await taskInstanceApi.getAll();
      setInstances(data);
      setFilteredInstances(data);
    } catch (err) {
      console.error('Error loading instances:', err);
      setPopup({
        show: true,
        message: `Error loading instances: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const loadTemplates = async () => {
    try {
      const data = await taskTemplateApi.getAll(true); // Active only
      setTemplates(data);
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const loadDomains = async () => {
    try {
      const data = await domainApi.getAll();
      setDomains(data);
    } catch (err) {
      console.error('Error loading domains:', err);
    }
  };

  const loadPrograms = async () => {
    try {
      const data = await programApi.getAll();
      setPrograms(data);
    } catch (err) {
      console.error('Error loading programs:', err);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      task_template_id: '',
      domain_id: '',
      program_id: '',
      program_section_id: '',
      semester: '',
      academic_year: '',
      week_number: '',
      month: '',
      effective_hours: 0,
      status: 'draft'
    });
    setEditingInstance(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.task_template_id || !formData.domain_id || !formData.program_id) {
      setPopup({
        show: true,
        message: 'Template, Domain, and Program are required',
        type: 'error'
      });
      return;
    }

    if (!formData.semester || !formData.academic_year) {
      setPopup({
        show: true,
        message: 'Semester and Academic Year are required',
        type: 'error'
      });
      return;
    }

    if (formData.effective_hours <= 0) {
      setPopup({
        show: true,
        message: 'Effective hours must be greater than 0',
        type: 'error'
      });
      return;
    }

    const submitData = {
      ...formData,
      task_template_id: parseInt(formData.task_template_id),
      domain_id: parseInt(formData.domain_id),
      program_id: parseInt(formData.program_id),
      program_section_id: formData.program_section_id ? parseInt(formData.program_section_id) : null,
      week_number: formData.week_number ? parseInt(formData.week_number) : null,
      month: formData.month ? parseInt(formData.month) : null,
      effective_hours: parseFloat(formData.effective_hours)
    };

    try {
      if (editingInstance) {
        await taskInstanceApi.update(editingInstance.id, submitData);
        setPopup({
          show: true,
          message: 'Task instance updated successfully!',
          type: 'success'
        });
      } else {
        await taskInstanceApi.create(submitData);
        setPopup({
          show: true,
          message: 'Task instance created successfully!',
          type: 'success'
        });
      }
      resetForm();
      loadInstances();
      setActiveTab('view-instances');
    } catch (err) {
      console.error('Error saving instance:', err);
      setPopup({
        show: true,
        message: `Error: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    }
  };

  const handleEdit = (instance) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to edit instances.',
        type: 'error'
      });
      return;
    }
    setEditingInstance(instance);
    setFormData({
      task_template_id: instance.task_template_id?.toString() || '',
      domain_id: instance.domain_id?.toString() || '',
      program_id: instance.program_id?.toString() || '',
      program_section_id: instance.program_section_id?.toString() || '',
      semester: instance.semester || '',
      academic_year: instance.academic_year || '',
      week_number: instance.week_number?.toString() || '',
      month: instance.month?.toString() || '',
      effective_hours: instance.effective_hours || 0,
      status: instance.status || 'draft'
    });
    setActiveTab('add-instance');
  };

  const handleDelete = async (instanceId) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to delete instances.',
        type: 'error'
      });
      return;
    }

    if (window.confirm('Are you sure you want to delete this instance?')) {
      try {
        await taskInstanceApi.delete(instanceId);
        setPopup({
          show: true,
          message: 'Instance deleted successfully',
          type: 'delete'
        });
        loadInstances();
      } catch (err) {
        console.error('Error deleting instance:', err);
        setPopup({
          show: true,
          message: `Error: ${err.message || 'Unknown error'}`,
          type: 'error'
        });
      }
    }
  };

  const handleApprove = async (instanceId) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to approve instances.',
        type: 'error'
      });
      return;
    }

    try {
      await taskInstanceApi.approve(instanceId);
      setPopup({
        show: true,
        message: 'Instance approved successfully',
        type: 'success'
      });
      loadInstances();
    } catch (err) {
      console.error('Error approving instance:', err);
      setPopup({
        show: true,
        message: `Error: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    }
  };

  const handleView = (instance) => {
    setSelectedInstance(instance);
    setActiveTab('instance-details');
  };

  const getTemplateName = (templateId) => {
    const template = templates.find(t => t.id === templateId);
    return template ? template.name : `Template ${templateId}`;
  };

  const getDomainName = (domainId) => {
    const domain = domains.find(d => d.domain_id === domainId);
    return domain ? domain.name : `Domain ${domainId}`;
  };

  const getProgramName = (programId) => {
    const program = programs.find(p => p.program_id === programId);
    return program ? program.name : `Program ${programId}`;
  };

  return (
    <div className="task-management">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}

      <div className="task-tabs">
        <button
          className={`tab-button ${activeTab === 'view-instances' ? 'active' : ''}`}
          onClick={() => setActiveTab('view-instances')}
        >
          View Instances
        </button>
        {isAdministrator && (
          <button
            className={`tab-button ${activeTab === 'add-instance' ? 'active' : ''}`}
            onClick={() => {
              resetForm();
              setActiveTab('add-instance');
            }}
          >
            {editingInstance ? 'Edit Instance' : 'Add Instance'}
          </button>
        )}
        <button
          className={`tab-button ${activeTab === 'instance-details' ? 'active' : ''}`}
          onClick={() => setActiveTab('instance-details')}
        >
          Instance Details
        </button>
      </div>

      {activeTab === 'view-instances' && (
        <div className="view-tasks-content">
          <h2 className="tasks-heading">Task Instances ({filteredInstances.length})</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div className="tasks-table-container">
              <table className="tasks-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Template</th>
                    <th>Domain</th>
                    <th>Program</th>
                    <th>Semester</th>
                    <th>Academic Year</th>
                    <th>Hours</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInstances.length > 0 ? (
                    filteredInstances.map(instance => (
                      <tr key={instance.id}>
                        <td>{instance.id}</td>
                        <td>{getTemplateName(instance.task_template_id)}</td>
                        <td>{getDomainName(instance.domain_id)}</td>
                        <td>{getProgramName(instance.program_id)}</td>
                        <td>{instance.semester}</td>
                        <td>{instance.academic_year}</td>
                        <td>{instance.effective_hours}h</td>
                        <td>
                          <span className={`status-${instance.status}`}>
                            {instance.status}
                          </span>
                        </td>
                        <td>
                          <button 
                            className="action-button view"
                            onClick={() => handleView(instance)}
                          >
                            View
                          </button>
                          {isAdministrator && (
                            <>
                              {instance.status === 'draft' && (
                                <button 
                                  className="action-button"
                                  onClick={() => handleApprove(instance.id)}
                                >
                                  Approve
                                </button>
                              )}
                              <button 
                                className="action-button"
                                onClick={() => handleEdit(instance)}
                              >
                                Edit
                              </button>
                              <button 
                                className="action-button delete"
                                onClick={() => handleDelete(instance.id)}
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="9" className="no-data">No instances found</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {activeTab === 'add-instance' && isAdministrator && (
        <div className="add-task-content">
          <h2 className="task-form-heading">
            {editingInstance ? 'Edit Task Instance' : 'Add New Task Instance'}
          </h2>
          <div className="form-container">
            <form className="task-form" onSubmit={handleSubmit}>
              <div className="form-columns">
                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="task_template_id">
                      Task Template <span className="required">*</span>
                    </label>
                    <select
                      id="task_template_id"
                      className="form-input"
                      value={formData.task_template_id}
                      onChange={(e) => handleInputChange('task_template_id', e.target.value)}
                      required
                    >
                      <option value="">Select Template</option>
                      {templates.map(template => (
                        <option key={template.id} value={template.id}>
                          {template.name} ({template.task_type})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="domain_id">
                      Domain <span className="required">*</span>
                    </label>
                    <select
                      id="domain_id"
                      className="form-input"
                      value={formData.domain_id}
                      onChange={(e) => handleInputChange('domain_id', e.target.value)}
                      required
                    >
                      <option value="">Select Domain</option>
                      {domains.map(domain => (
                        <option key={domain.domain_id} value={domain.domain_id}>
                          {domain.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="program_id">
                      Program <span className="required">*</span>
                    </label>
                    <select
                      id="program_id"
                      className="form-input"
                      value={formData.program_id}
                      onChange={(e) => handleInputChange('program_id', e.target.value)}
                      required
                    >
                      <option value="">Select Program</option>
                      {programs.map(program => (
                        <option key={program.program_id} value={program.program_id}>
                          {program.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="program_section_id">
                      Program Section (Optional)
                    </label>
                    <input
                      type="number"
                      id="program_section_id"
                      className="form-input"
                      value={formData.program_section_id}
                      onChange={(e) => handleInputChange('program_section_id', e.target.value)}
                      placeholder="Section ID"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="semester">
                      Semester <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="semester"
                      className="form-input"
                      value={formData.semester}
                      onChange={(e) => handleInputChange('semester', e.target.value)}
                      required
                      placeholder="e.g., 2025S1"
                    />
                  </div>
                </div>

                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="academic_year">
                      Academic Year <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="academic_year"
                      className="form-input"
                      value={formData.academic_year}
                      onChange={(e) => handleInputChange('academic_year', e.target.value)}
                      required
                      placeholder="e.g., 2024-2025"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="week_number">
                      Week Number (Optional)
                    </label>
                    <input
                      type="number"
                      id="week_number"
                      className="form-input"
                      value={formData.week_number}
                      onChange={(e) => handleInputChange('week_number', e.target.value)}
                      min="1"
                      max="52"
                      placeholder="1-52"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="month">
                      Month (Optional)
                    </label>
                    <input
                      type="number"
                      id="month"
                      className="form-input"
                      value={formData.month}
                      onChange={(e) => handleInputChange('month', e.target.value)}
                      min="1"
                      max="12"
                      placeholder="1-12"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="effective_hours">
                      Effective Hours <span className="required">*</span>
                    </label>
                    <input
                      type="number"
                      id="effective_hours"
                      className="form-input"
                      value={formData.effective_hours}
                      onChange={(e) => handleInputChange('effective_hours', parseFloat(e.target.value) || 0)}
                      required
                      min="0.1"
                      step="0.5"
                      placeholder="2.0"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="status">
                      Status <span className="required">*</span>
                    </label>
                    <select
                      id="status"
                      className="form-input"
                      value={formData.status}
                      onChange={(e) => handleInputChange('status', e.target.value)}
                      required
                    >
                      <option value="draft">Draft</option>
                      <option value="approved">Approved</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="submit-button">
                  {editingInstance ? 'Update Instance' : 'Create Instance'}
                </button>
                <button 
                  type="button" 
                  className="cancel-button"
                  onClick={() => {
                    resetForm();
                    setActiveTab('view-instances');
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'instance-details' && (
        <div className="task-details-content">
          <h2 className="task-form-heading">Instance Details</h2>
          {selectedInstance ? (
            <div className="details-grid">
              <div className="detail-card">
                <h3 className="detail-card-title">Instance #{selectedInstance.id}</h3>
                <div className="detail-card-content">
                  <div className="detail-item">
                    <span className="detail-label">Template:</span>
                    <span className="detail-value">{getTemplateName(selectedInstance.task_template_id)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Domain:</span>
                    <span className="detail-value">{getDomainName(selectedInstance.domain_id)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Program:</span>
                    <span className="detail-value">{getProgramName(selectedInstance.program_id)}</span>
                  </div>
                  {selectedInstance.program_section_id && (
                    <div className="detail-item">
                      <span className="detail-label">Program Section:</span>
                      <span className="detail-value">{selectedInstance.program_section_id}</span>
                    </div>
                  )}
                  <div className="detail-item">
                    <span className="detail-label">Semester:</span>
                    <span className="detail-value">{selectedInstance.semester}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Academic Year:</span>
                    <span className="detail-value">{selectedInstance.academic_year}</span>
                  </div>
                  {selectedInstance.week_number && (
                    <div className="detail-item">
                      <span className="detail-label">Week Number:</span>
                      <span className="detail-value">{selectedInstance.week_number}</span>
                    </div>
                  )}
                  {selectedInstance.month && (
                    <div className="detail-item">
                      <span className="detail-label">Month:</span>
                      <span className="detail-value">{selectedInstance.month}</span>
                    </div>
                  )}
                  <div className="detail-item">
                    <span className="detail-label">Effective Hours:</span>
                    <span className="detail-value">{selectedInstance.effective_hours}h</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Status:</span>
                    <span className="detail-value">
                      <span className={`status-${selectedInstance.status}`}>
                        {selectedInstance.status}
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="info-message">Select an instance to view details</p>
          )}
        </div>
      )}
    </div>
  );
};

export default TaskInstanceManagement;

