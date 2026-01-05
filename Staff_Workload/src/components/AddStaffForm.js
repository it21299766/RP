/**
 * AddStaffForm Component
 * 
 * This component provides a form for adding new staff members or editing existing ones.
 * It handles staff data input, validation, and submission.
 * 
 * Features:
 * - Dual mode: Add new staff or edit existing staff
 * - Profile picture upload with preview
 * - Form validation (required fields, file type, file size)
 * - Number input controls with increment/decrement buttons
 * - Auto-generated staff IDs
 * - LocalStorage integration (via parent component)
 * - Success/error popup messages
 * 
 * Props:
 * - onStaffAdded: Function - Callback when new staff is added, receives (staffData, action)
 *   - staffData: Object - New staff member data
 *   - action: String - 'cancel' to abort, undefined for successful add
 * - onStaffUpdated: Function - Callback when staff is updated, receives (updatedStaffData)
 * - editingStaff: Object|null - Staff member object being edited, null for new staff
 * 
 * Form Fields:
 * - staffId: String - Auto-generated or user-entered staff ID
 * - name: String (required) - Staff member's full name
 * - email: String (required) - Staff member's email address
 * - department: String (required) - Department selection
 * - role: String (required) - Position/role selection
 * - qualifications: String (required) - Comma-separated qualifications
 * - profilePicture: String - Base64 encoded image data
 * - minContactHoursYear: Number - Minimum contact hours per year
 * - minContactHoursWeek: Number - Minimum contact hours per week
 * - maxHoursWeek: Number - Maximum hours per week
 * - minHoursWeek: Number - Minimum hours per week
 * 
 * Validation:
 * - Required fields: name, email
 * - Profile picture: Must be image file, max 5MB
 * - File type: Only image files accepted
 * 
 * Dependencies:
 * - PopupMessage: Component for displaying success/error messages
 */
// Import React hooks for state management and side effects
import React, { useState, useEffect } from 'react';
// Import CSS styles for this component
import './AddStaffForm.css';
// Import PopupMessage component for notifications
import PopupMessage from './PopupMessage';

