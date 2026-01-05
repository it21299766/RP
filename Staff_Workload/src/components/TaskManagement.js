/**
 * TaskManagement Component
 * 
 * This component manages tasks in the system with role-based access control.
 * It provides functionality to view, add, edit, and delete tasks.
 * 
 * Features:
 * - Role-based access control (Administrators can add/edit/delete, Staff can only view)
 * - Task details viewing
 * - Task categorization (general, academic, administrative, research, teaching, assessment)
 * - LocalStorage persistence for task data
 * - Tab-based navigation (View Tasks, Add Task, Task Details)
 * - Auto-generated task IDs
 * - Dynamic department list from staff and courses
 * 
 * Props:
 * - userRole: String - 'Administrator' or 'Staff' (default: 'Administrator')
 * 
 * Role Permissions:
 * - Administrator: Full access (add, edit, delete, view all tasks)
 * - Staff: View-only access (cannot add, edit, or delete tasks)
 * 
 * Data Persistence:
 * - Task data is stored in localStorage under key 'tasks'
 * - Automatically loads saved data on component mount
 * - Saves data after any create, update, or delete operation
 * 
 * Dependencies:
 * - PopupMessage: Component for displaying success/error messages
 */
// Import React hooks for state management and side effects
import React, { useState, useEffect } from 'react';
// Import CSS styles for this component
import './TaskManagement.css';
// Import PopupMessage component for displaying notifications
import PopupMessage from './PopupMessage';

