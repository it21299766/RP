/**
 * ReportFiltersModal Component
 * 
 * This component provides a modal dialog for configuring report generation parameters.
 * Users can select filters, domains, include options, and display format before generating a report.
 * 
 * Features:
 * - Semester selection (required)
 * - Program and program section filtering (optional)
 * - Staff selection (optional)
 * - Domain selection checkboxes (Teaching, Research, Admin, Exams, Service)
 * - Include options checkboxes (Preparation Hours, Marking Hours, Research Hours, Admin Hours)
 * - Display format selection (Table, Chart, or Table + Chart)
 * - Form validation
 * - Modal overlay with click-outside-to-close functionality
 * 
 * Props:
 * - reportId: String - ID of the report type being configured
 * - initialFilters: Object - Initial filter values to populate the form
 * - onGenerate: Function - Callback called when "Generate Report" is clicked, receives filters object
 * - onClose: Function - Callback called when modal is closed
 * 
 * Filter Structure:
 * - semester: String (required)
 * - program: String (optional)
 * - programSection: String (optional)
 * - staff: String (optional)
 * - domains: Object with boolean flags for each domain
 * - include: Object with boolean flags for each include option
 * - displayFormat: String - 'table', 'chart', or 'table+chart'
 * 
 * Dependencies:
 * - None (standalone modal component)
 */
// Import React and useState hook for state management
import React, { useState } from 'react';
// Import CSS styles for this component
import './ReportFiltersModal.css';

