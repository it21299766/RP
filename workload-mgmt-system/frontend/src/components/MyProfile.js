import React, { useState, useEffect, useContext } from 'react';
import './MyProfile.css';
import { staffApi } from '../api/staffApi';
import { AuthContext } from '../context/AuthContext';
import PopupMessage from './PopupMessage';

const MyProfile = () => {
  const { user: currentUser } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });

  useEffect(() => {
    if (currentUser && currentUser.staff_id) {
      loadProfile();
    }
  }, [currentUser]);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const staffData = await staffApi.getById(currentUser.staff_id);
      // Map backend response to frontend format
      const mappedProfile = {
        ...staffData,
        id: staffData.staff_id,
        position: staffData.designation,
        email: `${staffData.name.toLowerCase().replace(/\s+/g, '.')}@university.edu`,
        profilePicture: staffData.profile_picture_path 
          ? `http://localhost:8000/uploads/${staffData.profile_picture_path}`
          : null
      };
      setProfile(mappedProfile);
    } catch (error) {
      console.error('Error loading profile:', error);
      setPopup({
        show: true,
        message: `Error loading profile: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAvailability = async () => {
    if (!profile) return;

    const newAvailability = !profile.available;
    const statusText = newAvailability ? 'available' : 'on leave';
    
    // Confirm action
    const confirmMessage = newAvailability 
      ? 'Mark yourself as available? You will be considered for new assignments.'
      : 'Mark yourself as on leave? You will not be assigned new tasks.';
    
    if (!window.confirm(confirmMessage)) {
      return;
    }

    setUpdating(true);
    try {
      const updatedData = await staffApi.update(profile.staff_id || profile.id, {
        available: newAvailability
      });
      
      // Update local profile state
      setProfile(prev => ({
        ...prev,
        available: updatedData.available
      }));
      
      setPopup({
        show: true,
        message: `Availability updated: You are now ${statusText}.`,
        type: 'success'
      });
    } catch (error) {
      console.error('Error updating availability:', error);
      setPopup({
        show: true,
        message: `Error updating availability: ${error.message || 'Unknown error'}`,
        type: 'error'
      });
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="my-profile">
        <div className="loading-message">Loading profile...</div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="my-profile">
        <div className="empty-state">
          <div className="empty-state-icon">👤</div>
          <p className="empty-state-message">Profile not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="my-profile">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}

      <div className="profile-header">
        <span className="profile-icon">👤</span>
        <h1>My Profile</h1>
      </div>

      <div className="profile-container">
        <div className="profile-card">
          <div className="profile-avatar-section">
            {profile.profilePicture ? (
              <img 
                src={profile.profilePicture} 
                alt={profile.name} 
                className="profile-avatar" 
              />
            ) : (
              <div className="profile-avatar-placeholder">
                {profile.name.charAt(0).toUpperCase()}
              </div>
            )}
            <h2 className="profile-name">{profile.name}</h2>
            <p className="profile-role">{profile.role || 'ACADEMIC'}</p>
          </div>

          <div className="profile-details">
            <div className="detail-section">
              <h3 className="section-title">Personal Information</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Staff ID:</span>
                  <span className="detail-value">{profile.staff_id || profile.id || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Username:</span>
                  <span className="detail-value">{profile.username || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Email:</span>
                  <span className="detail-value">{profile.email || 'N/A'}</span>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3 className="section-title">Academic Information</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Designation:</span>
                  <span className="detail-value">{profile.designation || profile.position || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Department:</span>
                  <span className="detail-value">{profile.department || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Qualification:</span>
                  <span className="detail-value">{profile.qualification || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Specialization:</span>
                  <span className="detail-value">{profile.specialization || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Experience:</span>
                  <span className="detail-value">{profile.experience_years || 0} years</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Max Hours:</span>
                  <span className="detail-value">{profile.max_hours || 'N/A'} hours</span>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h3 className="section-title">Skills & Availability</h3>
              <div className="detail-grid">
                <div className="detail-item full-width">
                  <span className="detail-label">Skills:</span>
                  <span className="detail-value">
                    {Array.isArray(profile.skills) && profile.skills.length > 0
                      ? profile.skills.join(', ')
                      : 'N/A'}
                  </span>
                </div>
                <div className="detail-item full-width">
                  <div className="availability-container">
                    <div className="availability-info">
                      <span className="detail-label">Current Status:</span>
                      <span className={`availability-badge ${profile.available ? 'available' : 'unavailable'}`}>
                        {profile.available ? 'Available' : 'On Leave'}
                      </span>
                    </div>
                    <button
                      className="availability-button"
                      onClick={handleUpdateAvailability}
                      disabled={updating}
                    >
                      {updating 
                        ? 'Updating...' 
                        : profile.available 
                          ? 'Mark as On Leave' 
                          : 'Mark as Available'}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyProfile;

