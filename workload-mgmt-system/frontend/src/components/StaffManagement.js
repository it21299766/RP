import React, { useState, useEffect } from 'react';
import './StaffManagement.css';
import AddStaffForm from './AddStaffForm';
import PopupMessage from './PopupMessage';
import { staffApi } from '../api/staffApi';

const StaffManagement = ({ userRole = 'Administrator', currentUserEmail = '' }) => {
  const [activeTab, setActiveTab] = useState('view-staff');
  const [selectedDepartment, setSelectedDepartment] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [staffMembers, setStaffMembers] = useState([]);
  const [filteredStaff, setFilteredStaff] = useState([]);
  const [editingStaff, setEditingStaff] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [selectedStaff, setSelectedStaff] = useState(null);
  
  const isAdministrator = userRole === 'Administrator';
  const isStaff = userRole === 'Staff';
  
  // Find current user's profile
  const currentUserProfile = staffMembers.find(staff => 
    currentUserEmail && staff.email.toLowerCase() === currentUserEmail.toLowerCase()
  ) || (isStaff && staffMembers.length > 0 ? staffMembers[0] : null);
  
  // Check if selected staff is the current user's profile
  const isOwnProfile = isStaff && selectedStaff && currentUserProfile && 
    selectedStaff.id === currentUserProfile.id;

  /**
   * Load staff data from backend API
   * This function is reusable and can be called after updates to refresh data
   */
  const loadStaffData = async () => {
    try {
      const data = await staffApi.getAll();
      if (Array.isArray(data)) {
        // Map backend response to frontend format
        const mappedData = data.map(staff => ({
          ...staff,
          id: staff.staff_id, // Use staff_id as id for compatibility
          staff_id: staff.staff_id, // Ensure both id and staff_id are set
          position: staff.designation, // Map designation to position for display
          email: `${staff.name.toLowerCase().replace(/\s+/g, '.')}@university.edu`, // Generate email if not present
          // Calculate hours for display (if not present)
          teachingHours: staff.teachingHours || 0,
          researchHours: staff.researchHours || 0,
          totalHours: staff.totalHours || (staff.max_hours || 0)
        }));
        setStaffMembers(mappedData);
        setFilteredStaff(mappedData);
        try { 
          localStorage.setItem('staffMembers', JSON.stringify(mappedData)); 
        } catch (e) {
          console.warn('Failed to save to localStorage:', e);
        }
        return mappedData;
      }
    } catch (err) {
      console.error('Error loading staff:', err);
      setPopup({
        show: true,
        message: `Error loading staff: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
      // Fallback to localStorage if available
      const savedStaff = localStorage.getItem('staffMembers');
      if (savedStaff) {
        try {
          const parsedStaff = JSON.parse(savedStaff);
          setStaffMembers(parsedStaff);
          setFilteredStaff(parsedStaff);
          return parsedStaff;
        } catch (e) {
          console.error('Failed to parse localStorage data:', e);
        }
      }
      return [];
    }
  };

  // Load staff data on component mount
  useEffect(() => {
    let mounted = true;

    const fetchData = async () => {
      const data = await loadStaffData();
      if (!mounted) return;
    };

    fetchData();
    return () => { mounted = false; };
  }, []);

  // Auto-load staff profile when role is Staff (only set selectedStaff, don't force tab change)
  useEffect(() => {
    if (isStaff && staffMembers.length > 0 && !selectedStaff) {
      // Find current user's profile
      const userProfile = currentUserEmail 
        ? staffMembers.find(staff => staff.email.toLowerCase() === currentUserEmail.toLowerCase())
        : null;
      
      const profileToShow = userProfile || staffMembers[0];
      setSelectedStaff(profileToShow);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isStaff, currentUserEmail, staffMembers.length]);

  useEffect(() => {
    // Filter staff based on department and search query
    let filtered = staffMembers;

    if (selectedDepartment !== 'All') {
      filtered = filtered.filter(staff => staff.department === selectedDepartment);
    }

    if (searchQuery.trim() !== '') {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(staff =>
        staff.name.toLowerCase().includes(query) ||
        staff.email.toLowerCase().includes(query)
      );
    }

    setFilteredStaff(filtered);
  }, [selectedDepartment, searchQuery, staffMembers]);

  const departments = ['All', ...new Set(staffMembers.map(staff => staff.department))];

  // Save staff to localStorage
  const saveStaffToStorage = (staff) => {
    localStorage.setItem('staffMembers', JSON.stringify(staff));
  };

  // Handle staff added (Create)
  const handleStaffAdded = async (newStaff, action) => {
    if (action === 'cancel') {
      setEditingStaff(null);
      return;
    }
    
    if (newStaff) {
      try {
        const created = await staffApi.create(newStaff);
        // Map backend response
        const mappedStaff = {
          ...created,
          id: created.staff_id,
          position: created.designation,
          email: `${created.name.toLowerCase().replace(/\s+/g, '.')}@university.edu`
        };
        const updatedStaff = [...staffMembers, mappedStaff];
        setStaffMembers(updatedStaff);
        setFilteredStaff(updatedStaff);
        try { saveStaffToStorage(updatedStaff); } catch (e) {}
        setActiveTab('view-staff');
        setPopup({ show: true, message: 'Staff member added successfully!', type: 'success' });
      } catch (err) {
        console.error('Error creating staff:', err);
        setPopup({
          show: true,
          message: `Error adding staff: ${err.message || 'Unknown error'}`,
          type: 'error'
        });
      }
    }
  };

  // Handle staff updated (Update)
  const handleStaffUpdated = async (updatedStaff) => {
    // Get staff_id from editingStaff (handle both id and staff_id)
    const staffId = editingStaff?.staff_id || editingStaff?.id;
    
    if (!editingStaff || !staffId) {
      setPopup({
        show: true,
        message: 'Cannot update: Staff ID not found',
        type: 'error'
      });
      return;
    }

    try {
      // Update staff in backend database (this persists to database)
      const saved = await staffApi.update(staffId, updatedStaff);
      
      // Reload all staff data from backend to ensure we have the latest data
      // This ensures consistency between frontend and backend
      const refreshedStaffList = await loadStaffData();
      
      // Find the updated staff in the refreshed list
      const updatedStaffInList = refreshedStaffList.find(staff => 
        (staff.staff_id || staff.id) === saved.staff_id
      );
      
      // Map backend response to frontend format (preserve frontend-only fields)
      const mappedStaff = updatedStaffInList ? {
        ...updatedStaffInList,
        id: updatedStaffInList.staff_id,
        staff_id: updatedStaffInList.staff_id,
        position: updatedStaffInList.designation,
        email: updatedStaffInList.email || `${updatedStaffInList.name.toLowerCase().replace(/\s+/g, '.')}@university.edu`,
        // Preserve profile picture if it exists (frontend-only field)
        profilePicture: editingStaff.profilePicture || updatedStaffInList.profilePicture || ''
      } : {
        ...saved,
        id: saved.staff_id,
        staff_id: saved.staff_id,
        position: saved.designation,
        email: saved.email || `${saved.name.toLowerCase().replace(/\s+/g, '.')}@university.edu`,
        profilePicture: editingStaff.profilePicture || saved.profilePicture || ''
      };
      
      // Update selectedStaff if it's the same staff member being edited
      if (selectedStaff) {
        const selectedId = selectedStaff.staff_id || selectedStaff.id;
        if (selectedId === saved.staff_id) {
          setSelectedStaff(mappedStaff);
        }
      }
      
      // Clear editing state and switch to view tab
      setEditingStaff(null);
      setActiveTab('view-staff');
      
      // Show success message
      setPopup({ 
        show: true, 
        message: 'Staff record updated successfully! Changes are saved to database.', 
        type: 'success' 
      });
    } catch (err) {
      console.error('Error updating staff:', err);
      setPopup({
        show: true,
        message: `Error updating staff: ${err.message || 'Unknown error'}`,
        type: 'error'
      });
    }
  };

  // Handle staff deleted (Delete)
  const handleDeleteStaff = async (staff) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to delete staff members.',
        type: 'error'
      });
      return;
    }
    
    const staffId = staff.staff_id || staff.id;
    if (!staffId) {
      setPopup({
        show: true,
        message: 'Cannot delete: Staff ID not found',
        type: 'error'
      });
      return;
    }
    
    if (window.confirm(`Are you sure you want to delete ${staff.name}?`)) {
      try {
        await staffApi.delete(staffId);
        const updatedList = staffMembers.filter(s => (s.staff_id || s.id) !== staffId);
        setStaffMembers(updatedList);
        setFilteredStaff(updatedList);
        try { saveStaffToStorage(updatedList); } catch (e) {}
        if (selectedStaff && (selectedStaff.staff_id || selectedStaff.id) === staffId) {
          setSelectedStaff(null);
        }
        setPopup({ show: true, message: 'Staff member deleted successfully', type: 'delete' });
      } catch (err) {
        console.error('Error deleting staff:', err);
        setPopup({
          show: true,
          message: `Error deleting staff: ${err.message || 'Unknown error'}`,
          type: 'error'
        });
      }
    }
  };

  // Handle edit staff
  const handleEditStaff = (staff) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to edit staff members.',
        type: 'error'
      });
      return;
    }
    setEditingStaff(staff);
    setActiveTab('add-staff');
  };

  // Handle view staff
  const handleViewStaff = (staff) => {
    setSelectedStaff(staff);
    setActiveTab('staff-details');
  };

  // Handle profile picture upload in details section
  const handleProfilePictureUpload = (e) => {
    const file = e.target.files[0];
    if (file && selectedStaff) {
      // Check if staff user is trying to upload their own profile picture
      if (isStaff && currentUserProfile && selectedStaff.id !== currentUserProfile.id) {
        setPopup({
          show: true,
          message: 'You can only upload your own profile picture.',
          type: 'error'
        });
        return;
      }
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setPopup({
          show: true,
          message: 'Please select a valid image file.',
          type: 'error'
        });
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setPopup({
          show: true,
          message: 'Image size should be less than 5MB.',
          type: 'error'
        });
        return;
      }

      const reader = new FileReader();
      reader.onloadend = () => {
        // Update the selected staff's profile picture
        const updatedStaff = {
          ...selectedStaff,
          profilePicture: reader.result
        };
        
        // Update in staff members array
        const updatedList = staffMembers.map(staff => 
          staff.id === selectedStaff.id ? updatedStaff : staff
        );
        
        setStaffMembers(updatedList);
        setFilteredStaff(updatedList);
        saveStaffToStorage(updatedList);
        setSelectedStaff(updatedStaff);
        
        // Update currentUserProfile if it's the current user
        if (isStaff && selectedStaff === currentUserProfile) {
          // currentUserProfile will be updated via useEffect
        }
        
        // Show success popup
        setPopup({
          show: true,
          message: 'Profile picture updated successfully!',
          type: 'success'
        });
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="staff-management">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}
      <div className="staff-tabs">
        <button
          className={`tab-button ${activeTab === 'view-staff' ? 'active' : ''}`}
          onClick={() => setActiveTab('view-staff')}
        >
          View Staff
        </button>
        {isAdministrator && (
          <button
            className={`tab-button ${activeTab === 'add-staff' ? 'active' : ''}`}
            onClick={() => setActiveTab('add-staff')}
          >
            Add Staff
          </button>
        )}
        <button
          className={`tab-button ${activeTab === 'staff-details' ? 'active' : ''}`}
          onClick={() => setActiveTab('staff-details')}
        >
          {isStaff ? 'My Profile' : 'Staff Details'}
        </button>
      </div>

      {activeTab === 'view-staff' && (
        <div className="view-staff-content">
          <div className="filters-section">
            <div className="filter-group">
              <label htmlFor="department-filter">Filter by Department</label>
              <select
                id="department-filter"
                className="filter-select"
                value={selectedDepartment}
                onChange={(e) => setSelectedDepartment(e.target.value)}
              >
                {departments.map(dept => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="search-staff">Search Staff</label>
              <input
                id="search-staff"
                type="text"
                className="search-input"
                placeholder="Enter name or email"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <h1 className="staff-heading">Staff Members ({filteredStaff.length})</h1>

          <div className="staff-table-container">
            <table className="staff-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Designation</th>
                  <th>Department</th>
                  <th>Qualification</th>
                  <th>Specialization</th>
                  <th>Experience</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStaff.length > 0 ? (
                  filteredStaff.map(staff => (
                    <tr key={staff.id}>
                      <td>
                        <div className="staff-name-cell">
                          {staff.profilePicture ? (
                            <img src={staff.profilePicture} alt={staff.name} className="staff-avatar" />
                          ) : (
                            <div className="staff-avatar-placeholder">
                              {staff.name.charAt(0).toUpperCase()}
                            </div>
                          )}
                          <span>{staff.name}</span>
                        </div>
                      </td>
                      <td>{staff.designation || staff.position || 'N/A'}</td>
                      <td>{staff.department}</td>
                      <td>{staff.qualification || 'N/A'}</td>
                      <td>{staff.specialization || 'N/A'}</td>
                      <td>{staff.experience_years || 0} years</td>
                      <td>{staff.role || 'N/A'}</td>
                      <td>
                        <button 
                          className="action-button view"
                          onClick={() => handleViewStaff(staff)}
                        >
                          View Staff
                        </button>
                        {isAdministrator && (
                          <>
                            <button 
                              className="action-button"
                              onClick={() => handleEditStaff(staff)}
                            >
                              Edit
                            </button>
                            <button 
                              className="action-button delete"
                              onClick={() => handleDeleteStaff(staff)}
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
                    <td colSpan="8" className="no-data">No staff members found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'add-staff' && isAdministrator && (
        <AddStaffForm 
          onStaffAdded={handleStaffAdded}
          onStaffUpdated={handleStaffUpdated}
          editingStaff={editingStaff}
        />
      )}
      {activeTab === 'add-staff' && !isAdministrator && (
        <div className="view-staff-content">
          <p className="info-message">You do not have permission to add or edit staff members.</p>
        </div>
      )}

      {activeTab === 'staff-details' && (
        <div className="staff-details-content">
          <h1 className="staff-heading">{isStaff ? 'My Profile' : 'Staff Details'}</h1>
          {selectedStaff ? (
            <div className="details-grid">
              <div className="detail-card">
                <div className="staff-detail-header">
                  {selectedStaff.profilePicture ? (
                    <img src={selectedStaff.profilePicture} alt={selectedStaff.name} className="staff-detail-avatar" />
                  ) : (
                    <div className="staff-detail-avatar-placeholder">
                      {selectedStaff.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                  <h3 className="detail-card-title">{selectedStaff.name}</h3>
                  {(isAdministrator || isOwnProfile) && (
                    <div className="profile-upload-section">
                      <input
                        type="file"
                        id="profilePictureUpload"
                        accept="image/*"
                        onChange={handleProfilePictureUpload}
                        className="file-input-hidden"
                      />
                      <button
                        type="button"
                        onClick={() => document.getElementById('profilePictureUpload').click()}
                        className="upload-profile-button"
                      >
                        Upload Profile Pic
                      </button>
                    </div>
                  )}
                </div>
                <div className="detail-card-content">
                  <div className="detail-item">
                    <span className="detail-label">Staff ID:</span>
                    <span className="detail-value">{selectedStaff.staff_id || selectedStaff.id || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Designation:</span>
                    <span className="detail-value">{selectedStaff.designation || selectedStaff.position || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Department:</span>
                    <span className="detail-value">{selectedStaff.department || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Qualification:</span>
                    <span className="detail-value">{selectedStaff.qualification || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Specialization:</span>
                    <span className="detail-value">{selectedStaff.specialization || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Experience:</span>
                    <span className="detail-value">{selectedStaff.experience_years || 0} years</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Role:</span>
                    <span className="detail-value">{selectedStaff.role || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Skills:</span>
                    <span className="detail-value">
                      {Array.isArray(selectedStaff.skills) && selectedStaff.skills.length > 0
                        ? selectedStaff.skills.join(', ')
                        : 'N/A'}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Available:</span>
                    <span className="detail-value">{selectedStaff.available ? 'Yes' : 'No'}</span>
                  </div>
                  {selectedStaff.max_hours && (
                    <div className="detail-item">
                      <span className="detail-label">Max Hours/Week:</span>
                      <span className="detail-value">{selectedStaff.max_hours}h</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <p className="info-message">
              {isStaff 
                ? 'Loading your profile...' 
                : 'Click "View Staff" on a staff member from the View Staff tab to see their details here.'}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default StaffManagement;


