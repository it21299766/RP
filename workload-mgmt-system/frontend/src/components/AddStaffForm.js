import React, { useState, useEffect } from 'react';
import './AddStaffForm.css';
import PopupMessage from './PopupMessage';
import { staffApi } from '../api/staffApi';

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
    profilePictureFile: null, // File object for upload
    profilePicturePreview: '' // Preview URL (for display only)
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
        profilePictureFile: null, // No file selected initially
        profilePicturePreview: editingStaff.profilePicture || '' // Show existing picture if available
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
      profilePictureFile: null,
      profilePicturePreview: ''
    });
    setSkillsInput('');
    setError(null);
  };

  // Handle profile picture file selection
  const handleProfilePictureChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file.');
        return;
      }
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('Image size should be less than 5MB.');
        return;
      }
      // Store file object and create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData(prev => ({
          ...prev,
          profilePictureFile: file, // Store File object for upload
          profilePicturePreview: reader.result // Preview URL for display
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
      const updateStaff = async () => {
        try {
          const staffId = editingStaff.staff_id || editingStaff.id;
          if (!staffId) {
            setError('Staff ID not found');
            setIsSubmitting(false);
            return;
          }
          
          // If only profile picture is being changed, just upload the picture
          const hasOnlyProfilePictureChange = formData.profilePictureFile && 
            Object.keys(submitData).every(key => {
              const currentValue = submitData[key];
              const originalValue = editingStaff[key] || editingStaff[key === 'experience_years' ? 'experience_years' : key];
              
              // Handle arrays (skills)
              if (Array.isArray(currentValue) && Array.isArray(originalValue)) {
                return JSON.stringify(currentValue.sort()) === JSON.stringify(originalValue.sort());
              }
              
              return currentValue === originalValue;
            });
          
          if (hasOnlyProfilePictureChange) {
            // Only profile picture changed - just upload it
            try {
              await staffApi.uploadProfilePicture(staffId, formData.profilePictureFile);
              setPopup({ show: true, message: 'Profile picture updated successfully', type: 'success' });
              if (onStaffUpdated) {
                // Reload staff data to show updated picture
                const updatedStaff = await staffApi.getById(staffId);
                onStaffUpdated(updatedStaff);
              }
              setIsSubmitting(false);
              return;
            } catch (uploadErr) {
              console.error('Error uploading profile picture:', uploadErr);
              setError(`Profile picture upload failed: ${uploadErr.message || 'Unknown error'}`);
              setIsSubmitting(false);
              return;
            }
          }
          
          // Update staff data first
          await onStaffUpdated(submitData);
          
          // Upload profile picture if file was selected
          if (formData.profilePictureFile) {
            try {
              await staffApi.uploadProfilePicture(staffId, formData.profilePictureFile);
              // Reload staff data to show updated picture
              const updatedStaff = await staffApi.getById(staffId);
              if (onStaffUpdated) {
                onStaffUpdated(updatedStaff);
              }
            } catch (uploadErr) {
              console.error('Error uploading profile picture:', uploadErr);
              setError(`Profile picture upload failed: ${uploadErr.message || 'Unknown error'}`);
              setIsSubmitting(false);
              return;
            }
          }
        } catch (err) {
          console.error('Error updating staff:', err);
          setError(`Error updating staff: ${err.message || 'Unknown error'}`);
          setIsSubmitting(false);
        }
      };
      
      updateStaff();
    } else {
      // Add new staff
      setIsSubmitting(false);
      if (onStaffAdded) {
        onStaffAdded(submitData);
      }
    }
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

              {editingStaff && (
                <div className="form-group">
                  <label htmlFor="profilePicture">
                    Profile Picture
                  </label>
                  <div className="profile-picture-upload">
                    {formData.profilePicturePreview ? (
                      <div className="profile-picture-preview">
                        <img src={formData.profilePicturePreview} alt="Profile preview" className="profile-preview-img" />
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
                      {formData.profilePicturePreview ? 'Change Picture' : 'Upload Picture'}
                    </button>
                    {formData.profilePictureFile && (
                      <small className="form-hint" style={{ display: 'block', marginTop: '0.5rem', color: '#28a745' }}>
                        Picture will be uploaded when you save changes
                      </small>
                    )}
                  </div>
                </div>
              )}
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
