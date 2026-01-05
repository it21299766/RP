/**
 * StaffManagement Component
 * 
 * This component manages staff members in the system with role-based access control.
 * It provides functionality to view, add, edit, and delete staff members.
 * 
 * Features:
 * - Role-based access control (Administrators can add/edit/delete, Staff can only view)
 * - Staff profile viewing with detailed information
 * - Profile picture upload (staff can upload their own, admins can upload any)
 * - Department and search filtering
 * - LocalStorage persistence for staff data
 * - Tab-based navigation (View Staff, Add Staff, Staff Details)
 * 
 * Props:
 * - userRole: String - 'Administrator' or 'Staff' (default: 'Administrator')
 * - currentUserEmail: String - Email of the currently logged-in user (for staff profile matching)
 * 
 * Role Permissions:
 * - Administrator: Full access (add, edit, delete, view all staff)
 * - Staff: View-only access (can view all staff, but can only edit/upload their own profile)
 * 
 * Data Persistence:
 * - Staff data is stored in localStorage under key 'staffMembers'
 * - Automatically loads saved data on component mount
 * - Saves data after any create, update, or delete operation
 * 
 * Dependencies:
 * - AddStaffForm: Form component for adding/editing staff
 * - PopupMessage: Component for displaying success/error messages
 */
// Import React hooks for state management and side effects
import React, { useState, useEffect } from 'react';
// Import CSS styles for this component
import './StaffManagement.css';
// Import AddStaffForm component for adding/editing staff
import AddStaffForm from './AddStaffForm';
// Import PopupMessage component for displaying notifications
import PopupMessage from './PopupMessage';

