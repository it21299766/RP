import React, { useState, useEffect } from 'react';
import './AddStaffForm.css';
import PopupMessage from './PopupMessage';

const AddStaffForm = ({ onStaffAdded, onStaffUpdated, editingStaff }) => {
  const [formData, setFormData] = useState({
    name: '',
    designation: 'Lecturer',
    qualification: 'MSc',
    specialization: 'Computer Science',
    department: 'Computer Science',
    role: 'ACADEMIC',
    experience_years: 0,
    skills: [],
    available: true,
    password: '',
    max_hours: 20.0,
    profilePicture: '' // Frontend-only field
  });

  const [skillsInput, setSkillsInput] = useState(''); // For comma-separated input
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });

  // Load editing staff data if editing
  useEffect(() => {
    if (editingStaff) {
      const skillsArray = Array.isArray(editingStaff.skills) 
        ? editingStaff.skills 
        : (editingStaff.skills ? editingStaff.skills.split(',').map(s => s.trim()) : []);
      
      setFormData({
        name: editingStaff.name || '',
        designation: editingStaff.designation || 'Lecturer',
        qualification: editingStaff.qualification || 'MSc',
        specialization: editingStaff.specialization || 'Computer Science',
        department: editingStaff.department || 'Computer Science',
        role: editingStaff.role || 'ACADEMIC',
        experience_years: editingStaff.experience_years || 0,
        skills: skillsArray,
        available: editingStaff.available !== undefined ? editingStaff.available : true,
        password: '', // Don't pre-fill password
        max_hours: editingStaff.max_hours || 20.0,
        profilePicture: editingStaff.profilePicture || ''
      });
      setSkillsInput(skillsArray.join(', '));
    } else {
      resetForm();
    }
  }, [editingStaff]);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSkillsInputChange = (value) => {
    setSkillsInput(value);
    // Convert comma-separated string to array
    const skillsArray = value.split(',').map(s => s.trim()).filter(s => s.length > 0);
    setFormData(prev => ({
      ...prev,
      skills: skillsArray
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      designation: 'Lecturer',
      qualification: 'MSc',
      specialization: 'Computer Science',
      department: 'Computer Science',
      role: 'ACADEMIC',
      experience_years: 0,
      skills: [],
      available: true,
      password: '',
      max_hours: 20.0,
      profilePicture: ''
    });
    setSkillsInput('');
    setError(null);
  };

  // Handle profile picture upload (frontend-only)
  const handleProfilePictureChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file.');
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        setError('Image size should be less than 5MB.');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData(prev => ({
          ...prev,
          profilePicture: reader.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    // Validate form
    if (!formData.name.trim()) {
      setError('Name is required.');
      setIsSubmitting(false);
      return;
    }

    if (!formData.specialization.trim()) {
      setError('Specialization is required.');
      setIsSubmitting(false);
      return;
    }

    // Prepare data for backend
    const submitData = {
      name: formData.name.trim(),
      designation: formData.designation,
      qualification: formData.qualification,
      specialization: formData.specialization.trim(),
      department: formData.department,
      role: formData.role,
      experience_years: parseInt(formData.experience_years) || 0,
      skills: formData.skills,
      available: formData.available,
      max_hours: parseFloat(formData.max_hours) || null
    };

    // Add password only if provided (for new staff)
    if (!editingStaff && formData.password.trim()) {
      submitData.password = formData.password;
    }

    if (editingStaff) {
      // Update existing staff
      if (onStaffUpdated) {
        onStaffUpdated(submitData);
      }
    } else {
      // Add new staff
      if (onStaffAdded) {
        onStaffAdded(submitData);
      }
    }
    
    setIsSubmitting(false);
  };

  const handleCancel = () => {
    resetForm();
    if (onStaffAdded) {
      onStaffAdded(null, 'cancel');
    }
  };

  const designations = [
    'Professor',
    'Senior Professor',
    'Associate Professor',
    'Senior Lecturer I',
    'Senior Lecturer II',
    'Lecturer',
    'Probationary Lecturer',
    'Temporary Lecturer',
    'Instructor',
    'Head of Department'
  ];

  const departments = [
    'Computer Science',
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'Engineering',
    'Business',
    'Arts'
  ];

  const specializations = [
    'Computer Science',
    'Software Engineering',
    'Artificial Intelligence',
    'Data Science',
    'Networks',
    'Cybersecurity',
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'General'
  ];

  return (
    <div className="add-staff-content">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}
      <h1 className="staff-heading">
        {editingStaff ? 'Edit Staff Member' : 'Add New Staff Member'}
      </h1>
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}
      <div className="form-container">
        <form className="staff-form" onSubmit={handleSubmit}>
          <div className="form-columns">
            {/* Left Column */}
            <div className="form-column">
              <div className="form-group">
                <label htmlFor="name">
                  Name <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  className="form-input"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  required
                  placeholder="e.g., Dr. John Smith"
                />
              </div>

              <div className="form-group">
                <label htmlFor="designation">
                  Designation <span className="required">*</span>
                </label>
                <select
                  id="designation"
                  className="form-input"
                  value={formData.designation}
                  onChange={(e) => handleInputChange('designation', e.target.value)}
                  required
                >
                  {designations.map(des => (
                    <option key={des} value={des}>{des}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="qualification">
                  Highest Qualification <span className="required">*</span>
                </label>
                <select
                  id="qualification"
                  className="form-input"
                  value={formData.qualification}
                  onChange={(e) => handleInputChange('qualification', e.target.value)}
                  required
                >
                  <option value="BSc">BSc</option>
                  <option value="MSc">MSc</option>
                  <option value="PhD">PhD</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="specialization">
                  Specialization <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="specialization"
                  className="form-input"
                  value={formData.specialization}
                  onChange={(e) => handleInputChange('specialization', e.target.value)}
                  required
                  placeholder="e.g., Artificial Intelligence"
                  list="specialization-list"
                />
                <datalist id="specialization-list">
                  {specializations.map(spec => (
                    <option key={spec} value={spec} />
                  ))}
                </datalist>
              </div>

              <div className="form-group">
                <label htmlFor="department">
                  Department <span className="required">*</span>
                </label>
                <select
                  id="department"
                  className="form-input"
                  value={formData.department}
                  onChange={(e) => handleInputChange('department', e.target.value)}
                  required
                >
                  {departments.map(dept => (
                    <option key={dept} value={dept}>{dept}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="role">
                  System Role <span className="required">*</span>
                </label>
                <select
                  id="role"
                  className="form-input"
                  value={formData.role}
                  onChange={(e) => handleInputChange('role', e.target.value)}
                  required
                >
                  <option value="ACADEMIC">ACADEMIC</option>
                  <option value="ADMIN">ADMIN</option>
                  <option value="MANAGEMENT">MANAGEMENT</option>
                </select>
              </div>
            </div>

            {/* Right Column */}
            <div className="form-column">
              <div className="form-group">
                <label htmlFor="experience_years">
                  Experience (Years) <span className="required">*</span>
                </label>
                <input
                  type="number"
                  id="experience_years"
                  className="form-input"
                  value={formData.experience_years}
                  onChange={(e) => handleInputChange('experience_years', parseInt(e.target.value) || 0)}
                  required
                  min="0"
                  placeholder="0"
                />
              </div>

              <div className="form-group">
                <label htmlFor="skills">
                  Skills (comma-separated)
                </label>
                <input
                  type="text"
                  id="skills"
                  className="form-input"
                  value={skillsInput}
                  onChange={(e) => handleSkillsInputChange(e.target.value)}
                  placeholder="e.g., Python, Machine Learning, OOP"
                />
                {formData.skills.length > 0 && (
                  <div className="skills-tags">
                    {formData.skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="max_hours">
                  Max Hours/Week (Optional)
                </label>
                <input
                  type="number"
                  id="max_hours"
                  className="form-input"
                  value={formData.max_hours}
                  onChange={(e) => handleInputChange('max_hours', parseFloat(e.target.value) || 0)}
                  min="0"
                  step="0.5"
                  placeholder="20.0"
                />
                <small className="form-hint">Leave empty to use designation policy</small>
              </div>

              <div className="form-group">
                <label htmlFor="available">
                  <input
                    type="checkbox"
                    id="available"
                    checked={formData.available}
                    onChange={(e) => handleInputChange('available', e.target.checked)}
                  />
                  <span style={{ marginLeft: '8px' }}>Available for Assignment</span>
                </label>
              </div>

              {!editingStaff && (
                <div className="form-group">
                  <label htmlFor="password">
                    Password (Optional)
                  </label>
                  <input
                    type="password"
                    id="password"
                    className="form-input"
                    value={formData.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    placeholder="Leave empty to set later"
                  />
                  <small className="form-hint">If not provided, password must be set later</small>
                </div>
              )}

              <div className="form-group">
                <label htmlFor="profilePicture">
                  Profile Picture (Frontend Only)
                </label>
                <div className="profile-picture-upload">
                  {formData.profilePicture ? (
                    <div className="profile-picture-preview">
                      <img src={formData.profilePicture} alt="Profile preview" className="profile-preview-img" />
                    </div>
                  ) : (
                    <div className="profile-picture-placeholder">
                      <span className="placeholder-icon">👤</span>
                      <span className="placeholder-text">No picture</span>
                    </div>
                  )}
                  <input
                    type="file"
                    id="profilePicture"
                    accept="image/*"
                    onChange={handleProfilePictureChange}
                    className="file-input"
                  />
                  <button
                    type="button"
                    onClick={() => document.getElementById('profilePicture').click()}
                    className="upload-button"
                  >
                    {formData.profilePicture ? 'Change Picture' : 'Upload from Device'}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              className="submit-button"
              disabled={isSubmitting}
            >
              {isSubmitting 
                ? (editingStaff ? 'Updating...' : 'Adding...') 
                : (editingStaff ? 'Update Staff' : 'Add Staff')
              }
            </button>
            <button 
              type="button" 
              className="cancel-button"
              onClick={handleCancel}
              disabled={isSubmitting}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddStaffForm;