// Component function that receives props via destructuring
const ReportFiltersModal = ({ reportId, initialFilters, onGenerate, onClose }) => {
  /**
   * State: filters
   * Stores all filter configuration values for report generation
   * Initialized with values from initialFilters prop or defaults
   */
  const [filters, setFilters] = useState({
    semester: initialFilters.semester || '', // Selected semester (required field, default empty)
    program: initialFilters.program || '', // Selected program (optional, default empty)
    programSection: initialFilters.programSection || '', // Selected program section (optional, default empty)
    staff: '', // Selected staff member (optional, default empty)
    // Domain selection flags - all default to true (all domains selected by default)
    domains: {
      teaching: true, // Teaching domain checkbox state
      research: true, // Research domain checkbox state
      admin: true, // Admin domain checkbox state
      exams: true, // Exams domain checkbox state
      service: true // Service domain checkbox state
    },
    // Include options flags - all default to true (all options included by default)
    include: {
      preparationHours: true, // Preparation hours checkbox state
      markingHours: true, // Marking hours checkbox state
      researchHours: true, // Research hours checkbox state
      adminHours: true // Admin hours checkbox state
    },
    displayFormat: 'table' // Display format selection (default: 'table')
  });

  /**
   * Handler: handleInputChange
   * Updates filter state when input fields change
   * Handles both simple fields and nested object fields (e.g., 'domains.teaching')
   * @param {string} field - Field name to update (can be nested like 'domains.teaching')
   * @param {any} value - New value for the field
   */
  const handleInputChange = (field, value) => {
    // Check if field name contains a dot (indicating nested object property)
    if (field.includes('.')) {
      // Split field name into parent and child (e.g., 'domains.teaching' -> ['domains', 'teaching'])
      const [parent, child] = field.split('.');
      // Update nested object property
      setFilters(prev => ({
        ...prev, // Spread existing filters
        [parent]: { // Update the parent object
          ...prev[parent], // Spread existing parent object properties
          [child]: value // Update the specific child property with new value
        }
      }));
    } else {
      // Update simple (non-nested) field
      setFilters(prev => ({
        ...prev, // Spread existing filters
        [field]: value // Update the specified field with new value (computed property name)
      }));
    }
  };

  /**
   * Handler: handleDomainToggle
   * Toggles a domain checkbox on/off
   * @param {string} domain - Domain name to toggle ('teaching', 'research', 'admin', 'exams', 'service')
   */
  const handleDomainToggle = (domain) => {
    // Update filters state, toggling the specified domain
    setFilters(prev => ({
      ...prev, // Spread existing filters
      domains: { // Update domains object
        ...prev.domains, // Spread existing domain states
        [domain]: !prev.domains[domain] // Toggle the specified domain (true -> false, false -> true)
      }
    }));
  };

  /**
   * Handler: handleIncludeToggle
   * Toggles an include option checkbox on/off
   * @param {string} include - Include option name to toggle ('preparationHours', 'markingHours', etc.)
   */
  const handleIncludeToggle = (include) => {
    // Update filters state, toggling the specified include option
    setFilters(prev => ({
      ...prev, // Spread existing filters
      include: { // Update include object
        ...prev.include, // Spread existing include option states
        [include]: !prev.include[include] // Toggle the specified include option (true -> false, false -> true)
      }
    }));
  };

  /**
   * Handler: handleSubmit
   * Processes form submission
   * Validates required fields and calls onGenerate callback with filter data
   * @param {Event} e - Form submit event
   */
  const handleSubmit = (e) => {
    // Prevent default form submission behavior (page refresh)
    e.preventDefault();
    // Validate that semester is selected (required field)
    if (!filters.semester) {
      // Show browser alert if semester is not selected
      alert('Please select a semester');
      // Exit function early if validation fails
      return;
    }
    // Call onGenerate callback with current filter values
    onGenerate(filters);
  };

  // Return JSX structure for the modal
  return (
    // Modal overlay - dark background that closes modal when clicked
    <div className="modal-overlay" onClick={onClose}>
      {/* Modal content container - stops click propagation to prevent closing when clicking inside */}
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal header with title and close button */}
        <div className="modal-header">
          {/* Modal title */}
          <h2 className="modal-title">Report Parameters</h2>
          {/* Close button (X) */}
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        {/* Main form for filter configuration */}
        <form className="modal-form" onSubmit={handleSubmit}>
          {/* Basic Filters section */}
          <div className="form-section">
            {/* Section title */}
            <h3 className="section-title">Basic Filters</h3>
            
            {/* Semester selection group */}
            <div className="form-group">
              {/* Label for semester dropdown */}
              <label htmlFor="semester">
                Semester <span className="required">*</span> {/* Required field indicator */}
              </label>
              {/* Semester dropdown select */}
              <select
                id="semester" // ID for label association
                className="form-input" // CSS class for styling
                value={filters.semester} // Current selected value from state
                onChange={(e) => handleInputChange('semester', e.target.value)} // Update state on change
                required // HTML5 required attribute
              >
                {/* Default option (empty selection) */}
                <option value="">Select Semester</option>
                {/* Semester 1 option */}
                <option value="Semester 1">Semester 1</option>
                {/* Semester 2 option */}
                <option value="Semester 2">Semester 2</option>
              </select>
            </div>

            {/* Program selection group */}
            <div className="form-group">
              {/* Label for program dropdown */}
              <label htmlFor="program">Program (Optional)</label> {/* Optional field indicator */}
              {/* Program dropdown select */}
              <select
                id="program" // ID for label association
                className="form-input" // CSS class for styling
                value={filters.program} // Current selected value from state
                onChange={(e) => handleInputChange('program', e.target.value)} // Update state on change
              >
                {/* Default option (all programs) */}
                <option value="">All Programs</option>
                {/* Computer Science option */}
                <option value="CS">Computer Science</option>
                {/* Mathematics option */}
                <option value="MATH">Mathematics</option>
              </select>
            </div>

            {/* Program Section selection group */}
            <div className="form-group">
              {/* Label for program section dropdown */}
              <label htmlFor="program-section">Program Section (Optional)</label> {/* Optional field indicator */}
              {/* Program section dropdown select */}
              <select
                id="program-section" // ID for label association
                className="form-input" // CSS class for styling
                value={filters.programSection} // Current selected value from state
                onChange={(e) => handleInputChange('programSection', e.target.value)} // Update state on change
              >
                {/* Default option (all sections) */}
                <option value="">All Sections</option>
                {/* Section A option */}
                <option value="A">Section A</option>
                {/* Section B option */}
                <option value="B">Section B</option>
              </select>
            </div>

            {/* Staff selection group */}
            <div className="form-group">
              {/* Label for staff dropdown */}
              <label htmlFor="staff">Staff (Optional)</label> {/* Optional field indicator */}
              {/* Staff dropdown select */}
              <select
                id="staff" // ID for label association
                className="form-input" // CSS class for styling
                value={filters.staff} // Current selected value from state
                onChange={(e) => handleInputChange('staff', e.target.value)} // Update state on change
              >
                {/* Default option (all staff) */}
                <option value="">All Staff</option>
                {/* Dr. John Smith option */}
                <option value="1">Dr. John Smith</option>
                {/* Dr. Sarah Johnson option */}
                <option value="2">Dr. Sarah Johnson</option>
              </select>
            </div>
          </div>

          {/* Select Domains section */}
          <div className="form-section">
            {/* Section title */}
            <h3 className="section-title">Select Domains</h3>
            {/* Checkbox group container */}
            <div className="checkbox-group">
              {/* Map over domains object to create checkboxes for each domain */}
              {Object.entries(filters.domains).map(([domain, checked]) => (
                // Label wrapping checkbox for each domain
                <label key={domain} className="checkbox-label">
                  {/* Checkbox input */}
                  <input
                    type="checkbox" // Checkbox input type
                    checked={checked} // Checked state from filters.domains[domain]
                    onChange={() => handleDomainToggle(domain)} // Toggle domain on change
                  />
                  {/* Checkbox label text (capitalize first letter) */}
                  <span className="checkbox-text">
                    {domain.charAt(0).toUpperCase() + domain.slice(1)} {/* Capitalize first letter of domain name */}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Include section */}
          <div className="form-section">
            {/* Section title */}
            <h3 className="section-title">Include</h3>
            {/* Checkbox group container */}
            <div className="checkbox-group">
              {/* Preparation Hours checkbox */}
              <label className="checkbox-label">
                {/* Checkbox input */}
                <input
                  type="checkbox" // Checkbox input type
                  checked={filters.include.preparationHours} // Checked state from filters.include.preparationHours
                  onChange={() => handleIncludeToggle('preparationHours')} // Toggle preparationHours on change
                />
                {/* Checkbox label text */}
                <span className="checkbox-text">Preparation Hours</span>
              </label>
              {/* Marking Hours checkbox */}
              <label className="checkbox-label">
                {/* Checkbox input */}
                <input
                  type="checkbox" // Checkbox input type
                  checked={filters.include.markingHours} // Checked state from filters.include.markingHours
                  onChange={() => handleIncludeToggle('markingHours')} // Toggle markingHours on change
                />
                {/* Checkbox label text */}
                <span className="checkbox-text">Marking Hours</span>
              </label>
              {/* Research Hours checkbox */}
              <label className="checkbox-label">
                {/* Checkbox input */}
                <input
                  type="checkbox" // Checkbox input type
                  checked={filters.include.researchHours} // Checked state from filters.include.researchHours
                  onChange={() => handleIncludeToggle('researchHours')} // Toggle researchHours on change
                />
                {/* Checkbox label text */}
                <span className="checkbox-text">Research Hours</span>
              </label>
              {/* Admin Hours checkbox */}
              <label className="checkbox-label">
                {/* Checkbox input */}
                <input
                  type="checkbox" // Checkbox input type
                  checked={filters.include.adminHours} // Checked state from filters.include.adminHours
                  onChange={() => handleIncludeToggle('adminHours')} // Toggle adminHours on change
                />
                {/* Checkbox label text */}
                <span className="checkbox-text">Admin Hours</span>
              </label>
            </div>
          </div>

          {/* Display Format section */}
          <div className="form-section">
            {/* Section title */}
            <h3 className="section-title">Display Format</h3>
            {/* Radio button group container */}
            <div className="radio-group">
              {/* Table format radio option */}
              <label className="radio-label">
                {/* Radio input */}
                <input
                  type="radio" // Radio button input type
                  name="displayFormat" // Group name (all radios in same group)
                  value="table" // Value for this option
                  checked={filters.displayFormat === 'table'} // Checked if displayFormat is 'table'
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)} // Update state on change
                />
                {/* Radio label text */}
                <span className="radio-text">Table</span>
              </label>
              {/* Chart format radio option */}
              <label className="radio-label">
                {/* Radio input */}
                <input
                  type="radio" // Radio button input type
                  name="displayFormat" // Group name (all radios in same group)
                  value="chart" // Value for this option
                  checked={filters.displayFormat === 'chart'} // Checked if displayFormat is 'chart'
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)} // Update state on change
                />
                {/* Radio label text */}
                <span className="radio-text">Chart</span>
              </label>
              {/* Table + Chart format radio option */}
              <label className="radio-label">
                {/* Radio input */}
                <input
                  type="radio" // Radio button input type
                  name="displayFormat" // Group name (all radios in same group)
                  value="table+chart" // Value for this option
                  checked={filters.displayFormat === 'table+chart'} // Checked if displayFormat is 'table+chart'
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)} // Update state on change
                />
                {/* Radio label text */}
                <span className="radio-text">Table + Chart</span>
              </label>
            </div>
          </div>

          {/* Modal action buttons section */}
          <div className="modal-actions">
            {/* Cancel button */}
            <button type="button" className="btn-cancel" onClick={onClose}>
              {/* Button text */}
              Cancel
            </button>
            {/* Generate Report submit button */}
            <button type="submit" className="btn-generate">
              {/* Button text */}
              Generate Report
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Export component as default for use in other files
export default ReportFiltersModal;

