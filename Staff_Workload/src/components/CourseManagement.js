/**
 * CourseManagement Component
 * 
 * This component manages courses in the system with role-based access control.
 * It provides functionality to view, add, edit, and delete courses.
 * 
 * Features:
 * - Role-based access control (Administrators can add/edit/delete, Staff can only view)
 * - Course filtering by semester
 * - Course details viewing
 * - LocalStorage persistence for course data
 * - Tab-based navigation (View Courses, Add Course, Course Details)
 * - Auto-generated course IDs
 * 
 * Props:
 * - userRole: String - 'Administrator' or 'Staff' (default: 'Administrator')
 * 
 * Role Permissions:
 * - Administrator: Full access (add, edit, delete, view all courses)
 * - Staff: View-only access (cannot add, edit, or delete courses)
 * 
 * Data Persistence:
 * - Course data is stored in localStorage under key 'courses'
 * - Automatically loads saved data on component mount
 * - Saves data after any create, update, or delete operation
 * 
 * Dependencies:
 * - PopupMessage: Component for displaying success/error messages
 */
// Import React hooks for state management and side effects
import React, { useState, useEffect } from 'react';
// Import CSS styles for this component
import './CourseManagement.css';
// Import PopupMessage component for displaying notifications
import PopupMessage from './PopupMessage';