// Component function that receives props via destructuring
const AddStaffForm = ({ onStaffAdded, onStaffUpdated, editingStaff }) => {
  // State: Object storing all form input values
  const [formData, setFormData] = useState({
    staffId: 'STAFF001', // Auto-generated staff identifier
    name: '', // Staff member's full name (required)
    email: '', // Staff member's email address (required)
    department: 'Computer Science', // Default department selection
    role: 'professor', // Default role/position
    qualifications: '', // Comma-separated qualifications (required)
    minContactHoursYear: 300.00, // Minimum contact hours per year (decimal)
    minContactHoursWeek: 10.00, // Minimum contact hours per week (decimal)
    maxHoursWeek: 30.00, // Maximum hours per week (decimal)
    minHoursWeek: 15.00, // Minimum hours per week (decimal)
    profilePicture: '' // Base64 encoded image data (optional)
  });

  // State: Boolean flag indicating if form is currently being submitted
  const [isSubmitting, setIsSubmitting] = useState(false);
  // State: String storing error message (null if no error)
  const [error, setError] = useState(null);
  // State: Boolean flag indicating successful submission (not currently used)
  const [success, setSuccess] = useState(false);
  // State: Object controlling popup message display
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });

  /**
   * useEffect: Load Editing Staff Data
   * Runs when editingStaff prop changes
   * If editingStaff exists, populates form with existing data
   * If editingStaff is null, resets form to default values
   */
  useEffect(() => {
    // Check if we're editing an existing staff member
    if (editingStaff) {
      // Populate form with existing staff data
      setFormData({
        staffId: editingStaff.staffId || `STAFF${editingStaff.id.toString().padStart(3, '0')}`, // Use existing staffId or generate from id
        name: editingStaff.name || '', // Use existing name or empty string
        email: editingStaff.email || '', // Use existing email or empty string
        department: editingStaff.department || 'Computer Science', // Use existing department or default
        role: editingStaff.role || (editingStaff.position ? editingStaff.position.toLowerCase() : 'professor'), // Use role or convert position to lowercase
        qualifications: editingStaff.qualifications || '', // Use existing qualifications or empty string
        minContactHoursYear: editingStaff.minContactHoursYear || 300.00, // Use existing value or default
        minContactHoursWeek: editingStaff.minContactHoursWeek || editingStaff.teachingHours || 10.00, // Use existing value or teachingHours or default
        maxHoursWeek: editingStaff.maxHoursWeek || 30.00, // Use existing value or default
        minHoursWeek: editingStaff.minHoursWeek || editingStaff.totalHours || 15.00, // Use existing value or totalHours or default
        profilePicture: editingStaff.profilePicture || '' // Use existing profile picture or empty string
      });
    } else {
      // Reset form to default values for new staff entry
      setFormData({
        staffId: 'STAFF001', // Default staff ID
        name: '', // Empty name field
        email: '', // Empty email field
        department: 'Computer Science', // Default department
        role: 'professor', // Default role
        qualifications: '', // Empty qualifications
        minContactHoursYear: 300.00, // Default minimum contact hours per year
        minContactHoursWeek: 10.00, // Default minimum contact hours per week
        maxHoursWeek: 30.00, // Default maximum hours per week
        minHoursWeek: 15.00, // Default minimum hours per week
        profilePicture: '' // Empty profile picture
      });
    }
  }, [editingStaff]); // Re-run when editingStaff prop changes

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNumberChange = (field, delta) => {
    setFormData(prev => {
      const currentValue = parseFloat(prev[field]) || 0;
      const newValue = Math.max(0, currentValue + delta);
      return {
        ...prev,
        [field]: newValue.toFixed(2)
      };
    });
  };

  const resetForm = () => {
    setFormData({
      staffId: 'STAFF001',
      name: '',
      email: '',
      department: 'Computer Science',
      role: 'professor',
      qualifications: '',
      minContactHoursYear: 300.00,
      minContactHoursWeek: 10.00,
      maxHoursWeek: 30.00,
      minHoursWeek: 15.00,
      profilePicture: ''
    });
    setError(null);
    setSuccess(false);
  };

  // Handle profile picture upload
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
    setSuccess(false);

    // Validate form
    if (!formData.name.trim() || !formData.email.trim()) {
      setError('Please fill in all required fields.');
      setIsSubmitting(false);
      return;
    }

    // Simulate async operation
    setTimeout(() => {
      try {
        // Prepare data - convert numeric strings to numbers
        const submitData = {
          ...formData,
          id: editingStaff ? editingStaff.id : undefined, // Keep ID if editing
          minContactHoursYear: parseFloat(formData.minContactHoursYear) || 0,
          minContactHoursWeek: parseFloat(formData.minContactHoursWeek) || 0,
          maxHoursWeek: parseFloat(formData.maxHoursWeek) || 0,
          minHoursWeek: parseFloat(formData.minHoursWeek) || 0,
          // Map role to position for compatibility
          position: formData.role.charAt(0).toUpperCase() + formData.role.slice(1),
          // Calculate hours
          totalHours: parseFloat(formData.minHoursWeek) || 0,
          teachingHours: parseFloat(formData.minContactHoursWeek) || 0,
          researchHours: Math.max(0, (parseFloat(formData.maxHoursWeek) || 0) - (parseFloat(formData.minContactHoursWeek) || 0))
        };

        if (editingStaff) {
          // Update existing staff
          if (onStaffUpdated) {
            onStaffUpdated(submitData);
          }
          // Popup will be shown by parent component (StaffManagement)
          setTimeout(() => {
            resetForm();
          }, 2000);
        } else {
          // Add new staff
          if (onStaffAdded) {
            onStaffAdded(submitData);
          }
          setPopup({
            show: true,
            message: 'Staff member added successfully!',
            type: 'success'
          });
          resetForm();
        }
      } catch (error) {
        console.error('Error:', error);
        setError('An error occurred. Please try again.');
      } finally {
        setIsSubmitting(false);
      }
    }, 500); // Simulate network delay
  };

  const handleCancel = () => {
    resetForm();
    // Optionally navigate back to view staff
    if (onStaffAdded) {
      onStaffAdded(null, 'cancel');
    }
  };

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
                <label htmlFor="staffId">
                  Staff ID <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="staffId"
                  className="form-input"
                  value={formData.staffId}
                  onChange={(e) => handleInputChange('staffId', e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="profilePicture">
                  Profile Picture
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
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">
                  Email <span className="required">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  className="form-input"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  required
                />
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
                  <option value="Computer Science">Computer Science</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="Physics">Physics</option>
                  <option value="Chemistry">Chemistry</option>
                  <option value="Biology">Biology</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="role">
                  Role <span className="required">*</span>
                </label>
                <select
                  id="role"
                  className="form-input"
                  value={formData.role}
                  onChange={(e) => handleInputChange('role', e.target.value)}
                  required
                >
                  <option value="professor">Professor</option>
                  <option value="associate professor">Associate Professor</option>
                  <option value="assistant professor">Assistant Professor</option>
                  <option value="lecturer">Lecturer</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="qualifications">
                  Qualifications (comma-separated) <span className="required">*</span>
                </label>
                <input
                  type="text"
                  id="qualifications"
                  className="form-input"
                  value={formData.qualifications}
                  onChange={(e) => handleInputChange('qualifications', e.target.value)}
                  placeholder="CS101, CS201, CS301"
                  required
                />
              </div>
            </div>

            {/* Right Column */}
            <div className="form-column">
              <div className="form-group">
                <label htmlFor="minContactHoursYear">
                  Min Contact Hours/Year <span className="required">*</span>
                </label>
                <div className="number-input-group">
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minContactHoursYear', -1)}
                  >
                    -
                  </button>
                  <input
                    type="number"
                    id="minContactHoursYear"
                    className="form-input number-input"
                    step="0.01"
                    min="0"
                    value={formData.minContactHoursYear}
                    onChange={(e) => handleInputChange('minContactHoursYear', e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minContactHoursYear', 1)}
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="minContactHoursWeek">
                  Min Contact Hours/Week <span className="required">*</span>
                </label>
                <div className="number-input-group">
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minContactHoursWeek', -1)}
                  >
                    -
                  </button>
                  <input
                    type="number"
                    id="minContactHoursWeek"
                    className="form-input number-input"
                    step="0.01"
                    min="0"
                    value={formData.minContactHoursWeek}
                    onChange={(e) => handleInputChange('minContactHoursWeek', e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minContactHoursWeek', 1)}
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="maxHoursWeek">
                  Max Hours/Week <span className="required">*</span>
                </label>
                <div className="number-input-group">
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('maxHoursWeek', -1)}
                  >
                    -
                  </button>
                  <input
                    type="number"
                    id="maxHoursWeek"
                    className="form-input number-input"
                    step="0.01"
                    min="0"
                    value={formData.maxHoursWeek}
                    onChange={(e) => handleInputChange('maxHoursWeek', e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('maxHoursWeek', 1)}
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="minHoursWeek">
                  Min Hours/Week <span className="required">*</span>
                </label>
                <div className="number-input-group">
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minHoursWeek', -1)}
                  >
                    -
                  </button>
                  <input
                    type="number"
                    id="minHoursWeek"
                    className="form-input number-input"
                    step="0.01"
                    min="0"
                    value={formData.minHoursWeek}
                    onChange={(e) => handleInputChange('minHoursWeek', e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="number-button"
                    onClick={() => handleNumberChange('minHoursWeek', 1)}
                  >
                    +
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

