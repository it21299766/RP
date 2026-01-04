import React, { useState, useEffect } from 'react';
import './TaskManagement.css';
import PopupMessage from './PopupMessage';
import { taskTemplateApi } from '../api/taskTemplateApi';

const TaskTemplateManagement = ({ userRole = 'Administrator' }) => {
  const [activeTab, setActiveTab] = useState('view-templates');
  const [templates, setTemplates] = useState([]);
  const [filteredTemplates, setFilteredTemplates] = useState([]);
  const [editingTemplate, setEditingTemplate] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const isAdministrator = userRole === 'Administrator';
  
  const [formData, setFormData] = useState({
    name: '',
    task_type: 'lecture',
    default_hours: 0,
    required_qualification_level: 'MSc',
    required_specialization: '',
    required_skills: [],
    required_experience_years: 0,
    is_active: true
  });

  const [skillsInput, setSkillsInput] = useState('');

  // Load templates from backend
  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setLoading(true);
    try {
      const data = await taskTemplateApi.getAll(false);
      setTemplates(data);
      setFilteredTemplates(data);
    } catch (err) {
      console.error('Error loading templates:', err);
      setPopup({
        show: true,
        message: `Error loading templates: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setFilteredTemplates(templates);
  }, [templates]);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSkillsInputChange = (value) => {
    setSkillsInput(value);
    const skillsArray = value.split(',').map(s => s.trim()).filter(s => s.length > 0);
    setFormData(prev => ({
      ...prev,
      required_skills: skillsArray
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      task_type: 'lecture',
      default_hours: 0,
      required_qualification_level: 'MSc',
      required_specialization: '',
      required_skills: [],
      required_experience_years: 0,
      is_active: true
    });
    setSkillsInput('');
    setEditingTemplate(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      setPopup({
        show: true,
        message: 'Name is required',
        type: 'error'
      });
      return;
    }

    if (formData.default_hours <= 0) {
      setPopup({
        show: true,
        message: 'Default hours must be greater than 0',
        type: 'error'
      });
      return;
    }

    try {
      if (editingTemplate) {
        await taskTemplateApi.update(editingTemplate.id, formData);
        setPopup({
          show: true,
          message: 'Task template updated successfully!',
          type: 'success'
        });
      } else {
        await taskTemplateApi.create(formData);
        setPopup({
          show: true,
          message: 'Task template created successfully!',
          type: 'success'
        });
      }
      resetForm();
      loadTemplates();
      setActiveTab('view-templates');
    } catch (err) {
      console.error('Error saving template:', err);
      setPopup({
        show: true,
        message: `Error: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    }
  };

  const handleEdit = (template) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to edit templates.',
        type: 'error'
      });
      return;
    }
    setEditingTemplate(template);
    setFormData({
      name: template.name || '',
      task_type: template.task_type || 'lecture',
      default_hours: template.default_hours || 0,
      required_qualification_level: template.required_qualification_level || 'MSc',
      required_specialization: template.required_specialization || '',
      required_skills: Array.isArray(template.required_skills) ? template.required_skills : [],
      required_experience_years: template.required_experience_years || 0,
      is_active: template.is_active !== undefined ? template.is_active : true
    });
    setSkillsInput(Array.isArray(template.required_skills) ? template.required_skills.join(', ') : '');
    setActiveTab('add-template');
  };

  const handleDelete = async (templateId) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to delete templates.',
        type: 'error'
      });
      return;
    }

    if (window.confirm('Are you sure you want to delete this template?')) {
      try {
        await taskTemplateApi.delete(templateId);
        setPopup({
          show: true,
          message: 'Template deleted successfully',
          type: 'delete'
        });
        loadTemplates();
      } catch (err) {
        console.error('Error deleting template:', err);
        setPopup({
          show: true,
          message: `Error: ${err.message || 'Unknown error'}`,
          type: 'error'
        });
      }
    }
  };

  const handleView = (template) => {
    setSelectedTemplate(template);
    setActiveTab('template-details');
  };

  const taskTypes = ['lecture', 'lab', 'tutorial', 'exam', 'admin', 'research'];

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
          className={`tab-button ${activeTab === 'view-templates' ? 'active' : ''}`}
          onClick={() => setActiveTab('view-templates')}
        >
          View Templates
        </button>
        {isAdministrator && (
          <button
            className={`tab-button ${activeTab === 'add-template' ? 'active' : ''}`}
            onClick={() => {
              resetForm();
              setActiveTab('add-template');
            }}
          >
            {editingTemplate ? 'Edit Template' : 'Add Template'}
          </button>
        )}
        <button
          className={`tab-button ${activeTab === 'template-details' ? 'active' : ''}`}
          onClick={() => setActiveTab('template-details')}
        >
          Template Details
        </button>
      </div>

      {activeTab === 'view-templates' && (
        <div className="view-tasks-content">
          <h2 className="tasks-heading">Task Templates ({filteredTemplates.length})</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div className="tasks-table-container">
              <table className="tasks-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Default Hours</th>
                    <th>Qualification</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTemplates.length > 0 ? (
                    filteredTemplates.map(template => (
                      <tr key={template.id}>
                        <td>{template.id}</td>
                        <td>{template.name}</td>
                        <td>
                          <span className="category-badge">
                            {template.task_type}
                          </span>
                        </td>
                        <td>{template.default_hours}h</td>
                        <td>{template.required_qualification_level}</td>
                        <td>
                          <span className={template.is_active ? 'status-active' : 'status-inactive'}>
                            {template.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td>
                          <button 
                            className="action-button view"
                            onClick={() => handleView(template)}
                          >
                            View
                          </button>
                          {isAdministrator && (
                            <>
                              <button 
                                className="action-button"
                                onClick={() => handleEdit(template)}
                              >
                                Edit
                              </button>
                              <button 
                                className="action-button delete"
                                onClick={() => handleDelete(template.id)}
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
                      <td colSpan="7" className="no-data">No templates found</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {activeTab === 'add-template' && isAdministrator && (
        <div className="add-task-content">
          <h2 className="task-form-heading">
            {editingTemplate ? 'Edit Task Template' : 'Add New Task Template'}
          </h2>
          <div className="form-container">
            <form className="task-form" onSubmit={handleSubmit}>
              <div className="form-columns">
                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="name">
                      Template Name <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="name"
                      className="form-input"
                      value={formData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      required
                      placeholder="e.g., CS101 Lecture"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="task_type">
                      Task Type <span className="required">*</span>
                    </label>
                    <select
                      id="task_type"
                      className="form-input"
                      value={formData.task_type}
                      onChange={(e) => handleInputChange('task_type', e.target.value)}
                      required
                    >
                      {taskTypes.map(type => (
                        <option key={type} value={type}>
                          {type.charAt(0).toUpperCase() + type.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="default_hours">
                      Default Hours <span className="required">*</span>
                    </label>
                    <input
                      type="number"
                      id="default_hours"
                      className="form-input"
                      value={formData.default_hours}
                      onChange={(e) => handleInputChange('default_hours', parseFloat(e.target.value) || 0)}
                      required
                      min="0.1"
                      step="0.5"
                      placeholder="2.0"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="required_qualification_level">
                      Required Qualification <span className="required">*</span>
                    </label>
                    <select
                      id="required_qualification_level"
                      className="form-input"
                      value={formData.required_qualification_level}
                      onChange={(e) => handleInputChange('required_qualification_level', e.target.value)}
                      required
                    >
                      <option value="BSc">BSc</option>
                      <option value="MSc">MSc</option>
                      <option value="PhD">PhD</option>
                    </select>
                  </div>
                </div>

                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="required_specialization">
                      Required Specialization
                    </label>
                    <input
                      type="text"
                      id="required_specialization"
                      className="form-input"
                      value={formData.required_specialization}
                      onChange={(e) => handleInputChange('required_specialization', e.target.value)}
                      placeholder="e.g., Computer Science"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="required_skills">
                      Required Skills (comma-separated)
                    </label>
                    <input
                      type="text"
                      id="required_skills"
                      className="form-input"
                      value={skillsInput}
                      onChange={(e) => handleSkillsInputChange(e.target.value)}
                      placeholder="e.g., Python, OOP, Databases"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="required_experience_years">
                      Required Experience (Years)
                    </label>
                    <input
                      type="number"
                      id="required_experience_years"
                      className="form-input"
                      value={formData.required_experience_years}
                      onChange={(e) => handleInputChange('required_experience_years', parseInt(e.target.value) || 0)}
                      min="0"
                      placeholder="0"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="is_active">
                      <input
                        type="checkbox"
                        id="is_active"
                        checked={formData.is_active}
                        onChange={(e) => handleInputChange('is_active', e.target.checked)}
                      />
                      <span style={{ marginLeft: '8px' }}>Active</span>
                    </label>
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="submit-button">
                  {editingTemplate ? 'Update Template' : 'Create Template'}
                </button>
                <button 
                  type="button" 
                  className="cancel-button"
                  onClick={() => {
                    resetForm();
                    setActiveTab('view-templates');
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'template-details' && (
        <div className="task-details-content">
          <h2 className="task-form-heading">Template Details</h2>
          {selectedTemplate ? (
            <div className="details-grid">
              <div className="detail-card">
                <h3 className="detail-card-title">{selectedTemplate.name}</h3>
                <div className="detail-card-content">
                  <div className="detail-item">
                    <span className="detail-label">ID:</span>
                    <span className="detail-value">{selectedTemplate.id}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Task Type:</span>
                    <span className="detail-value">{selectedTemplate.task_type}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Default Hours:</span>
                    <span className="detail-value">{selectedTemplate.default_hours}h</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Required Qualification:</span>
                    <span className="detail-value">{selectedTemplate.required_qualification_level}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Required Specialization:</span>
                    <span className="detail-value">{selectedTemplate.required_specialization || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Required Skills:</span>
                    <span className="detail-value">
                      {Array.isArray(selectedTemplate.required_skills) && selectedTemplate.required_skills.length > 0
                        ? selectedTemplate.required_skills.join(', ')
                        : 'N/A'}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Required Experience:</span>
                    <span className="detail-value">{selectedTemplate.required_experience_years} years</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Status:</span>
                    <span className="detail-value">
                      <span className={selectedTemplate.is_active ? 'status-active' : 'status-inactive'}>
                        {selectedTemplate.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="info-message">Select a template to view details</p>
          )}
        </div>
      )}
    </div>
  );
};

export default TaskTemplateManagement;