// Main component function - receives userRole prop with default value 'Administrator'
const CourseManagement = ({ userRole = 'Administrator' }) => {
  // State: Tracks which tab is currently active ('view-courses', 'add-course', 'course-details')
  const [activeTab, setActiveTab] = useState('view-courses');
  // State: Stores the selected semester filter value ('All' shows all semesters)
  const [selectedSemester, setSelectedSemester] = useState('All');
  // State: Array storing all course objects in the system
  const [courses, setCourses] = useState([]);
  // State: Array storing filtered courses based on selected filters
  const [filteredCourses, setFilteredCourses] = useState([]);
  // State: Stores the course object being edited (null when not editing)
  const [editingCourse, setEditingCourse] = useState(null);
  // State: Controls popup message display - object with show flag, message text, and type
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  // State: Stores the course object currently being viewed in details tab
  const [selectedCourse, setSelectedCourse] = useState(null);
  
  // Computed: Boolean indicating if current user has Administrator role
  const isAdministrator = userRole === 'Administrator';
  // Computed: Boolean indicating if current user has Staff role
  const isStaff = userRole === 'Staff';
  // State: Object storing form input values for adding/editing courses
  const [formData, setFormData] = useState({
    courseId: 'COURSE001', // Auto-generated course identifier
    courseCode: '', // Course code (e.g., 'CS101')
    courseName: '', // Full course name
    department: 'Faculty of Computing', // Default department selection
    credits: 3, // Number of credits for the course
    contactHoursWeek: 3.00, // Contact hours per week (decimal)
    canCombineSections: false, // Boolean flag for section combination
    courseType: 'lecture', // Type of course (lecture, lab, seminar, workshop)
    requiredQualification: '', // Prerequisite course code
    semester: 'Semester 1', // Semester offering
    expectedEnrollment: 50, // Expected number of students
    maxStudentsSection: 50, // Maximum students per section
    priority: 5 // Priority level (1-10 scale)
  });

  /**
   * Function: generateCourseId
   * Generates a unique course ID by finding the highest existing ID and incrementing
   * @returns {string} - New course ID in format 'COURSE001', 'COURSE002', etc.
   */
  const generateCourseId = () => {
    // Check if courses array has items, otherwise default to 0
    const maxId = courses.length > 0 
      ? // If courses exist, find the maximum ID number
        Math.max(...courses.map(c => {
          // Extract numeric part from courseId using regex (e.g., 'COURSE001' -> '001')
          const match = c.courseId?.match(/\d+/);
          // Convert matched string to integer, or 0 if no match
          return match ? parseInt(match[0]) : 0;
        }))
      : // If no courses exist, start from 0
        0;
    // Generate new ID: increment maxId, pad with zeros to 3 digits, prefix with 'COURSE'
    return `COURSE${String(maxId + 1).padStart(3, '0')}`;
  };

  /**
   * useEffect: Load Courses Data
   * Runs once on component mount to load saved courses from localStorage
   * If no saved data exists, initializes with sample data
   */
  useEffect(() => {
    // Inner function to load course data
    const loadCoursesData = () => {
      // Retrieve saved courses from browser's localStorage
      const savedCourses = localStorage.getItem('courses');
      // Check if saved data exists
      if (savedCourses) {
        // Parse JSON string back into JavaScript array
        const parsedCourses = JSON.parse(savedCourses);
        // Update courses state with loaded data
        setCourses(parsedCourses);
        // Initialize filtered courses with all courses (no filter applied yet)
        setFilteredCourses(parsedCourses);
      } else {
        // If no saved data, create initial sample data for demonstration
        const sampleData = [
          {
            id: 1,
            courseCode: 'CS101',
            courseName: 'Introduction to Computer Science',
            department: 'Computer Science',
            semester: 'Semester 1',
            credits: 3,
            contactHours: 3,
            description: 'Fundamental concepts of computer science'
          },
          {
            id: 2,
            courseCode: 'CS201',
            courseName: 'Data Structures',
            department: 'Computer Science',
            semester: 'Semester 2',
            credits: 4,
            contactHours: 4,
            description: 'Introduction to data structures and algorithms'
          },
          {
            id: 3,
            courseCode: 'MATH101',
            courseName: 'Calculus I',
            department: 'Mathematics',
            semester: 'Semester 1',
            credits: 4,
            contactHours: 4,
            description: 'Differential and integral calculus'
          },
          {
            id: 4,
            courseCode: 'PHYS101',
            courseName: 'Physics I',
            department: 'Physics',
            semester: 'Semester 1',
            credits: 4,
            contactHours: 4,
            description: 'Mechanics and thermodynamics'
          },
          {
            id: 5,
            courseCode: 'CS301',
            courseName: 'Database Systems',
            department: 'Computer Science',
            semester: 'Semester 2',
            credits: 3,
            contactHours: 3,
            description: 'Database design and management'
          },
          {
            id: 6,
            courseCode: 'MATH201',
            courseName: 'Linear Algebra',
            department: 'Mathematics',
            semester: 'Semester 2',
            credits: 3,
            contactHours: 3,
            description: 'Vector spaces and linear transformations'
          },
          {
            id: 7,
            courseCode: 'CS401',
            courseName: 'Software Engineering',
            department: 'Computer Science',
            semester: 'Semester 1',
            credits: 3,
            contactHours: 3,
            description: 'Software development methodologies'
          },
          {
            id: 8,
            courseCode: 'CHEM101',
            courseName: 'General Chemistry',
            department: 'Chemistry',
            semester: 'Semester 1',
            credits: 4,
            contactHours: 4,
            description: 'Fundamental principles of chemistry'
          }
        ];
        // Update courses state with sample data
        setCourses(sampleData);
        // Initialize filtered courses with all sample data
        setFilteredCourses(sampleData);
        // Save sample data to localStorage for persistence
        localStorage.setItem('courses', JSON.stringify(sampleData));
      }
    };

    // Call the load function when component mounts
    loadCoursesData();
  }, []); // Empty dependency array means this runs only once on mount

  /**
   * useEffect: Auto-generate Course ID
   * Updates the course ID in form data when courses list changes (for new courses)
   * Only updates if not currently editing an existing course
   */
  useEffect(() => {
    // Only update ID if not editing (to avoid changing ID of course being edited)
    if (!editingCourse) {
      // Find the maximum existing course ID number
      const maxId = courses.length > 0 
        ? // If courses exist, find max ID
          Math.max(...courses.map(c => {
            // Extract numeric part from courseId using regex
            const match = c.courseId?.match(/\d+/);
            // Convert to integer or default to 0
            return match ? parseInt(match[0]) : 0;
          }))
        : // If no courses, start from 0
          0;
      // Generate new course ID by incrementing max ID and padding with zeros
      const newCourseId = `COURSE${String(maxId + 1).padStart(3, '0')}`;
      // Update form data with new course ID
      setFormData(prev => ({
        ...prev, // Keep existing form data
        courseId: newCourseId // Update only the courseId field
      }));
    }
  }, [courses.length, editingCourse]); // Re-run when courses count or editing state changes

  /**
   * useEffect: Filter Courses
   * Automatically filters courses when semester filter or courses list changes
   */
  useEffect(() => {
    // Start with all courses
    let filtered = courses;

    // If a specific semester is selected (not 'All')
    if (selectedSemester !== 'All') {
      // Filter courses to only include those matching selected semester
      filtered = filtered.filter(course => course.semester === selectedSemester);
    }

    // Update filtered courses state with filtered results
    setFilteredCourses(filtered);
  }, [selectedSemester, courses]); // Re-run when semester filter or courses list changes

  // Array of available semester options for filter dropdown
  const semesters = ['All', 'Semester 1', 'Semester 2'];

  /**
   * Function: saveCoursesToStorage
   * Persists courses array to browser's localStorage
   * @param {Array} coursesList - Array of course objects to save
   */
  const saveCoursesToStorage = (coursesList) => {
    // Convert array to JSON string and save to localStorage
    localStorage.setItem('courses', JSON.stringify(coursesList));
  };

  /**
   * Handler: handleCourseAdded
   * Processes new course creation
   * Validates required fields, generates ID, adds to list, saves, and shows success message
   */
  const handleCourseAdded = () => {
    // Validate required fields: courseCode, courseName, and requiredQualification must not be empty
    if (!formData.courseCode.trim() || !formData.courseName.trim() || !formData.requiredQualification.trim()) {
      // Show error popup if validation fails
      setPopup({
        show: true, // Display the popup
        message: 'Please fill in all required fields.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if validation fails
      return;
    }

    // Find the maximum existing course ID to generate next sequential ID
    const maxId = courses.length > 0 
      ? // If courses exist, find maximum ID value
        Math.max(...courses.map(c => c.id)) 
      : // If no courses, start from 0
        0;
    
    // Create new course object with form data
    const newCourse = {
      id: maxId + 1, // Assign new sequential ID
      ...formData, // Spread all form data fields
      courseId: formData.courseId || generateCourseId() // Use existing courseId or generate new one
    };

    // Create new array with all existing courses plus the new course
    const updatedCourses = [...courses, newCourse];
    // Update courses state with new array
    setCourses(updatedCourses);
    // Update filtered courses (will be re-filtered by useEffect)
    setFilteredCourses(updatedCourses);
    // Persist updated courses to localStorage
    saveCoursesToStorage(updatedCourses);
    // Switch to view-courses tab to show the updated list
    setActiveTab('view-courses');
    
    // Reset form to default values for next entry
    setFormData({
      courseId: generateCourseId(), // Generate new course ID
      courseCode: '', // Clear course code
      courseName: '', // Clear course name
      department: 'Faculty of Computing', // Reset to default department
      credits: 3, // Reset to default credits
      contactHoursWeek: 3.00, // Reset to default contact hours
      canCombineSections: false, // Reset checkbox
      courseType: 'lecture', // Reset to default type
      requiredQualification: '', // Clear qualification
      semester: 'Semester 1', // Reset to default semester
      expectedEnrollment: 50, // Reset to default enrollment
      maxStudentsSection: 50, // Reset to default max students
      priority: 5 // Reset to default priority
    });
    
    // Show success popup notification
    setPopup({
      show: true, // Display the popup
      message: 'Course added successfully!', // Success message text
      type: 'success' // Success type for green styling
    });
  };

  /**
   * Handler: handleCourseUpdated
   * Processes course update/edit operation
   * Validates required fields, updates course in list, saves, and shows success message
   */
  const handleCourseUpdated = () => {
    // Validate required fields: courseCode, courseName, and requiredQualification must not be empty
    if (!formData.courseCode.trim() || !formData.courseName.trim() || !formData.requiredQualification.trim()) {
      // Show error popup if validation fails
      setPopup({
        show: true, // Display the popup
        message: 'Please fill in all required fields.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if validation fails
      return;
    }

    // Map through courses array and update the one being edited
    const updatedList = courses.map(course => 
      // If this course matches the one being edited, merge form data with existing course data
      course.id === editingCourse.id ? { ...course, ...formData } : course
    );
    // Update courses state with modified array
    setCourses(updatedList);
    // Update filtered courses with modified array
    setFilteredCourses(updatedList);
    // Persist updated courses to localStorage
    saveCoursesToStorage(updatedList);
    // Clear editing state (no longer editing)
    setEditingCourse(null);
    // Switch to view-courses tab to show the updated list
    setActiveTab('view-courses');
    
    // Reset form to default values
    setFormData({
      courseId: generateCourseId(), // Generate new course ID for next entry
      courseCode: '', // Clear course code
      courseName: '', // Clear course name
      department: 'Faculty of Computing', // Reset to default department
      credits: 3, // Reset to default credits
      contactHoursWeek: 3.00, // Reset to default contact hours
      canCombineSections: false, // Reset checkbox
      courseType: 'lecture', // Reset to default type
      requiredQualification: '', // Clear qualification
      semester: 'Semester 1', // Reset to default semester
      expectedEnrollment: 50, // Reset to default enrollment
      maxStudentsSection: 50, // Reset to default max students
      priority: 5 // Reset to default priority
    });
    
    // Show success popup notification
    setPopup({
      show: true, // Display the popup
      message: 'Course updated successfully!', // Success message text
      type: 'success' // Success type for green styling
    });
  };

  /**
   * Handler: handleDeleteCourse
   * Processes course deletion with permission check
   * Only administrators can delete courses
   * @param {number} id - ID of course to delete
   */
  const handleDeleteCourse = (id) => {
    // Permission check: Only administrators can delete courses
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to delete courses.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    
    // Show browser confirmation dialog before deleting
    if (window.confirm('Are you sure you want to delete this course?')) {
      // Filter out the course with matching ID
      const updatedList = courses.filter(course => course.id !== id);
      // Update courses state with filtered array (course removed)
      setCourses(updatedList);
      // Update filtered courses with filtered array
      setFilteredCourses(updatedList);
      // Persist updated courses to localStorage
      saveCoursesToStorage(updatedList);
      
      // Clear selected course if the deleted course was currently selected
      if (selectedCourse && selectedCourse.id === id) {
        setSelectedCourse(null); // Clear selection
      }
      
      // Show delete confirmation popup
      setPopup({
        show: true, // Display the popup
        message: 'Course deleted successfully!', // Success message text
        type: 'delete' // Delete type for red styling with trash icon
      });
    }
  };

  /**
   * Handler: handleEditCourse
   * Initiates course editing mode
   * Only administrators can edit courses
   * @param {Object} course - Course object to edit
   */
  const handleEditCourse = (course) => {
    // Permission check: Only administrators can edit courses
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to edit courses.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    
    // Set the course being edited in state
    setEditingCourse(course);
    // Populate form data with existing course values
    setFormData({
      courseId: course.courseId || course.courseCode || generateCourseId(), // Use existing courseId, courseCode, or generate new
      courseCode: course.courseCode || '', // Use existing course code or empty string
      courseName: course.courseName || '', // Use existing course name or empty string
      department: course.department || 'Faculty of Computing', // Use existing department or default
      credits: course.credits || 3, // Use existing credits or default 3
      contactHoursWeek: course.contactHoursWeek || course.contactHours || 3.00, // Use contactHoursWeek, contactHours, or default
      canCombineSections: course.canCombineSections || false, // Use existing value or default false
      courseType: course.courseType || 'lecture', // Use existing type or default 'lecture'
      requiredQualification: course.requiredQualification || '', // Use existing qualification or empty string
      semester: course.semester || 'Semester 1', // Use existing semester or default
      expectedEnrollment: course.expectedEnrollment || 50, // Use existing enrollment or default 50
      maxStudentsSection: course.maxStudentsSection || 50, // Use existing max students or default 50
      priority: course.priority || 5 // Use existing priority or default 5
    });
    // Switch to add-course tab (form will be in edit mode)
    setActiveTab('add-course');
  };

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
   * Handler: handleNumberChange
   * Updates numeric form fields with increment/decrement functionality
   * @param {string} field - Field name to update
   * @param {number} delta - Amount to add/subtract (can be negative)
   */
  const handleNumberChange = (field, delta) => {
    // Update formData with calculated new value
    setFormData(prev => {
      // Get current value as float, default to 0 if not a number
      const currentValue = parseFloat(prev[field]) || 0;
      // Calculate new value, ensure it's not negative (Math.max with 0)
      const newValue = Math.max(0, currentValue + delta);
      // Return updated form data
      return {
        ...prev, // Spread existing form data
        // If field is contactHoursWeek, format to 2 decimal places, otherwise use integer
        [field]: field === 'contactHoursWeek' ? newValue.toFixed(2) : newValue
      };
    });
  };

  /**
   * Handler: handleSubmit
   * Processes form submission
   * Routes to either update or add handler based on editing state
   * @param {Event} e - Form submit event
   */
  const handleSubmit = (e) => {
    // Prevent default form submission (page refresh)
    e.preventDefault();
    // Check if we're editing an existing course
    if (editingCourse) {
      // Call update handler if editing
      handleCourseUpdated();
    } else {
      // Call add handler if creating new course
      handleCourseAdded();
    }
  };

  /**
   * Handler: handleCancel
   * Cancels form editing and resets to default state
   * Returns to view-courses tab
   */
  const handleCancel = () => {
    // Clear editing state (no longer editing)
    setEditingCourse(null);
    // Reset form to default values
    setFormData({
      courseId: generateCourseId(), // Generate new course ID
      courseCode: '', // Clear course code
      courseName: '', // Clear course name
      department: 'Faculty of Computing', // Reset to default department
      credits: 3, // Reset to default credits
      contactHoursWeek: 3.00, // Reset to default contact hours
      canCombineSections: false, // Reset checkbox
      courseType: 'lecture', // Reset to default type
      requiredQualification: '', // Clear qualification
      semester: 'Semester 2', // Reset to default semester
      expectedEnrollment: 50, // Reset to default enrollment
      maxStudentsSection: 50, // Reset to default max students
      priority: 5 // Reset to default priority
    });
    // Switch back to view-courses tab
    setActiveTab('view-courses');
  };

  /**
   * Handler: handleViewCourse
   * Displays course details in the details tab
   * @param {Object} course - Course object to view
   */
  const handleViewCourse = (course) => {
    // Set the course to view in state
    setSelectedCourse(course);
    // Switch to course-details tab
    setActiveTab('course-details');
  };

  // Return JSX structure for the component
  return (
    // Main container div
    <div className="course-management">
      {/* Conditional rendering: Show popup message if popup.show is true */}
      {popup.show && (
        // PopupMessage component for displaying notifications
        <PopupMessage
          message={popup.message} // Message text from popup state
          type={popup.type} // Message type (success, error, delete)
          onClose={() => setPopup({ show: false, message: '', type: 'success' })} // Close handler that resets popup state
        />
      )}
      
      {/* Header section with title and action buttons */}
      <div className="course-header">
        {/* Left side of header */}
        <div className="course-header-left">
          {/* Book emoji icon */}
          <span className="course-icon">📚</span>
          {/* Main page title */}
          <h1 className="course-title">Course Management</h1>
        </div>
        {/* Right side of header */}
        <div className="course-header-right">
          {/* Deploy button (placeholder - functionality not implemented) */}
          <button className="deploy-button">Deploy</button>
          {/* Menu button (placeholder - functionality not implemented) */}
          <button className="menu-button">⋮</button>
        </div>
      </div>

      {/* Tab navigation buttons */}
      <div className="course-tabs">
        {/* View Courses tab button */}
        <button
          className={`tab-button ${activeTab === 'view-courses' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('view-courses')} // Switch to view-courses tab on click
        >
          {/* Button text */}
          View Courses
        </button>
        {/* Conditional rendering: Only show Add Course tab for administrators */}
        {isAdministrator && (
          // Add Course tab button (only visible to administrators)
          <button
            className={`tab-button ${activeTab === 'add-course' ? 'active' : ''}`} // Add 'active' class if this tab is selected
            onClick={() => setActiveTab('add-course')} // Switch to add-course tab on click
          >
            {/* Button text */}
            Add Course
          </button>
        )}
        {/* Course Details tab button */}
        <button
          className={`tab-button ${activeTab === 'course-details' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('course-details')} // Switch to course-details tab on click
        >
          {/* Button text */}
          Course Details
        </button>
      </div>

      {/* Conditional rendering: Show View Courses tab content if that tab is active */}
      {activeTab === 'view-courses' && (
        <div className="view-courses-content">
          {/* Filter section for semester selection */}
          <div className="filter-section">
            {/* Label for semester filter dropdown */}
            <label htmlFor="semester-filter">Filter by Semester</label>
            {/* Semester filter dropdown */}
            <select
              id="semester-filter" // ID for label association
              className="filter-select" // CSS class for styling
              value={selectedSemester} // Current selected value from state
              onChange={(e) => setSelectedSemester(e.target.value)} // Update state when selection changes
            >
              {/* Map over semesters array to create options */}
              {semesters.map(sem => (
                <option key={sem} value={sem}>{sem}</option> // Each semester as an option
              ))}
            </select>
          </div>

          {/* Heading showing total number of filtered courses */}
          <h2 className="courses-heading">Courses ({filteredCourses.length})</h2>

          {/* Table container with scrollable content */}
          <div className="courses-table-container">
            {/* Main courses table */}
            <table className="courses-table">
              {/* Table header row */}
              <thead>
                <tr>
                  <th>Course Code</th> {/* Column header for course code */}
                  <th>Name</th> {/* Column header for course name */}
                  <th>Department</th> {/* Column header for department */}
                  <th>Semester</th> {/* Column header for semester */}
                  <th>Credits</th> {/* Column header for credits */}
                  <th>Contact Hours</th> {/* Column header for contact hours */}
                  <th>Actions</th> {/* Column header for action buttons */}
                </tr>
              </thead>
              {/* Table body with course data */}
              <tbody>
                {/* Conditional rendering: Show courses if any exist, otherwise show empty message */}
                {filteredCourses.length > 0 ? (
                  // Map over filtered courses array to create table rows
                  filteredCourses.map(course => (
                    // Table row for each course
                    <tr key={course.id}>
                      <td>{course.courseCode}</td> {/* Display course code */}
                      <td>{course.courseName}</td> {/* Display course name */}
                      <td>{course.department || 'N/A'}</td> {/* Display department or 'N/A' if missing */}
                      <td>{course.semester}</td> {/* Display semester */}
                      <td>{course.credits}</td> {/* Display credits */}
                      <td>{course.contactHoursWeek || course.contactHours || 'N/A'}</td> {/* Display contact hours or 'N/A' */}
                      <td>
                        {/* View Course button - available to all users */}
                        <button 
                          className="action-button view" // CSS class for view button styling
                          onClick={() => handleViewCourse(course)} // Call handler to view course details
                        >
                          {/* Button text */}
                          View Course
                        </button>
                        {/* Conditional rendering: Only show Edit/Delete buttons for administrators */}
                        {isAdministrator && (
                          <>
                            {/* Edit button - only for administrators */}
                            <button 
                              className="action-button" // CSS class for edit button styling
                              onClick={() => handleEditCourse(course)} // Call handler to edit course
                            >
                              {/* Button text */}
                              Edit
                            </button>
                            {/* Delete button - only for administrators */}
                            <button 
                              className="action-button delete" // CSS class for delete button styling
                              onClick={() => handleDeleteCourse(course.id)} // Call handler to delete course
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
                  // Empty state row when no courses found
                  <tr>
                    {/* Cell spanning all 7 columns with empty message */}
                    <td colSpan="7" className="no-data">No courses found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Conditional rendering: Show Add Course form if that tab is active AND user is administrator */}
      {activeTab === 'add-course' && isAdministrator && (
        <div className="add-course-content">
          {/* Form heading (changes to "Edit Course" when editing) */}
          <h2 className="course-form-heading">{editingCourse ? 'Edit Course' : 'Add New Course'}</h2>
          {/* Form container */}
          <div className="form-container">
            {/* Main form element */}
            <form className="course-form" onSubmit={handleSubmit}>
              {/* Two-column layout for form fields */}
              <div className="form-columns">
                {/* Left column of form fields */}
                <div className="form-column">
                  {/* Course ID input group */}
                  <div className="form-group">
                    {/* Label for course ID input */}
                    <label htmlFor="courseId">
                      Course ID <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Course ID text input */}
                    <input
                      type="text" // Text input type
                      id="courseId" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.courseId} // Current value from state
                      onChange={(e) => handleInputChange('courseId', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    />
                  </div>

                  {/* Course Name input group */}
                  <div className="form-group">
                    {/* Label for course name input */}
                    <label htmlFor="courseName">
                      Course Name <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Course name text input */}
                    <input
                      type="text" // Text input type
                      id="courseName" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.courseName} // Current value from state
                      onChange={(e) => handleInputChange('courseName', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="e.g., Introduction to Computer Science" // Placeholder text for guidance
                    />
                  </div>

                  {/* Department selection group */}
                  <div className="form-group">
                    {/* Label for department dropdown */}
                    <label htmlFor="department">
                      Department <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Department dropdown select */}
                    <select
                      id="department" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.department} // Current selected value from state
                      onChange={(e) => handleInputChange('department', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    >
                      {/* Faculty of Computing option */}
                      <option value="Faculty of Computing">Faculty of Computing</option>
                      {/* Faculty of Business option */}
                      <option value="Faculty of Business">Faculty of Business</option>
                      {/* Faculty of Sciences option */}
                      <option value="Faculty of Sciences">Faculty of Sciences</option>
                      {/* Faculty of Architecture option */}
                      <option value="Faculty of Architecture">Faculty of Architecture</option>
                    </select>
                  </div>

                  {/* Course Code input group */}
                  <div className="form-group">
                    {/* Label for course code input */}
                    <label htmlFor="courseCode">
                      Course Code <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Course code text input */}
                    <input
                      type="text" // Text input type
                      id="courseCode" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.courseCode} // Current value from state
                      onChange={(e) => handleInputChange('courseCode', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="e.g., CS101" // Placeholder text for guidance
                    />
                  </div>

                  {/* Credits input group with increment/decrement buttons */}
                  <div className="form-group">
                    {/* Label for credits input */}
                    <label htmlFor="credits">
                      Credits <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Number input group with +/- buttons */}
                    <div className="number-input-group">
                      {/* Decrement button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('credits', -1)} // Decrease credits by 1
                      >
                        {/* Minus symbol */}
                        -
                      </button>
                      {/* Credits number input */}
                      <input
                        type="number" // Number input type
                        id="credits" // ID for label association
                        className="form-input number-input" // CSS classes for styling
                        value={formData.credits} // Current value from state
                        onChange={(e) => handleInputChange('credits', parseInt(e.target.value) || 0)} // Update state, default to 0 if invalid
                        required // HTML5 required attribute
                        min="1" // Minimum value of 1
                        max="6" // Maximum value of 6
                      />
                      {/* Increment button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('credits', 1)} // Increase credits by 1
                      >
                        {/* Plus symbol */}
                        +
                      </button>
                    </div>
                  </div>

                  {/* Contact Hours/Week input group with increment/decrement buttons */}
                  <div className="form-group">
                    {/* Label for contact hours input */}
                    <label htmlFor="contactHoursWeek">
                      Contact Hours/Week <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Number input group with +/- buttons */}
                    <div className="number-input-group">
                      {/* Decrement button (decreases by 0.5) */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('contactHoursWeek', -0.5)} // Decrease by 0.5 hours
                      >
                        {/* Minus symbol */}
                        -
                      </button>
                      {/* Contact hours number input */}
                      <input
                        type="number" // Number input type
                        id="contactHoursWeek" // ID for label association
                        className="form-input number-input" // CSS classes for styling
                        step="0.5" // Allow 0.5 increments
                        min="0" // Minimum value of 0
                        value={formData.contactHoursWeek} // Current value from state
                        onChange={(e) => handleInputChange('contactHoursWeek', parseFloat(e.target.value) || 0)} // Update state, default to 0 if invalid
                        required // HTML5 required attribute
                      />
                      {/* Increment button (increases by 0.5) */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('contactHoursWeek', 0.5)} // Increase by 0.5 hours
                      >
                        {/* Plus symbol */}
                        +
                      </button>
                    </div>
                  </div>

                  {/* Can Combine Sections checkbox group */}
                  <div className="form-group checkbox-group">
                    {/* Label wrapping checkbox */}
                    <label className="checkbox-label">
                      {/* Checkbox input */}
                      <input
                        type="checkbox" // Checkbox input type
                        checked={formData.canCombineSections} // Checked state from form data
                        onChange={(e) => handleInputChange('canCombineSections', e.target.checked)} // Update state when toggled
                      />
                      {/* Checkbox label text */}
                      <span>Can Combine Sections</span>
                    </label>
                  </div>

                  {/* Course Type selection group */}
                  <div className="form-group">
                    {/* Label for course type dropdown */}
                    <label htmlFor="courseType">Course Type</label>
                    {/* Course type dropdown select */}
                    <select
                      id="courseType" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.courseType} // Current selected value from state
                      onChange={(e) => handleInputChange('courseType', e.target.value)} // Update state on change
                    >
                      {/* Lecture option */}
                      <option value="lecture">Lecture</option>
                      {/* Lab option */}
                      <option value="lab">Lab</option>
                      {/* Seminar option */}
                      <option value="seminar">Seminar</option>
                      {/* Workshop option */}
                      <option value="workshop">Workshop</option>
                    </select>
                  </div>
                </div>

                {/* Right column of form fields */}
                <div className="form-column">
                  {/* Required Qualification input group */}
                  <div className="form-group">
                    {/* Label with help icon */}
                    <label htmlFor="requiredQualification" className="label-with-help">
                      Required Qualification <span className="required">*</span> {/* Required field indicator */}
                      {/* Help icon with tooltip */}
                      <span className="help-icon" title="Enter the prerequisite course code">?</span>
                    </label>
                    {/* Required qualification text input */}
                    <input
                      type="text" // Text input type
                      id="requiredQualification" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.requiredQualification} // Current value from state
                      onChange={(e) => handleInputChange('requiredQualification', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="e.g., CS101" // Placeholder text for guidance
                    />
                  </div>

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
                      value={formData.semester} // Current selected value from state
                      onChange={(e) => handleInputChange('semester', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    >
                      {/* Semester 1 option */}
                      <option value="Semester 1">Semester 1</option>
                      {/* Semester 2 option */}
                      <option value="Semester 2">Semester 2</option>
                    </select>
                  </div>

                  {/* Expected Enrollment input group with increment/decrement buttons */}
                  <div className="form-group">
                    {/* Label for expected enrollment input */}
                    <label htmlFor="expectedEnrollment">
                      Expected Enrollment <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Number input group with +/- buttons */}
                    <div className="number-input-group">
                      {/* Decrement button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('expectedEnrollment', -1)} // Decrease enrollment by 1
                      >
                        {/* Minus symbol */}
                        -
                      </button>
                      {/* Expected enrollment number input */}
                      <input
                        type="number" // Number input type
                        id="expectedEnrollment" // ID for label association
                        className="form-input number-input" // CSS classes for styling
                        value={formData.expectedEnrollment} // Current value from state
                        onChange={(e) => handleInputChange('expectedEnrollment', parseInt(e.target.value) || 0)} // Update state, default to 0 if invalid
                        required // HTML5 required attribute
                        min="1" // Minimum value of 1
                      />
                      {/* Increment button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('expectedEnrollment', 1)} // Increase enrollment by 1
                      >
                        {/* Plus symbol */}
                        +
                      </button>
                    </div>
                  </div>

                  {/* Max Students/Section input group with increment/decrement buttons */}
                  <div className="form-group">
                    {/* Label for max students input */}
                    <label htmlFor="maxStudentsSection">
                      Max Students/Section <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Number input group with +/- buttons */}
                    <div className="number-input-group">
                      {/* Decrement button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('maxStudentsSection', -1)} // Decrease max students by 1
                      >
                        {/* Minus symbol */}
                        -
                      </button>
                      {/* Max students number input */}
                      <input
                        type="number" // Number input type
                        id="maxStudentsSection" // ID for label association
                        className="form-input number-input" // CSS classes for styling
                        value={formData.maxStudentsSection} // Current value from state
                        onChange={(e) => handleInputChange('maxStudentsSection', parseInt(e.target.value) || 0)} // Update state, default to 0 if invalid
                        required // HTML5 required attribute
                        min="1" // Minimum value of 1
                      />
                      {/* Increment button */}
                      <button
                        type="button" // Button type (not submit)
                        className="number-button" // CSS class for styling
                        onClick={() => handleNumberChange('maxStudentsSection', 1)} // Increase max students by 1
                      >
                        {/* Plus symbol */}
                        +
                      </button>
                    </div>
                  </div>

                  {/* Priority slider group */}
                  <div className="form-group">
                    {/* Label with current priority value display */}
                    <label htmlFor="priority">
                      Priority <span className="priority-value">{formData.priority}</span> {/* Display current priority value */}
                    </label>
                    {/* Range slider input for priority */}
                    <input
                      type="range" // Range slider input type
                      id="priority" // ID for label association
                      className="priority-slider" // CSS class for styling
                      min="1" // Minimum value of 1
                      max="10" // Maximum value of 10
                      value={formData.priority} // Current value from state
                      onChange={(e) => handleInputChange('priority', parseInt(e.target.value))} // Update state on change
                    />
                  </div>
                </div>
              </div>

              {/* Form action buttons section */}
              <div className="form-actions">
                {/* Submit button */}
                <button 
                  type="submit" // Submit button type
                  className="submit-button" // CSS class for styling
                >
                  {/* Button text (changes to "Update Course" when editing) */}
                  {editingCourse ? 'Update Course' : 'Add Course'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {/* Conditional rendering: Show permission denied message if staff user tries to access add-course tab */}
      {activeTab === 'add-course' && !isAdministrator && (
        <div className="view-courses-content">
          {/* Permission denied message */}
          <p className="info-message">You do not have permission to add or edit courses.</p>
        </div>
      )}

      {/* Conditional rendering: Show Course Details tab content if that tab is active */}
      {activeTab === 'course-details' && (
        <div className="course-details-content">
          {/* Section heading */}
          <h2 className="course-form-heading">Course Details</h2>
          {/* Conditional rendering: Show course details if a course is selected, otherwise show message */}
          {selectedCourse ? (
            // Details grid container
            <div className="details-grid">
              {/* Detail card container */}
              <div className="detail-card">
                {/* Course name as card title */}
                <h3 className="detail-card-title">{selectedCourse.courseName}</h3>
                {/* Card content container */}
                <div className="detail-card-content">
                  {/* Course ID detail item */}
                  <div className="detail-item">
                    {/* Label for course ID */}
                    <span className="detail-label">Course ID:</span>
                    {/* Value: Use courseId, courseCode, or 'N/A' as fallback */}
                    <span className="detail-value">{selectedCourse.courseId || selectedCourse.courseCode || 'N/A'}</span>
                  </div>
                  {/* Course Code detail item */}
                  <div className="detail-item">
                    {/* Label for course code */}
                    <span className="detail-label">Course Code:</span>
                    {/* Value: Display course code */}
                    <span className="detail-value">{selectedCourse.courseCode}</span>
                  </div>
                  {/* Department detail item */}
                  <div className="detail-item">
                    {/* Label for department */}
                    <span className="detail-label">Department:</span>
                    {/* Value: Display department or 'N/A' if missing */}
                    <span className="detail-value">{selectedCourse.department || 'N/A'}</span>
                  </div>
                  {/* Semester detail item */}
                  <div className="detail-item">
                    {/* Label for semester */}
                    <span className="detail-label">Semester:</span>
                    {/* Value: Display semester */}
                    <span className="detail-value">{selectedCourse.semester}</span>
                  </div>
                  {/* Credits detail item */}
                  <div className="detail-item">
                    {/* Label for credits */}
                    <span className="detail-label">Credits:</span>
                    {/* Value: Display credits */}
                    <span className="detail-value">{selectedCourse.credits}</span>
                  </div>
                  {/* Contact Hours/Week detail item */}
                  <div className="detail-item">
                    {/* Label for contact hours */}
                    <span className="detail-label">Contact Hours/Week:</span>
                    {/* Value: Display contactHoursWeek, contactHours, or 'N/A' as fallback */}
                    <span className="detail-value">{selectedCourse.contactHoursWeek || selectedCourse.contactHours || 'N/A'}</span>
                  </div>
                  {/* Conditional rendering: Show Can Combine Sections only if property exists */}
                  {selectedCourse.canCombineSections !== undefined && (
                    <div className="detail-item">
                      {/* Label for can combine sections */}
                      <span className="detail-label">Can Combine Sections:</span>
                      {/* Value: Display 'Yes' or 'No' based on boolean value */}
                      <span className="detail-value">{selectedCourse.canCombineSections ? 'Yes' : 'No'}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Course Type only if property exists */}
                  {selectedCourse.courseType && (
                    <div className="detail-item">
                      {/* Label for course type */}
                      <span className="detail-label">Course Type:</span>
                      {/* Value: Capitalize first letter of course type */}
                      <span className="detail-value">{selectedCourse.courseType.charAt(0).toUpperCase() + selectedCourse.courseType.slice(1)}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Required Qualification only if property exists */}
                  {selectedCourse.requiredQualification && (
                    <div className="detail-item">
                      {/* Label for required qualification */}
                      <span className="detail-label">Required Qualification:</span>
                      {/* Value: Display required qualification */}
                      <span className="detail-value">{selectedCourse.requiredQualification}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Expected Enrollment only if property exists */}
                  {selectedCourse.expectedEnrollment && (
                    <div className="detail-item">
                      {/* Label for expected enrollment */}
                      <span className="detail-label">Expected Enrollment:</span>
                      {/* Value: Display expected enrollment */}
                      <span className="detail-value">{selectedCourse.expectedEnrollment}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Max Students/Section only if property exists */}
                  {selectedCourse.maxStudentsSection && (
                    <div className="detail-item">
                      {/* Label for max students per section */}
                      <span className="detail-label">Max Students/Section:</span>
                      {/* Value: Display max students per section */}
                      <span className="detail-value">{selectedCourse.maxStudentsSection}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Priority only if property exists */}
                  {selectedCourse.priority !== undefined && (
                    <div className="detail-item">
                      {/* Label for priority */}
                      <span className="detail-label">Priority:</span>
                      {/* Value: Display priority value */}
                      <span className="detail-value">{selectedCourse.priority}</span>
                    </div>
                  )}
                  {/* Conditional rendering: Show Description only if property exists */}
                  {selectedCourse.description && (
                    <div className="detail-item">
                      {/* Label for description */}
                      <span className="detail-label">Description:</span>
                      {/* Value: Display course description */}
                      <span className="detail-value">{selectedCourse.description}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            // Empty state message when no course is selected
            <p className="info-message">Click "View Course" on a course from the View Courses tab to see its details here.</p>
          )}
        </div>
      )}
    </div>
  );
};

// Export component as default for use in other files
export default CourseManagement;