// Component function that receives props via destructuring with default values
const StaffManagement = ({ userRole = 'Administrator', currentUserEmail = '' }) => {
  /**
   * State: activeTab
   * Controls which tab is currently displayed
   * Values: 'view-staff', 'add-staff', 'staff-details'
   */
  // Initialize activeTab state to 'view-staff' (default tab)
  const [activeTab, setActiveTab] = useState('view-staff');

  /**
   * State: selectedDepartment
   * Stores the currently selected department filter
   * Value 'All' shows all departments
   */
  const [selectedDepartment, setSelectedDepartment] = useState('All');

  /**
   * State: searchQuery
   * Stores the search input for filtering staff by name or email
   */
  const [searchQuery, setSearchQuery] = useState('');

  /**
   * State: staffMembers
   * Array of all staff member objects
   * Each object contains: id, name, email, department, position, hours, etc.
   */
  const [staffMembers, setStaffMembers] = useState([]);

  /**
   * State: filteredStaff
   * Array of staff members after applying department and search filters
   * Updated automatically when staffMembers, selectedDepartment, or searchQuery changes
   */
  const [filteredStaff, setFilteredStaff] = useState([]);

  /**
   * State: editingStaff
   * Stores the staff member object being edited (null if not editing)
   * When set, the AddStaffForm switches to edit mode
   */
  const [editingStaff, setEditingStaff] = useState(null);

  /**
   * State: popup
   * Controls popup message display
   * Object with: { show: boolean, message: string, type: 'success'|'error'|'delete' }
   */
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });

  /**
   * State: selectedStaff
   * Stores the staff member currently being viewed in the details tab
   */
  const [selectedStaff, setSelectedStaff] = useState(null);
  
  /**
   * Computed: isAdministrator
   * Boolean indicating if current user has Administrator role
   */
  const isAdministrator = userRole === 'Administrator';

  /**
   * Computed: isStaff
   * Boolean indicating if current user has Staff role
   */
  const isStaff = userRole === 'Staff';
  
  /**
   * Computed: currentUserProfile
   * Finds the staff profile matching the current user's email
   * Falls back to first staff member if no match found (for staff users)
   */
  const currentUserProfile = staffMembers.find(staff => 
    currentUserEmail && staff.email.toLowerCase() === currentUserEmail.toLowerCase()
  ) || (isStaff && staffMembers.length > 0 ? staffMembers[0] : null);
  
  /**
   * Computed: isOwnProfile
   * Boolean indicating if the selected staff profile belongs to the current user
   * Used to determine if staff user can upload/edit their own profile picture
   */
  const isOwnProfile = isStaff && selectedStaff && currentUserProfile && 
    selectedStaff.id === currentUserProfile.id;

  /**
   * useEffect: Load Staff Data
   * Runs once on component mount to load staff data from localStorage.
   * If no saved data exists, initializes with sample data.
   * This ensures data persistence across page refreshes.
   */
  useEffect(() => {
    // Inner function to load staff data
    const loadStaffData = () => {
      // Retrieve saved staff data from browser's localStorage
      const savedStaff = localStorage.getItem('staffMembers');
      // Check if saved data exists
      if (savedStaff) {
        // Parse JSON string back into JavaScript array
        const parsedStaff = JSON.parse(savedStaff);
        // Update staffMembers state with loaded data
        setStaffMembers(parsedStaff);
        // Initialize filteredStaff with all loaded staff (no filter applied yet)
        setFilteredStaff(parsedStaff);
      } else {
        // If no saved data, create initial sample data for demonstration
        const sampleData = [
          {
            id: 1,
            name: 'Dr. John Smith',
            email: 'john.smith@university.edu',
            department: 'Computer Science',
            position: 'Professor',
            teachingHours: 12,
            researchHours: 6,
            totalHours: 18
          },
          {
            id: 2,
            name: 'Dr. Sarah Johnson',
            email: 'sarah.johnson@university.edu',
            department: 'Mathematics',
            position: 'Associate Professor',
            teachingHours: 10,
            researchHours: 5,
            totalHours: 15
          },
          {
            id: 3,
            name: 'Dr. Michael Williams',
            email: 'michael.williams@university.edu',
            department: 'Physics',
            position: 'Professor',
            teachingHours: 15,
            researchHours: 5,
            totalHours: 20
          },
          {
            id: 4,
            name: 'Dr. Emily Brown',
            email: 'emily.brown@university.edu',
            department: 'Computer Science',
            position: 'Assistant Professor',
            teachingHours: 8,
            researchHours: 4,
            totalHours: 12
          },
          {
            id: 5,
            name: 'Dr. David Davis',
            email: 'david.davis@university.edu',
            department: 'Mathematics',
            position: 'Associate Professor',
            teachingHours: 11,
            researchHours: 5,
            totalHours: 16
          }
        ];
        // Update staffMembers state with sample data
        setStaffMembers(sampleData);
        // Initialize filteredStaff with sample data
        setFilteredStaff(sampleData);
        // Save sample data to localStorage for persistence
        localStorage.setItem('staffMembers', JSON.stringify(sampleData));
      }
    };

    // Call the load function when component mounts
    loadStaffData();
  }, []); // Empty dependency array means this runs only once on mount

  /**
   * useEffect: Auto-load Staff Profile
   * For staff users, automatically selects their profile when data loads.
   * This allows staff to see their profile without manually selecting it.
   * Note: Does not force tab change, allowing staff to navigate to "View Staff" first.
   */
  useEffect(() => {
    // Check if user is staff, staff data exists, and no staff is currently selected
    if (isStaff && staffMembers.length > 0 && !selectedStaff) {
      // Find current user's profile by matching email
      const userProfile = currentUserEmail 
        ? // If currentUserEmail exists, search for matching staff member
          staffMembers.find(staff => staff.email.toLowerCase() === currentUserEmail.toLowerCase())
        : // If no email provided, set to null
          null;
      
      // Use found profile or fall back to first staff member
      const profileToShow = userProfile || staffMembers[0];
      // Set the profile to display
      setSelectedStaff(profileToShow);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isStaff, currentUserEmail, staffMembers.length]); // Re-run when these values change

  /**
   * useEffect: Filter Staff
   * Automatically filters staff list when:
   * - Department filter changes
   * - Search query changes
   * - Staff members list changes
   * Applies both department and search filters simultaneously.
   */
  useEffect(() => {
    // Start with all staff members
    let filtered = staffMembers;

    // Apply department filter if a specific department is selected (not 'All')
    if (selectedDepartment !== 'All') {
      // Filter to only include staff matching selected department
      filtered = filtered.filter(staff => staff.department === selectedDepartment);
    }

    // Apply search filter if search query is not empty
    if (searchQuery.trim() !== '') {
      // Convert search query to lowercase for case-insensitive matching
      const query = searchQuery.toLowerCase();
      // Filter to only include staff whose name or email contains the search query
      filtered = filtered.filter(staff =>
        staff.name.toLowerCase().includes(query) || // Check if name contains query
        staff.email.toLowerCase().includes(query) // Check if email contains query
      );
    }

    // Update filteredStaff state with filtered results
    setFilteredStaff(filtered);
  }, [selectedDepartment, searchQuery, staffMembers]); // Re-run when these values change

  /**
   * Computed: departments
   * Creates array of unique department names from staff members
   * Includes 'All' as first option for filter dropdown
   */
  // Extract unique departments from staff members and prepend 'All' option
  const departments = ['All', ...new Set(staffMembers.map(staff => staff.department))];

  /**
   * Function: saveStaffToStorage
   * Persists staff data to localStorage
   * Called after any create, update, or delete operation
   * @param {Array} staff - Array of staff member objects to save
   */
  const saveStaffToStorage = (staff) => {
    // Convert array to JSON string and save to localStorage
    localStorage.setItem('staffMembers', JSON.stringify(staff));
  };

  /**
   * Handler: handleStaffAdded
   * Processes new staff member creation
   * Generates ID if not provided, adds to list, saves to localStorage, and shows success message
   * @param {Object} newStaff - New staff member object
   * @param {string} action - Action type ('cancel' to abort)
   */
  const handleStaffAdded = (newStaff, action) => {
    // Check if action is 'cancel' (form was cancelled)
    if (action === 'cancel') {
      // Clear editing state
      setEditingStaff(null);
      // Exit function early
      return;
    }
    
    // Check if newStaff object exists
    if (newStaff) {
      // Generate ID if not present in newStaff object
      if (!newStaff.id) {
        // Find the maximum existing staff ID
        const maxId = staffMembers.length > 0 
          ? // If staff exist, find maximum ID value
            Math.max(...staffMembers.map(s => s.id)) 
          : // If no staff, start from 0
            0;
        // Assign new sequential ID
        newStaff.id = maxId + 1;
      }

      // Create new array with all existing staff plus the new staff member
      const updatedStaff = [...staffMembers, newStaff];
      // Update staffMembers state with new array
      setStaffMembers(updatedStaff);
      // Update filteredStaff with new array (will be re-filtered by useEffect)
      setFilteredStaff(updatedStaff);
      // Persist updated staff to localStorage
      saveStaffToStorage(updatedStaff);
      // Switch to view-staff tab to show the updated list
      setActiveTab('view-staff');
      
      // Show success popup notification
      setPopup({
        show: true, // Display the popup
        message: 'Staff member added successfully!', // Success message text
        type: 'success' // Success type for green styling
      });
    }
  };

  /**
   * Handler: handleStaffUpdated
   * Processes staff member updates
   * Updates existing staff in list, saves to localStorage, and shows success message
   * @param {Object} updatedStaff - Updated staff member object with same ID
   */
  const handleStaffUpdated = (updatedStaff) => {
    // Map through staffMembers array and update the one being edited
    const updatedList = staffMembers.map(staff => 
      // If this staff matches the one being edited, replace with updatedStaff, otherwise keep original
      staff.id === updatedStaff.id ? updatedStaff : staff
    );
    // Update staffMembers state with modified array
    setStaffMembers(updatedList);
    // Update filteredStaff with modified array
    setFilteredStaff(updatedList);
    // Persist updated staff to localStorage
    saveStaffToStorage(updatedList);
    // Clear editing state (no longer editing)
    setEditingStaff(null);
    // Switch to view-staff tab to show the updated list
    setActiveTab('view-staff');
    
    // Show update popup notification
    setPopup({
      show: true, // Display the popup
      message: 'Staff record updated', // Success message text
      type: 'success' // Success type for green styling
    });
  };

  /**
   * Handler: handleDeleteStaff
   * Processes staff member deletion with permission check
   * Only administrators can delete staff members
   * @param {number} id - ID of staff member to delete
   */
  const handleDeleteStaff = (id) => {
    // Permission check: Only administrators can delete staff members
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to delete staff members.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    
    // Show browser confirmation dialog before deleting
    if (window.confirm('Are you sure you want to delete this staff member?')) {
      // Filter out the staff member with matching ID
      const updatedList = staffMembers.filter(staff => staff.id !== id);
      // Update staffMembers state with filtered array (staff removed)
      setStaffMembers(updatedList);
      // Update filteredStaff with filtered array
      setFilteredStaff(updatedList);
      // Persist updated staff to localStorage
      saveStaffToStorage(updatedList);
      
      // Clear selected staff if the deleted staff was currently selected
      if (selectedStaff && selectedStaff.id === id) {
        setSelectedStaff(null); // Clear selection
      }
      
      // Show delete confirmation popup
      setPopup({
        show: true, // Display the popup
        message: 'Record deleted', // Success message text
        type: 'delete' // Delete type for red styling with trash icon
      });
    }
  };

  /**
   * Handler: handleEditStaff
   * Initiates staff editing mode
   * Only administrators can edit staff members
   * @param {Object} staff - Staff member object to edit
   */
  const handleEditStaff = (staff) => {
    // Permission check: Only administrators can edit staff members
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to edit staff members.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    // Set the staff member being edited in state
    setEditingStaff(staff);
    // Switch to add-staff tab (form will be in edit mode)
    setActiveTab('add-staff');
  };

  /**
   * Handler: handleViewStaff
   * Displays staff details in the details tab
   * @param {Object} staff - Staff member object to view
   */
  const handleViewStaff = (staff) => {
    // Set the staff member to view in state
    setSelectedStaff(staff);
    // Switch to staff-details tab
    setActiveTab('staff-details');
  };

  /**
   * Handler: handleProfilePictureUpload
   * Processes profile picture uploads with validation
   * - Administrators can upload for any staff
   * - Staff can only upload their own profile picture
   * - Validates file type (must be image)
   * - Validates file size (max 5MB)
   * - Converts to base64 data URL for storage
   * @param {Event} e - File input change event
   */
  const handleProfilePictureUpload = (e) => {
    // Get the first file from the file input
    const file = e.target.files[0];
    // Check if file exists and a staff member is selected
    if (file && selectedStaff) {
      // Permission check: Staff users can only upload their own profile picture
      if (isStaff && currentUserProfile && selectedStaff.id !== currentUserProfile.id) {
        // Show error popup if staff user tries to upload someone else's picture
        setPopup({
          show: true, // Display the popup
          message: 'You can only upload your own profile picture.', // Error message text
          type: 'error' // Error type for red styling
        });
        // Exit function early if permission denied
        return;
      }
      
      // Validate file type: must be an image file
      if (!file.type.startsWith('image/')) {
        // Show error popup if file is not an image
        setPopup({
          show: true, // Display the popup
          message: 'Please select a valid image file.', // Error message text
          type: 'error' // Error type for red styling
        });
        // Exit function early if validation fails
        return;
      }
      
      // Validate file size: maximum 5MB
      if (file.size > 5 * 1024 * 1024) {
        // Show error popup if file is too large
        setPopup({
          show: true, // Display the popup
          message: 'Image size should be less than 5MB.', // Error message text
          type: 'error' // Error type for red styling
        });
        // Exit function early if validation fails
        return;
      }

      // Create FileReader to convert file to base64 data URL
      const reader = new FileReader();
      // Callback when file reading is complete
      reader.onloadend = () => {
        // Create updated staff object with new profile picture (base64 data URL)
        const updatedStaff = {
          ...selectedStaff, // Spread existing staff properties
          profilePicture: reader.result // Add/update profilePicture with base64 data
        };
        
        // Update the staff member in the staffMembers array
        const updatedList = staffMembers.map(staff => 
          // If this staff matches the selected one, replace with updatedStaff, otherwise keep original
          staff.id === selectedStaff.id ? updatedStaff : staff
        );
        
        // Update staffMembers state with modified array
        setStaffMembers(updatedList);
        // Update filteredStaff with modified array
        setFilteredStaff(updatedList);
        // Persist updated staff to localStorage
        saveStaffToStorage(updatedList);
        // Update selectedStaff to show new picture immediately
        setSelectedStaff(updatedStaff);
        
        // Note: currentUserProfile will be updated automatically via useEffect when staffMembers changes
        if (isStaff && selectedStaff === currentUserProfile) {
          // currentUserProfile will be updated via useEffect
        }
        
        // Show success popup notification
        setPopup({
          show: true, // Display the popup
          message: 'Profile picture updated successfully!', // Success message text
          type: 'success' // Success type for green styling
        });
      };
      // Start reading file as data URL (base64 encoded string)
      reader.readAsDataURL(file);
    }
  };

  // Return JSX structure for the component
  return (
    // Main container div
    <div className="staff-management">
      {/* Conditional rendering: Show popup message if popup.show is true */}
      {popup.show && (
        // PopupMessage component for displaying notifications
        <PopupMessage
          message={popup.message} // Message text from popup state
          type={popup.type} // Message type (success, error, delete)
          onClose={() => setPopup({ show: false, message: '', type: 'success' })} // Close handler that resets popup state
        />
      )}
      {/* Tab navigation buttons */}
      <div className="staff-tabs">
        {/* View Staff tab button */}
        <button
          className={`tab-button ${activeTab === 'view-staff' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('view-staff')} // Switch to view-staff tab on click
        >
          {/* Button text */}
          View Staff
        </button>
        {/* Conditional rendering: Only show Add Staff tab for administrators */}
        {isAdministrator && (
          // Add Staff tab button (only visible to administrators)
          <button
            className={`tab-button ${activeTab === 'add-staff' ? 'active' : ''}`} // Add 'active' class if this tab is selected
            onClick={() => setActiveTab('add-staff')} // Switch to add-staff tab on click
          >
            {/* Button text */}
            Add Staff
          </button>
        )}
        {/* Staff Details tab button */}
        <button
          className={`tab-button ${activeTab === 'staff-details' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('staff-details')} // Switch to staff-details tab on click
        >
          {/* Conditional button text: 'My Profile' for staff, 'Staff Details' for administrators */}
          {isStaff ? 'My Profile' : 'Staff Details'}
        </button>
      </div>

      {/* Conditional rendering: Show View Staff tab content if that tab is active */}
      {activeTab === 'view-staff' && (
        <div className="view-staff-content">
          {/* Filters section for department and search */}
          <div className="filters-section">
            {/* Department filter group */}
            <div className="filter-group">
              {/* Label for department filter dropdown */}
              <label htmlFor="department-filter">Filter by Department</label>
              {/* Department filter dropdown */}
              <select
                id="department-filter" // ID for label association
                className="filter-select" // CSS class for styling
                value={selectedDepartment} // Current selected value from state
                onChange={(e) => setSelectedDepartment(e.target.value)} // Update state when selection changes
              >
                {/* Map over departments array to create options */}
                {departments.map(dept => (
                  <option key={dept} value={dept}>{dept}</option> // Each department as an option
                ))}
              </select>
            </div>

            {/* Search filter group */}
            <div className="filter-group">
              {/* Label for search input */}
              <label htmlFor="search-staff">Search Staff</label>
              {/* Search text input */}
              <input
                id="search-staff" // ID for label association
                type="text" // Text input type
                className="search-input" // CSS class for styling
                placeholder="Enter name or email" // Placeholder text for guidance
                value={searchQuery} // Current value from state
                onChange={(e) => setSearchQuery(e.target.value)} // Update state on change
              />
            </div>
          </div>

          {/* Heading showing total number of filtered staff members */}
          <h1 className="staff-heading">Staff Members ({filteredStaff.length})</h1>

          {/* Table container with scrollable content */}
          <div className="staff-table-container">
            {/* Main staff table */}
            <table className="staff-table">
              {/* Table header row */}
              <thead>
                <tr>
                  <th>Name</th> {/* Column header for staff name */}
                  <th>Email</th> {/* Column header for email */}
                  <th>Department</th> {/* Column header for department */}
                  <th>Position</th> {/* Column header for position */}
                  <th>Teaching Hours</th> {/* Column header for teaching hours */}
                  <th>Research Hours</th> {/* Column header for research hours */}
                  <th>Total Hours</th> {/* Column header for total hours */}
                  <th>Actions</th> {/* Column header for action buttons */}
                </tr>
              </thead>
              {/* Table body with staff data */}
              <tbody>
                {/* Conditional rendering: Show staff rows if any exist, otherwise show empty message */}
                {filteredStaff.length > 0 ? (
                  // Map over filteredStaff array to create table rows
                  filteredStaff.map(staff => (
                    // Table row for each staff member
                    <tr key={staff.id}>
                      {/* Name cell with avatar and name */}
                      <td>
                        <div className="staff-name-cell">
                          {/* Conditional rendering: Show profile picture if exists, otherwise show placeholder */}
                          {staff.profilePicture ? (
                            // Profile picture image
                            <img src={staff.profilePicture} alt={staff.name} className="staff-avatar" />
                          ) : (
                            // Avatar placeholder with first letter of name
                            <div className="staff-avatar-placeholder">
                              {staff.name.charAt(0).toUpperCase()} {/* Display first letter in uppercase */}
                            </div>
                          )}
                          {/* Staff name text */}
                          <span>{staff.name}</span>
                        </div>
                      </td>
                      <td>{staff.email}</td> {/* Display email */}
                      <td>{staff.department}</td> {/* Display department */}
                      <td>{staff.position}</td> {/* Display position */}
                      <td>{staff.teachingHours}h</td> {/* Display teaching hours with 'h' suffix */}
                      <td>{staff.researchHours}h</td> {/* Display research hours with 'h' suffix */}
                      <td>{staff.totalHours}h</td> {/* Display total hours with 'h' suffix */}
                      <td>
                        {/* View Staff button - available to all users */}
                        <button 
                          className="action-button view" // CSS class for view button styling
                          onClick={() => handleViewStaff(staff)} // Call handler to view staff details
                        >
                          {/* Button text */}
                          View Staff
                        </button>
                        {/* Conditional rendering: Only show Edit/Delete buttons for administrators */}
                        {isAdministrator && (
                          <>
                            {/* Edit button - only for administrators */}
                            <button 
                              className="action-button" // CSS class for edit button styling
                              onClick={() => handleEditStaff(staff)} // Call handler to edit staff
                            >
                              {/* Button text */}
                              Edit
                            </button>
                            {/* Delete button - only for administrators */}
                            <button 
                              className="action-button delete" // CSS class for delete button styling
                              onClick={() => handleDeleteStaff(staff.id)} // Call handler to delete staff
                            >
                              {/* Button text */}
                              Delete
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))
                ) : (
                  // Empty state row when no staff found
                  <tr>
                    {/* Cell spanning all 8 columns with empty message */}
                    <td colSpan="8" className="no-data">No staff members found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Conditional rendering: Show Add Staff form if that tab is active AND user is administrator */}
      {activeTab === 'add-staff' && isAdministrator && (
        // AddStaffForm component for adding/editing staff
        <AddStaffForm 
          onStaffAdded={handleStaffAdded} // Callback when new staff is added
          onStaffUpdated={handleStaffUpdated} // Callback when staff is updated
          editingStaff={editingStaff} // Staff object being edited (null for new staff)
        />
      )}
      {/* Conditional rendering: Show permission denied message if staff user tries to access add-staff tab */}
      {activeTab === 'add-staff' && !isAdministrator && (
        <div className="view-staff-content">
          {/* Permission denied message */}
          <p className="info-message">You do not have permission to add or edit staff members.</p>
        </div>
      )}

      {/* Conditional rendering: Show Staff Details tab content if that tab is active */}
      {activeTab === 'staff-details' && (
        <div className="staff-details-content">
          {/* Section heading (conditional text based on user role) */}
          <h1 className="staff-heading">{isStaff ? 'My Profile' : 'Staff Details'}</h1>
          {/* Conditional rendering: Show staff details if a staff member is selected, otherwise show message */}
          {selectedStaff ? (
            // Details grid container
            <div className="details-grid">
              {/* Detail card container */}
              <div className="detail-card">
                {/* Staff detail header with avatar and upload button */}
                <div className="staff-detail-header">
                  {/* Conditional rendering: Show profile picture if exists, otherwise show placeholder */}
                  {selectedStaff.profilePicture ? (
                    // Profile picture image
                    <img src={selectedStaff.profilePicture} alt={selectedStaff.name} className="staff-detail-avatar" />
                  ) : (
                    // Avatar placeholder with first letter of name
                    <div className="staff-detail-avatar-placeholder">
                      {selectedStaff.name.charAt(0).toUpperCase()} {/* Display first letter in uppercase */}
                    </div>
                  )}
                  {/* Staff name as card title */}
                  <h3 className="detail-card-title">{selectedStaff.name}</h3>
                  {/* Conditional rendering: Show upload button only for administrators or staff viewing their own profile */}
                  {(isAdministrator || isOwnProfile) && (
                    <div className="profile-upload-section">
                      {/* Hidden file input for profile picture upload */}
                      <input
                        type="file" // File input type
                        id="profilePictureUpload" // ID for button click trigger
                        accept="image/*" // Accept only image files
                        onChange={handleProfilePictureUpload} // Call handler when file is selected
                        className="file-input-hidden" // CSS class to hide the input
                      />
                      {/* Upload button that triggers file input click */}
                      <button
                        type="button" // Button type (not submit)
                        onClick={() => document.getElementById('profilePictureUpload').click()} // Trigger file input click
                        className="upload-profile-button" // CSS class for styling
                      >
                        {/* Button text */}
                        Upload Profile Pic
                      </button>
                    </div>
                  )}
                </div>
                <div className="detail-card-content">
                  <div className="detail-item">
                    <span className="detail-label">Staff ID:</span>
                    <span className="detail-value">{selectedStaff.staffId || `STAFF${selectedStaff.id.toString().padStart(3, '0')}`}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Email:</span>
                    <span className="detail-value">{selectedStaff.email}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Department:</span>
                    <span className="detail-value">{selectedStaff.department}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Position:</span>
                    <span className="detail-value">{selectedStaff.position}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Qualifications:</span>
                    <span className="detail-value">{selectedStaff.qualifications || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Teaching Hours:</span>
                    <span className="detail-value">{selectedStaff.teachingHours}h</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Research Hours:</span>
                    <span className="detail-value">{selectedStaff.researchHours}h</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Total Hours:</span>
                    <span className="detail-value">{selectedStaff.totalHours}h</span>
                  </div>
                  {selectedStaff.minContactHoursYear && (
                    <div className="detail-item">
                      <span className="detail-label">Min Contact Hours/Year:</span>
                      <span className="detail-value">{selectedStaff.minContactHoursYear}h</span>
                    </div>
                  )}
                  {selectedStaff.minContactHoursWeek && (
                    <div className="detail-item">
                      <span className="detail-label">Min Contact Hours/Week:</span>
                      <span className="detail-value">{selectedStaff.minContactHoursWeek}h</span>
                    </div>
                  )}
                  {selectedStaff.maxHoursWeek && (
                    <div className="detail-item">
                      <span className="detail-label">Max Hours/Week:</span>
                      <span className="detail-value">{selectedStaff.maxHoursWeek}h</span>
                    </div>
                  )}
                  {selectedStaff.minHoursWeek && (
                    <div className="detail-item">
                      <span className="detail-label">Min Hours/Week:</span>
                      <span className="detail-value">{selectedStaff.minHoursWeek}h</span>
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

