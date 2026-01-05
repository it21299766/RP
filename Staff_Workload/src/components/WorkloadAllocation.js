/**
 * WorkloadAllocation Component
 * 
 * This component handles workload allocation configuration and results display.
 * It provides a form to configure allocation parameters and displays allocation results.
 * 
 * Features:
 * - Semester selection for allocation
 * - Department filtering (optional)
 * - Allocation execution
 * - Results display (placeholder for future implementation)
 * - Tab-based navigation (Run Allocation, Allocation Results)
 * 
 * Current Status:
 * - UI is implemented
 * - Allocation logic is not yet implemented (TODO)
 * - Results display is a placeholder
 * 
 * Future Implementation:
 * - Connect to backend allocation algorithm
 * - Display detailed allocation results
 * - Allow export of allocation data
 * 
 * Dependencies:
 * - None (standalone component)
 */
// Import React and useState hook for state management
import React, { useState } from 'react';
// Import CSS styles for this component
import './WorkloadAllocation.css';

// Component function (no props needed)
const WorkloadAllocation = () => {
  // State: Tracks which tab is currently active ('run-allocation' or 'allocation-results')
  const [activeTab, setActiveTab] = useState('run-allocation');
  // State: Stores form input values for allocation configuration
  const [formData, setFormData] = useState({
    semester: 'Fall 2024', // Selected semester (default value)
    department: 'All' // Selected department filter (default to 'All')
  });

  // Array of available semester options for dropdown
  const semesters = ['Semester 1', 'Semester 2'];
  
  /**
   * Function: getDepartments
   * Retrieves unique departments from staff and courses in localStorage
   * Falls back to default departments if localStorage is unavailable
   * @returns {Array} - Array of department names with 'All' as first option
   */
  const getDepartments = () => {
    try {
      // Retrieve staff members from localStorage, default to empty array if not found
      const staffMembers = JSON.parse(localStorage.getItem('staffMembers') || '[]');
      // Retrieve courses from localStorage, default to empty array if not found
      const courses = JSON.parse(localStorage.getItem('courses') || '[]');
      // Use Set to automatically handle uniqueness
      const departments = new Set();
      
      // Iterate through staff members and add their departments to Set
      staffMembers.forEach(staff => {
        // Only add if department exists
        if (staff.department) departments.add(staff.department);
      });
      
      // Iterate through courses and add their departments to Set
      courses.forEach(course => {
        // Only add if department exists
        if (course.department) departments.add(course.department);
      });
      
      // Convert Set to sorted array
      const deptArray = Array.from(departments).sort();
      // Return array with 'All' option first, followed by sorted departments
      return ['All', ...deptArray];
    } catch (error) {
      // If error occurs (e.g., localStorage unavailable), return default departments
      return ['All', 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology'];
    }
  };

  // Get departments list by calling the function
  const departments = getDepartments();

  /**
   * Handler: handleInputChange
   * Updates form data when input fields change
   * @param {string} field - Field name to update
   * @param {any} value - New value for the field
   */
  const handleInputChange = (field, value) => {
    // Update formData state, preserving existing fields and updating specified field
    setFormData(prev => ({
      ...prev, // Spread existing form data
      [field]: value // Update the specified field with new value (computed property name)
    }));
  };

  /**
   * Handler: handleRunAllocation
   * Processes allocation execution (placeholder - logic not yet implemented)
   * Currently just logs data and switches to results tab
   */
  const handleRunAllocation = () => {
    // TODO: Implement allocation logic
    // Log allocation parameters to console for debugging
    console.log('Running allocation with:', formData);
    // Switch to results tab to show allocation results
    setActiveTab('allocation-results');
  };

  // Return JSX structure for the component
  return (
    // Main container div
    <div className="workload-allocation">
      {/* Header section with title and refresh button */}
      <div className="allocation-header">
        {/* Left side of header */}
        <div className="allocation-header-left">
          {/* Main page title */}
          <h1 className="allocation-title">Workload Allocation</h1>
        </div>
        {/* Right side of header */}
        <div className="allocation-header-right">
          {/* Refresh button (placeholder - functionality not implemented) */}
          <button className="refresh-button" title="Refresh">
            {/* Refresh icon emoji */}
            <span className="refresh-icon">🔄</span>
          </button>
        </div>
      </div>

      {/* Tab navigation buttons */}
      <div className="allocation-tabs">
        {/* Run Allocation tab button */}
        <button
          className={`allocation-tab-button ${activeTab === 'run-allocation' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('run-allocation')} // Switch to run-allocation tab on click
        >
          {/* Button text */}
          Run Allocation
        </button>
        {/* Allocation Results tab button */}
        <button
          className={`allocation-tab-button ${activeTab === 'allocation-results' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('allocation-results')} // Switch to allocation-results tab on click
        >
          {/* Button text */}
          Allocation Results
        </button>
      </div>

      {/* Conditional rendering: Show Run Allocation form if that tab is active */}
      {activeTab === 'run-allocation' && (
        <div className="run-allocation-content">
          {/* Configuration section */}
          <div className="configure-allocation-section">
            {/* Section title */}
            <h2 className="section-title">Configure Allocation</h2>
            
            {/* Form for allocation configuration */}
            <form className="allocation-form" onSubmit={(e) => { e.preventDefault(); handleRunAllocation(); }}>
              {/* Form row containing input fields */}
              <div className="form-row">
                {/* Semester selection group */}
                <div className="form-group">
                  {/* Label for semester dropdown */}
                  <label htmlFor="semester">
                    Semester <span className="required">*</span> {/* Required field indicator */}
                  </label>
                  {/* Semester dropdown select */}
                  <select
                    id="semester" // ID for label association
                    className="form-select" // CSS class for styling
                    value={formData.semester} // Current selected value from state
                    onChange={(e) => handleInputChange('semester', e.target.value)} // Update state on change
                    required // HTML5 required attribute
                  >
                    {/* Map over semesters array to create options */}
                    {semesters.map(sem => (
                      <option key={sem} value={sem}>{sem}</option> // Each semester as an option
                    ))}
                  </select>
                </div>

                {/* Department selection group */}
                <div className="form-group">
                  {/* Label for department dropdown */}
                  <label htmlFor="department">
                    Department (Optional) {/* Optional field indicator */}
                  </label>
                  {/* Department dropdown select */}
                  <select
                    id="department" // ID for label association
                    className="form-select" // CSS class for styling
                    value={formData.department} // Current selected value from state
                    onChange={(e) => handleInputChange('department', e.target.value)} // Update state on change
                  >
                    {/* Map over departments array to create options */}
                    {departments.map(dept => (
                      <option key={dept} value={dept}>{dept}</option> // Each department as an option
                    ))}
                  </select>
                </div>
              </div>

              {/* Form action buttons */}
              <div className="form-actions">
                {/* Submit button to run allocation */}
                <button type="submit" className="run-allocation-button">
                  {/* Button text */}
                  Run Allocation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Conditional rendering: Show Allocation Results if that tab is active */}
      {activeTab === 'allocation-results' && (
        <div className="allocation-results-content">
          {/* Section title */}
          <h2 className="section-title">Allocation Results</h2>
          {/* Placeholder container for results */}
          <div className="results-placeholder">
            {/* Info message (conditional based on form data) */}
            <p className="info-message">
              {/* If semester and department are set, show specific message */}
              {formData.semester && formData.department
                ? `Allocation results for ${formData.semester}${formData.department !== 'All' ? ` - ${formData.department}` : ''} will appear here.` // Include department name if not 'All'
                : 'Run an allocation to see results here.'} {/* Default message if no data */}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

// Export component as default for use in other files
export default WorkloadAllocation;