// Component function that receives props via destructuring with default value
const TaskManagement = ({ userRole = 'Administrator' }) => {
  /**
   * State: activeTab
   * Controls which tab is currently displayed
   * Values: 'view-tasks', 'add-task', 'task-details'
   */
  // Initialize activeTab state to 'view-tasks' (default tab)
  const [activeTab, setActiveTab] = useState('view-tasks');
  
  /**
   * State: tasks
   * Array of all task objects in the system
   * Each object contains: id, taskId, taskName, description, category, etc.
   */
  // Initialize tasks state as empty array
  const [tasks, setTasks] = useState([]);
  
  /**
   * State: filteredTasks
   * Array of tasks after applying filters (currently shows all tasks)
   * Updated automatically when tasks change
   */
  // Initialize filteredTasks state as empty array
  const [filteredTasks, setFilteredTasks] = useState([]);
  
  /**
   * State: editingTask
   * Stores the task object being edited (null if not editing)
   * When set, the form switches to edit mode
   */
  // Initialize editingTask state as null (no task being edited initially)
  const [editingTask, setEditingTask] = useState(null);
  
  /**
   * State: popup
   * Controls popup message display
   * Object with: { show: boolean, message: string, type: 'success'|'error'|'delete' }
   */
  // Initialize popup state with show: false (hidden by default)
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  
  /**
   * State: selectedTask
   * Stores the task currently being viewed in the details tab
   */
  // Initialize selectedTask state as null (no task selected initially)
  const [selectedTask, setSelectedTask] = useState(null);
  
  /**
   * Computed: isAdministrator
   * Boolean indicating if current user has Administrator role
   */
  // Check if userRole is 'Administrator'
  const isAdministrator = userRole === 'Administrator';
  
  /**
   * Computed: isStaff
   * Boolean indicating if current user has Staff role
   */
  // Check if userRole is 'Staff'
  const isStaff = userRole === 'Staff';
  
  /**
   * State: formData
   * Stores form input values for adding/editing tasks
   * Contains all task fields: taskId, taskName, description, category, etc.
   */
  // Initialize formData state with default values
  const [formData, setFormData] = useState({
    taskId: 'T001', // Auto-generated task ID (format: T001, T002, etc.)
    taskName: '', // Task name input (required)
    description: '', // Task description input (required)
    category: 'general', // Task category (default: 'general')
    hoursNeeded: '', // Number of hours needed for task (required)
    noOfStaff: '', // Number of staff required (required)
    staffQualificationCriteria: '', // Qualification requirements (required)
    department: '', // Department assignment (required)
    programme: '', // Programme assignment (required)
    module: '' // Module assignment (required)
  });

  /**
   * Function: generateTaskId
   * Generates a new sequential task ID in format T001, T002, T003, etc.
   * Extracts numeric part from existing task IDs and increments by 1
   * @returns {string} - New task ID (e.g., 'T001', 'T002')
   */
  const generateTaskId = () => {
    // Find the maximum task ID number from existing tasks
    const maxId = tasks.length > 0 
      ? // If tasks exist, find the maximum numeric ID
        Math.max(...tasks.map(t => {
          // Extract numeric part from taskId using regex (e.g., 'T001' -> '001')
          const match = t.taskId?.match(/\d+/);
          // Convert to integer if match found, otherwise return 0
          return match ? parseInt(match[0]) : 0;
        }))
      : // If no tasks exist, start from 0
        0;
    // Generate new ID: 'T' + padded number (e.g., 'T001', 'T002')
    return `T${String(maxId + 1).padStart(3, '0')}`;
  };

  /**
   * useEffect: Load Tasks Data
   * Runs once on component mount to load task data from localStorage.
   * If no saved data exists, initializes with sample data.
   * This ensures data persistence across page refreshes.
   */
  useEffect(() => {
    // Inner function to load task data
    const loadTasksData = () => {
      // Retrieve saved task data from browser's localStorage
      const savedTasks = localStorage.getItem('tasks');
      // Check if saved data exists
      if (savedTasks) {
        // Parse JSON string back into JavaScript array
        const parsedTasks = JSON.parse(savedTasks);
        // Update tasks state with loaded data
        setTasks(parsedTasks);
        // Initialize filteredTasks with all loaded tasks (no filter applied yet)
        setFilteredTasks(parsedTasks);
      } else {
        // If no saved data, create initial sample data for demonstration
        const sampleData = [
          {
            id: 1,
            taskId: 'T001',
            taskName: 'Review Course Materials',
            description: 'Review and update course materials for CS101',
            category: 'academic',
            hoursNeeded: '40',
            noOfStaff: '2',
            staffQualificationCriteria: 'PhD in Computer Science, 5+ years teaching experience',
            department: 'Computer Science',
            programme: 'Bachelor of Science',
            module: 'Module 1'
          },
          {
            id: 2,
            taskId: 'T002',
            taskName: 'Prepare Exam Questions',
            description: 'Create final exam questions for MATH101',
            category: 'assessment',
            hoursNeeded: '20',
            noOfStaff: '1',
            staffQualificationCriteria: 'PhD in Mathematics',
            department: 'Mathematics',
            programme: 'Bachelor of Science',
            module: 'Module 2'
          },
          {
            id: 3,
            taskId: 'T003',
            taskName: 'Update Syllabus',
            description: 'Update syllabus for Spring 2024 semester',
            category: 'administrative',
            hoursNeeded: '15',
            noOfStaff: '1',
            staffQualificationCriteria: 'Senior lecturer or above',
            department: 'Computer Science',
            programme: 'Master of Science',
            module: 'Module 3'
          }
        ];
        // Update tasks state with sample data
        setTasks(sampleData);
        // Initialize filteredTasks with sample data
        setFilteredTasks(sampleData);
        // Save sample data to localStorage for persistence
        localStorage.setItem('tasks', JSON.stringify(sampleData));
      }
    };

    // Call the load function when component mounts
    loadTasksData();
  }, []); // Empty dependency array means this runs only once on mount

  /**
   * useEffect: Auto-update Task ID
   * Updates the task ID in formData when tasks list changes (new task added)
   * Only updates if not currently editing a task (to preserve existing task ID)
   */
  useEffect(() => {
    // Only update task ID if not currently editing a task
    if (!editingTask) {
      // Generate new sequential task ID
      const newTaskId = generateTaskId();
      // Update formData with new task ID (preserve other form fields)
      setFormData(prev => ({
        ...prev, // Spread existing form data
        taskId: newTaskId // Update taskId field
      }));
    }
  }, [tasks.length, editingTask]); // Re-run when tasks count or editingTask changes

  /**
   * useEffect: Update Filtered Tasks
   * Automatically updates filteredTasks when tasks list changes
   * Currently shows all tasks (no filtering logic implemented)
   */
  useEffect(() => {
    // Set filtered tasks to all tasks (no filtering applied currently)
    setFilteredTasks(tasks);
  }, [tasks]); // Re-run when tasks array changes

  /**
   * Function: getDepartments
   * Dynamically retrieves department list from staff and courses in localStorage
   * Falls back to default departments if no data exists or error occurs
   * @returns {Array} - Sorted array of unique department names
   */
  const getDepartments = () => {
    try {
      // Retrieve staff members from localStorage (default to empty array if not found)
      const staffMembers = JSON.parse(localStorage.getItem('staffMembers') || '[]');
      // Retrieve courses from localStorage (default to empty array if not found)
      const courses = JSON.parse(localStorage.getItem('courses') || '[]');
      // Use Set to store unique department names
      const departments = new Set();
      
      // Extract departments from staff members
      staffMembers.forEach(staff => {
        // Add department to Set if it exists
        if (staff.department) departments.add(staff.department);
      });
      
      // Extract departments from courses
      courses.forEach(course => {
        // Add department to Set if it exists
        if (course.department) departments.add(course.department);
      });
      
      // Convert Set to sorted array
      const deptArray = Array.from(departments).sort();
      // Return departments if found, otherwise return default list
      return deptArray.length > 0 ? deptArray : ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology'];
    } catch (error) {
      // Return default departments if any error occurs (e.g., invalid JSON)
      return ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology'];
    }
  };

  /**
   * Computed: departments
   * Array of available departments for task assignment
   * Dynamically loaded from staff and courses data
   */
  // Get departments by calling the function
  const departments = getDepartments();
  
  /**
   * Constant: programmes
   * Array of available academic programmes for task assignment
   */
  // List of academic programmes
  const programmes = ['Bachelor of Science', 'Bachelor of Arts', 'Master of Science', 'Master of Arts', 'PhD', 'Diploma'];
  
  /**
   * Constant: modules
   * Array of available modules for task assignment
   */
  // List of module options
  const modules = ['Module 1', 'Module 2', 'Module 3', 'Module 4', 'Module 5', 'Module 6'];
  
  /**
   * Constant: categories
   * Array of available task categories
   */
  // List of task categories
  const categories = ['general', 'academic', 'administrative', 'research', 'teaching', 'assessment'];

  /**
   * Function: saveTasksToStorage
   * Persists task data to localStorage
   * Called after any create, update, or delete operation
   * @param {Array} tasksList - Array of task objects to save
   */
  const saveTasksToStorage = (tasksList) => {
    // Convert array to JSON string and save to localStorage
    localStorage.setItem('tasks', JSON.stringify(tasksList));
  };

  /**
   * Handler: handleTaskAdded
   * Processes new task creation
   * Validates required fields, generates ID, adds to list, saves to localStorage, and shows success message
   */
  const handleTaskAdded = () => {
    // Validate required fields (taskName and description must not be empty)
    if (!formData.taskName.trim() || !formData.description.trim()) {
      // Show error popup if validation fails
      setPopup({
        show: true, // Display the popup
        message: 'Please fill in all required fields.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if validation fails
      return;
    }

    // Find the maximum existing task ID
    const maxId = tasks.length > 0 
      ? // If tasks exist, find maximum ID value
        Math.max(...tasks.map(t => t.id)) 
      : // If no tasks, start from 0
        0;
    
    // Create new task object
    const newTask = {
      id: maxId + 1, // Assign new sequential ID
      ...formData, // Spread all form data fields
      taskId: formData.taskId || generateTaskId() // Use existing taskId or generate new one
    };

    // Create new array with all existing tasks plus the new task
    const updatedTasks = [...tasks, newTask];
    // Update tasks state with new array
    setTasks(updatedTasks);
    // Update filteredTasks with new array
    setFilteredTasks(updatedTasks);
    // Persist updated tasks to localStorage
    saveTasksToStorage(updatedTasks);
    // Switch to view-tasks tab to show the updated list
    setActiveTab('view-tasks');
    
    // Reset form to default values
    setFormData({
      taskId: generateTaskId(), // Generate new task ID for next task
      taskName: '', // Clear task name
      description: '', // Clear description
      category: 'general', // Reset to default category
      hoursNeeded: '', // Clear hours needed
      noOfStaff: '', // Clear number of staff
      staffQualificationCriteria: '', // Clear qualification criteria
      department: '', // Clear department
      programme: '', // Clear programme
      module: '' // Clear module
    });
    
    // Show success popup notification
    setPopup({
      show: true, // Display the popup
      message: 'Task added successfully!', // Success message text
      type: 'success' // Success type for green styling
    });
  };

  /**
   * Handler: handleTaskUpdated
   * Processes task updates
   * Validates required fields, updates existing task in list, saves to localStorage, and shows success message
   */
  const handleTaskUpdated = () => {
    // Validate required fields (taskName and description must not be empty)
    if (!formData.taskName.trim() || !formData.description.trim()) {
      // Show error popup if validation fails
      setPopup({
        show: true, // Display the popup
        message: 'Please fill in all required fields.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if validation fails
      return;
    }

    // Map through tasks array and update the one being edited
    const updatedList = tasks.map(task => 
      // If this task matches the one being edited, replace with updated formData, otherwise keep original
      task.id === editingTask.id ? { ...task, ...formData } : task
    );
    // Update tasks state with modified array
    setTasks(updatedList);
    // Update filteredTasks with modified array
    setFilteredTasks(updatedList);
    // Persist updated tasks to localStorage
    saveTasksToStorage(updatedList);
    // Clear editing state (no longer editing)
    setEditingTask(null);
    // Switch to view-tasks tab to show the updated list
    setActiveTab('view-tasks');
    
    // Reset form to default values
    setFormData({
      taskId: generateTaskId(), // Generate new task ID for next task
      taskName: '', // Clear task name
      description: '', // Clear description
      category: 'general', // Reset to default category
      hoursNeeded: '', // Clear hours needed
      noOfStaff: '', // Clear number of staff
      staffQualificationCriteria: '', // Clear qualification criteria
      department: '', // Clear department
      programme: '', // Clear programme
      module: '' // Clear module
    });
    
    // Show update success popup notification
    setPopup({
      show: true, // Display the popup
      message: 'Task updated successfully!', // Success message text
      type: 'success' // Success type for green styling
    });
  };

  /**
   * Handler: handleDeleteTask
   * Processes task deletion with permission check
   * Only administrators can delete tasks
   * @param {number} id - ID of task to delete
   */
  const handleDeleteTask = (id) => {
    // Permission check: Only administrators can delete tasks
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to delete tasks.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    
    // Show browser confirmation dialog before deleting
    if (window.confirm('Are you sure you want to delete this task?')) {
      // Filter out the task with matching ID
      const updatedList = tasks.filter(task => task.id !== id);
      // Update tasks state with filtered array (task removed)
      setTasks(updatedList);
      // Update filteredTasks with filtered array
      setFilteredTasks(updatedList);
      // Persist updated tasks to localStorage
      saveTasksToStorage(updatedList);
      
      // Clear selected task if the deleted task was currently selected
      if (selectedTask && selectedTask.id === id) {
        setSelectedTask(null); // Clear selection
      }
      
      // Show delete confirmation popup
      setPopup({
        show: true, // Display the popup
        message: 'Task deleted successfully!', // Success message text
        type: 'delete' // Delete type for red styling with trash icon
      });
    }
  };

  /**
   * Handler: handleEditTask
   * Initiates task editing mode
   * Only administrators can edit tasks
   * @param {Object} task - Task object to edit
   */
  const handleEditTask = (task) => {
    // Permission check: Only administrators can edit tasks
    if (!isAdministrator) {
      // Show error popup if user lacks permission
      setPopup({
        show: true, // Display the popup
        message: 'You do not have permission to edit tasks.', // Error message text
        type: 'error' // Error type for red styling
      });
      // Exit function early if permission denied
      return;
    }
    
    // Set the task being edited in state
    setEditingTask(task);
    // Populate form with task data (use existing values or defaults)
    setFormData({
      taskId: task.taskId || generateTaskId(), // Use existing taskId or generate new
      taskName: task.taskName || '', // Use existing taskName or empty string
      description: task.description || '', // Use existing description or empty string
      category: task.category || 'general', // Use existing category or 'general'
      hoursNeeded: task.hoursNeeded || '', // Use existing hoursNeeded or empty string
      noOfStaff: task.noOfStaff || '', // Use existing noOfStaff or empty string
      staffQualificationCriteria: task.staffQualificationCriteria || '', // Use existing criteria or empty string
      department: task.department || '', // Use existing department or empty string
      programme: task.programme || '', // Use existing programme or empty string
      module: task.module || '' // Use existing module or empty string
    });
    // Switch to add-task tab (form will be in edit mode)
    setActiveTab('add-task');
  };

  /**
   * Handler: handleInputChange
   * Updates formData state when form input fields change
   * @param {string} field - Field name to update
   * @param {any} value - New value for the field
   */
  const handleInputChange = (field, value) => {
    // Update formData state with new value for specified field
    setFormData(prev => ({
      ...prev, // Spread existing form data
      [field]: value // Update the specified field with new value (computed property name)
    }));
  };

  /**
   * Handler: handleSubmit
   * Processes form submission
   * Determines whether to create new task or update existing based on editingTask state
   * @param {Event} e - Form submit event
   */
  const handleSubmit = (e) => {
    // Prevent default form submission behavior (page refresh)
    e.preventDefault();
    // Check if currently editing a task
    if (editingTask) {
      // Call update handler if editing
      handleTaskUpdated();
    } else {
      // Call create handler if adding new task
      handleTaskAdded();
    }
  };

  /**
   * Handler: handleCancel
   * Cancels form editing/adding
   * Clears editing state, resets form, and switches to view-tasks tab
   */
  const handleCancel = () => {
    // Clear editing state
    setEditingTask(null);
    // Reset form to default values
    setFormData({
      taskId: generateTaskId(), // Generate new task ID
      taskName: '', // Clear task name
      description: '', // Clear description
      category: 'general', // Reset to default category
      hoursNeeded: '', // Clear hours needed
      noOfStaff: '', // Clear number of staff
      staffQualificationCriteria: '', // Clear qualification criteria
      department: '', // Clear department
      programme: '', // Clear programme
      module: '' // Clear module
    });
    // Switch to view-tasks tab
    setActiveTab('view-tasks');
  };

  /**
   * Handler: handleViewTask
   * Displays task details in the details tab
   * @param {Object} task - Task object to view
   */
  const handleViewTask = (task) => {
    // Set the task to view in state
    setSelectedTask(task);
    // Switch to task-details tab
    setActiveTab('task-details');
  };


  // Return JSX structure for the component
  return (
    // Main container div
    <div className="task-management">
      {/* Conditional rendering: Show popup message if popup.show is true */}
      {popup.show && (
        // PopupMessage component for displaying notifications
        <PopupMessage
          message={popup.message} // Message text from popup state
          type={popup.type} // Message type (success, error, delete)
          onClose={() => setPopup({ show: false, message: '', type: 'success' })} // Close handler that resets popup state
        />
      )}
      
      {/* Task header section with icon, title, and action buttons */}
      <div className="task-header">
        {/* Left side of header */}
        <div className="task-header-left">
          {/* Task icon emoji */}
          <span className="task-icon">✅</span>
          {/* Page title */}
          <h1 className="task-title">Task Management</h1>
        </div>
        {/* Right side of header */}
        <div className="task-header-right">
          {/* Deploy button (functionality not implemented) */}
          <button className="deploy-button">Deploy</button>
          {/* Menu button (functionality not implemented) */}
          <button className="menu-button">⋮</button>
        </div>
      </div>

      {/* Tab navigation buttons */}
      <div className="task-tabs">
        {/* View Tasks tab button */}
        <button
          className={`tab-button ${activeTab === 'view-tasks' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('view-tasks')} // Switch to view-tasks tab on click
        >
          {/* Button text */}
          View Tasks
        </button>
        {/* Conditional rendering: Only show Add Task tab for administrators */}
        {isAdministrator && (
          // Add Task tab button (only visible to administrators)
          <button
            className={`tab-button ${activeTab === 'add-task' ? 'active' : ''}`} // Add 'active' class if this tab is selected
            onClick={() => setActiveTab('add-task')} // Switch to add-task tab on click
          >
            {/* Button text */}
            Add Task
          </button>
        )}
        {/* Task Details tab button */}
        <button
          className={`tab-button ${activeTab === 'task-details' ? 'active' : ''}`} // Add 'active' class if this tab is selected
          onClick={() => setActiveTab('task-details')} // Switch to task-details tab on click
        >
          {/* Button text */}
          Task Details
        </button>
      </div>

      {/* Conditional rendering: Show View Tasks tab content if that tab is active */}
      {activeTab === 'view-tasks' && (
        <div className="view-tasks-content">
          {/* Heading showing total number of tasks */}
          <h2 className="tasks-heading">Tasks ({filteredTasks.length})</h2>

          {/* Table container with scrollable content */}
          <div className="tasks-table-container">
            {/* Main tasks table */}
            <table className="tasks-table">
              {/* Table header row */}
              <thead>
                <tr>
                  <th>Task ID</th> {/* Column header for task ID */}
                  <th>Task Name</th> {/* Column header for task name */}
                  <th>Category</th> {/* Column header for category */}
                  <th>Hours Needed</th> {/* Column header for hours needed */}
                  <th>No. of Staff</th> {/* Column header for number of staff */}
                  <th>Department</th> {/* Column header for department */}
                  <th>Actions</th> {/* Column header for action buttons */}
                </tr>
              </thead>
              {/* Table body with task data */}
              <tbody>
                {/* Conditional rendering: Show task rows if any exist, otherwise show empty message */}
                {filteredTasks.length > 0 ? (
                  // Map over filteredTasks array to create table rows
                  filteredTasks.map(task => (
                    // Table row for each task
                    <tr key={task.id}>
                      <td>{task.taskId}</td> {/* Display task ID */}
                      <td>{task.taskName}</td> {/* Display task name */}
                      <td>
                        {/* Category badge with capitalized category name */}
                        <span className="category-badge">
                          {/* Capitalize first letter of category, or show 'N/A' if no category */}
                          {task.category ? task.category.charAt(0).toUpperCase() + task.category.slice(1) : 'N/A'}
                        </span>
                      </td>
                      <td>{task.hoursNeeded || 'N/A'}</td> {/* Display hours needed or 'N/A' */}
                      <td>{task.noOfStaff || 'N/A'}</td> {/* Display number of staff or 'N/A' */}
                      <td>{task.department || 'N/A'}</td> {/* Display department or 'N/A' */}
                      <td>
                        {/* View Task button - available to all users */}
                        <button 
                          className="action-button view" // CSS class for view button styling
                          onClick={() => handleViewTask(task)} // Call handler to view task details
                        >
                          {/* Button text */}
                          View Task
                        </button>
                        {/* Conditional rendering: Only show Edit/Delete buttons for administrators */}
                        {isAdministrator && (
                          <>
                            {/* Edit button - only for administrators */}
                            <button 
                              className="action-button" // CSS class for edit button styling
                              onClick={() => handleEditTask(task)} // Call handler to edit task
                            >
                              {/* Button text */}
                              Edit
                            </button>
                            {/* Delete button - only for administrators */}
                            <button 
                              className="action-button delete" // CSS class for delete button styling
                              onClick={() => handleDeleteTask(task.id)} // Call handler to delete task
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
                  // Empty state row when no tasks found
                  <tr>
                    {/* Cell spanning all 7 columns with empty message */}
                    <td colSpan="7" className="no-data">No tasks found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Conditional rendering: Show Add Task form if that tab is active AND user is administrator */}
      {activeTab === 'add-task' && isAdministrator && (
        <div className="add-task-content">
          {/* Form heading (conditional text based on edit mode) */}
          <h2 className="task-form-heading">{editingTask ? 'Edit Task' : 'Add New Task'}</h2>
          {/* Form container */}
          <div className="form-container">
            {/* Main form element */}
            <form className="task-form" onSubmit={handleSubmit}>
              {/* Two-column form layout */}
              <div className="form-columns">
                {/* Left column */}
                <div className="form-column">
                  {/* Task ID input group */}
                  <div className="form-group">
                    {/* Label for task ID input */}
                    <label htmlFor="taskId">
                      Task ID <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Task ID text input */}
                    <input
                      type="text" // Text input type
                      id="taskId" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.taskId} // Current value from state
                      onChange={(e) => handleInputChange('taskId', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    />
                  </div>

                  {/* Task Name input group */}
                  <div className="form-group">
                    {/* Label for task name input */}
                    <label htmlFor="taskName">
                      Task Name <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Task name text input */}
                    <input
                      type="text" // Text input type
                      id="taskName" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.taskName} // Current value from state
                      onChange={(e) => handleInputChange('taskName', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="e.g., Review Course Materials" // Placeholder text for guidance
                    />
                  </div>

                  {/* Task Description input group */}
                  <div className="form-group">
                    {/* Label for description textarea */}
                    <label htmlFor="description">
                      Task Description <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Description textarea */}
                    <textarea
                      id="description" // ID for label association
                      className="form-input form-textarea" // CSS class for styling
                      value={formData.description} // Current value from state
                      onChange={(e) => handleInputChange('description', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="Enter task description" // Placeholder text for guidance
                      rows="4" // Number of visible rows
                    />
                  </div>

                  {/* Task Category input group */}
                  <div className="form-group">
                    {/* Label for category dropdown */}
                    <label htmlFor="category">
                      Task Category <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Category dropdown select */}
                    <select
                      id="category" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.category} // Current selected value from state
                      onChange={(e) => handleInputChange('category', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    >
                      {/* Map over categories array to create options */}
                      {categories.map(cat => (
                        // Option for each category (capitalize first letter)
                        <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
                      ))}
                    </select>
                  </div>

                  {/* Hours Needed input group */}
                  <div className="form-group">
                    {/* Label for hours needed input */}
                    <label htmlFor="hoursNeeded">
                      Hours Needed <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Hours needed number input */}
                    <input
                      type="number" // Number input type
                      id="hoursNeeded" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.hoursNeeded} // Current value from state
                      onChange={(e) => handleInputChange('hoursNeeded', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      min="1" // Minimum value allowed
                      placeholder="e.g., 40" // Placeholder text for guidance
                    />
                  </div>
                </div>

                {/* Right column */}
                <div className="form-column">
                  {/* Number of Staff input group */}
                  <div className="form-group">
                    {/* Label for number of staff input */}
                    <label htmlFor="noOfStaff">
                      No. of Staff <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Number of staff number input */}
                    <input
                      type="number" // Number input type
                      id="noOfStaff" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.noOfStaff} // Current value from state
                      onChange={(e) => handleInputChange('noOfStaff', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      min="1" // Minimum value allowed
                      placeholder="e.g., 2" // Placeholder text for guidance
                    />
                  </div>

                  {/* Staff Qualification Criteria input group */}
                  <div className="form-group">
                    {/* Label for qualification criteria textarea */}
                    <label htmlFor="staffQualificationCriteria">
                      Staff Qualification Criteria <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Qualification criteria textarea */}
                    <textarea
                      id="staffQualificationCriteria" // ID for label association
                      className="form-input form-textarea" // CSS class for styling
                      value={formData.staffQualificationCriteria} // Current value from state
                      onChange={(e) => handleInputChange('staffQualificationCriteria', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                      placeholder="e.g., PhD in Computer Science, 5+ years teaching experience" // Placeholder text for guidance
                      rows="3" // Number of visible rows
                    />
                  </div>

                  {/* Department input group */}
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
                      {/* Default option (empty selection) */}
                      <option value="">Select Department</option>
                      {/* Map over departments array to create options */}
                      {departments.map(dept => (
                        // Option for each department
                        <option key={dept} value={dept}>{dept}</option>
                      ))}
                    </select>
                  </div>

                  {/* Programme input group */}
                  <div className="form-group">
                    {/* Label for programme dropdown */}
                    <label htmlFor="programme">
                      Programme <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Programme dropdown select */}
                    <select
                      id="programme" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.programme} // Current selected value from state
                      onChange={(e) => handleInputChange('programme', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    >
                      {/* Default option (empty selection) */}
                      <option value="">Select Programme</option>
                      {/* Map over programmes array to create options */}
                      {programmes.map(prog => (
                        // Option for each programme
                        <option key={prog} value={prog}>{prog}</option>
                      ))}
                    </select>
                  </div>

                  {/* Module input group */}
                  <div className="form-group">
                    {/* Label for module dropdown */}
                    <label htmlFor="module">
                      Module <span className="required">*</span> {/* Required field indicator */}
                    </label>
                    {/* Module dropdown select */}
                    <select
                      id="module" // ID for label association
                      className="form-input" // CSS class for styling
                      value={formData.module} // Current selected value from state
                      onChange={(e) => handleInputChange('module', e.target.value)} // Update state on change
                      required // HTML5 required attribute
                    >
                      {/* Default option (empty selection) */}
                      <option value="">Select Module</option>
                      {/* Map over modules array to create options */}
                      {modules.map(mod => (
                        // Option for each module
                        <option key={mod} value={mod}>{mod}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* Form action buttons */}
              <div className="form-actions">
                {/* Submit button (conditional text based on edit mode) */}
                <button 
                  type="submit" // Submit button type
                  className="submit-button" // CSS class for styling
                >
                  {/* Conditional button text: 'Update Task' if editing, 'Add Task' if adding */}
                  {editingTask ? 'Update Task' : 'Add Task'}
                </button>
                {/* Cancel button */}
                <button 
                  type="button" // Button type (not submit)
                  className="cancel-button" // CSS class for styling
                  onClick={handleCancel} // Call handler to cancel form
                >
                  {/* Button text */}
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {/* Conditional rendering: Show permission denied message if staff user tries to access add-task tab */}
      {activeTab === 'add-task' && !isAdministrator && (
        <div className="view-tasks-content">
          {/* Permission denied message */}
          <p className="info-message">You do not have permission to add or edit tasks.</p>
        </div>
      )}

      {/* Conditional rendering: Show Task Details tab content if that tab is active */}
      {activeTab === 'task-details' && (
        <div className="task-details-content">
          {/* Section heading */}
          <h2 className="task-form-heading">Task Details</h2>
          {/* Conditional rendering: Show task details if a task is selected, otherwise show message */}
          {selectedTask ? (
            // Details grid container
            <div className="details-grid">
              {/* Detail card container */}
              <div className="detail-card">
                {/* Task name as card title */}
                <h3 className="detail-card-title">{selectedTask.taskName}</h3>
                {/* Detail card content */}
                <div className="detail-card-content">
                  {/* Task ID detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Task ID:</span>
                    <span className="detail-value">{selectedTask.taskId}</span>
                  </div>
                  {/* Description detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Description:</span>
                    <span className="detail-value">{selectedTask.description}</span>
                  </div>
                  {/* Category detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Category:</span>
                    {/* Capitalize first letter of category, or show 'N/A' if no category */}
                    <span className="detail-value">{selectedTask.category ? selectedTask.category.charAt(0).toUpperCase() + selectedTask.category.slice(1) : 'N/A'}</span>
                  </div>
                  {/* Hours Needed detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Hours Needed:</span>
                    <span className="detail-value">{selectedTask.hoursNeeded || 'N/A'}</span>
                  </div>
                  {/* Number of Staff detail item */}
                  <div className="detail-item">
                    <span className="detail-label">No. of Staff:</span>
                    <span className="detail-value">{selectedTask.noOfStaff || 'N/A'}</span>
                  </div>
                  {/* Staff Qualification Criteria detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Staff Qualification Criteria:</span>
                    <span className="detail-value">{selectedTask.staffQualificationCriteria || 'N/A'}</span>
                  </div>
                  {/* Department detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Department:</span>
                    <span className="detail-value">{selectedTask.department || 'N/A'}</span>
                  </div>
                  {/* Programme detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Programme:</span>
                    <span className="detail-value">{selectedTask.programme || 'N/A'}</span>
                  </div>
                  {/* Module detail item */}
                  <div className="detail-item">
                    <span className="detail-label">Module:</span>
                    <span className="detail-value">{selectedTask.module || 'N/A'}</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            // Empty state message when no task is selected
            <p className="info-message">Click "View Task" on a task from the View Tasks tab to see its details here.</p>
          )}
        </div>
      )}
    </div>
  );
};

// Export component as default for use in other files
export default TaskManagement;

