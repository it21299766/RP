import React, { useState, useEffect } from 'react';
import './CourseManagement.css';
import PopupMessage from './PopupMessage';

const CourseManagement = ({ userRole = 'Administrator' }) => {
  const [activeTab, setActiveTab] = useState('view-courses');
  const [selectedSemester, setSelectedSemester] = useState('All');
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [editingCourse, setEditingCourse] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: 'success' });
  const [selectedCourse, setSelectedCourse] = useState(null);
  
  const isAdministrator = userRole === 'Administrator';
  const isStaff = userRole === 'Staff';
  const [formData, setFormData] = useState({
    courseId: 'COURSE001',
    courseCode: '',
    courseName: '',
    department: 'Faculty of Computing',
    credits: 3,
    contactHoursWeek: 3.00,
    canCombineSections: false,
    courseType: 'lecture',
    requiredQualification: '',
    semester: 'Semester 1',
    expectedEnrollment: 50,
    maxStudentsSection: 50,
    priority: 5
  });

  // Generate Course ID
  const generateCourseId = () => {
    const maxId = courses.length > 0 
      ? Math.max(...courses.map(c => {
          const match = c.courseId?.match(/\d+/);
          return match ? parseInt(match[0]) : 0;
        }))
      : 0;
    return `COURSE${String(maxId + 1).padStart(3, '0')}`;
  };

  // Load courses data from localStorage on component mount
  useEffect(() => {
    const loadCoursesData = () => {
      const savedCourses = localStorage.getItem('courses');
      if (savedCourses) {
        const parsedCourses = JSON.parse(savedCourses);
        setCourses(parsedCourses);
        setFilteredCourses(parsedCourses);
      } else {
        // Initial sample data
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
        setCourses(sampleData);
        setFilteredCourses(sampleData);
        localStorage.setItem('courses', JSON.stringify(sampleData));
      }
    };

    loadCoursesData();
  }, []);

  useEffect(() => {
    // Update course ID when courses change and not editing
    if (!editingCourse) {
      const maxId = courses.length > 0 
        ? Math.max(...courses.map(c => {
            const match = c.courseId?.match(/\d+/);
            return match ? parseInt(match[0]) : 0;
          }))
        : 0;
      const newCourseId = `COURSE${String(maxId + 1).padStart(3, '0')}`;
      setFormData(prev => ({
        ...prev,
        courseId: newCourseId
      }));
    }
  }, [courses.length, editingCourse]);

  useEffect(() => {
    // Filter courses based on semester
    let filtered = courses;

    if (selectedSemester !== 'All') {
      filtered = filtered.filter(course => course.semester === selectedSemester);
    }

    setFilteredCourses(filtered);
  }, [selectedSemester, courses]);

  const semesters = ['All', 'Semester 1', 'Semester 2'];

  // Save courses to localStorage
  const saveCoursesToStorage = (coursesList) => {
    localStorage.setItem('courses', JSON.stringify(coursesList));
  };

  // Handle course added (Create)
  const handleCourseAdded = () => {
    if (!formData.courseCode.trim() || !formData.courseName.trim() || !formData.requiredQualification.trim()) {
      setPopup({
        show: true,
        message: 'Please fill in all required fields.',
        type: 'error'
      });
      return;
    }

    const maxId = courses.length > 0 
      ? Math.max(...courses.map(c => c.id)) 
      : 0;
    
    const newCourse = {
      id: maxId + 1,
      ...formData,
      courseId: formData.courseId || generateCourseId()
    };

    const updatedCourses = [...courses, newCourse];
    setCourses(updatedCourses);
    setFilteredCourses(updatedCourses);
    saveCoursesToStorage(updatedCourses);
    setActiveTab('view-courses');
    
    // Reset form
    setFormData({
      courseId: generateCourseId(),
      courseCode: '',
      courseName: '',
      department: 'Faculty of Computing',
      credits: 3,
      contactHoursWeek: 3.00,
      canCombineSections: false,
      courseType: 'lecture',
      requiredQualification: '',
      semester: 'Semester 1',
      expectedEnrollment: 50,
      maxStudentsSection: 50,
      priority: 5
    });
    
    // Show success popup
    setPopup({
      show: true,
      message: 'Course added successfully!',
      type: 'success'
    });
  };

  // Handle course updated (Update)
  const handleCourseUpdated = () => {
    if (!formData.courseCode.trim() || !formData.courseName.trim() || !formData.requiredQualification.trim()) {
      setPopup({
        show: true,
        message: 'Please fill in all required fields.',
        type: 'error'
      });
      return;
    }

    const updatedList = courses.map(course => 
      course.id === editingCourse.id ? { ...course, ...formData } : course
    );
    setCourses(updatedList);
    setFilteredCourses(updatedList);
    saveCoursesToStorage(updatedList);
    setEditingCourse(null);
    setActiveTab('view-courses');
    
    // Reset form
    setFormData({
      courseId: generateCourseId(),
      courseCode: '',
      courseName: '',
      department: 'Faculty of Computing',
      credits: 3,
      contactHoursWeek: 3.00,
      canCombineSections: false,
      courseType: 'lecture',
      requiredQualification: '',
      semester: 'Semester 1',
      expectedEnrollment: 50,
      maxStudentsSection: 50,
      priority: 5
    });
    
    // Show update popup
    setPopup({
      show: true,
      message: 'Course updated successfully!',
      type: 'success'
    });
  };

  // Handle course deleted (Delete)
  const handleDeleteCourse = (id) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to delete courses.',
        type: 'error'
      });
      return;
    }
    
    if (window.confirm('Are you sure you want to delete this course?')) {
      const updatedList = courses.filter(course => course.id !== id);
      setCourses(updatedList);
      setFilteredCourses(updatedList);
      saveCoursesToStorage(updatedList);
      
      // Clear selected course if it was deleted
      if (selectedCourse && selectedCourse.id === id) {
        setSelectedCourse(null);
      }
      
      // Show delete popup
      setPopup({
        show: true,
        message: 'Course deleted successfully!',
        type: 'delete'
      });
    }
  };

  // Handle edit course
  const handleEditCourse = (course) => {
    if (!isAdministrator) {
      setPopup({
        show: true,
        message: 'You do not have permission to edit courses.',
        type: 'error'
      });
      return;
    }
    
    setEditingCourse(course);
    setFormData({
      courseId: course.courseId || course.courseCode || generateCourseId(),
      courseCode: course.courseCode || '',
      courseName: course.courseName || '',
      department: course.department || 'Faculty of Computing',
      credits: course.credits || 3,
      contactHoursWeek: course.contactHoursWeek || course.contactHours || 3.00,
      canCombineSections: course.canCombineSections || false,
      courseType: course.courseType || 'lecture',
      requiredQualification: course.requiredQualification || '',
      semester: course.semester || 'Semester 1',
      expectedEnrollment: course.expectedEnrollment || 50,
      maxStudentsSection: course.maxStudentsSection || 50,
      priority: course.priority || 5
    });
    setActiveTab('add-course');
  };

  // Handle form input change
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle number change with increment/decrement
  const handleNumberChange = (field, delta) => {
    setFormData(prev => {
      const currentValue = parseFloat(prev[field]) || 0;
      const newValue = Math.max(0, currentValue + delta);
      return {
        ...prev,
        [field]: field === 'contactHoursWeek' ? newValue.toFixed(2) : newValue
      };
    });
  };

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingCourse) {
      handleCourseUpdated();
    } else {
      handleCourseAdded();
    }
  };

  // Handle cancel
  const handleCancel = () => {
    setEditingCourse(null);
    setFormData({
      courseId: generateCourseId(),
      courseCode: '',
      courseName: '',
      department: 'Faculty of Computing',
      credits: 3,
      contactHoursWeek: 3.00,
      canCombineSections: false,
      courseType: 'lecture',
      requiredQualification: '',
      semester: 'Semester 2',
      expectedEnrollment: 50,
      maxStudentsSection: 50,
      priority: 5
    });
    setActiveTab('view-courses');
  };

  // Handle view course
  const handleViewCourse = (course) => {
    setSelectedCourse(course);
    setActiveTab('course-details');
  };

  return (
    <div className="course-management">
      {popup.show && (
        <PopupMessage
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: 'success' })}
        />
      )}
      
      <div className="course-header">
        <div className="course-header-left">
          <span className="course-icon">📚</span>
          <h1 className="course-title">Course Management</h1>
        </div>
        <div className="course-header-right">
          <button className="menu-button">⋮</button>
        </div>
      </div>

      <div className="course-tabs">
        <button
          className={`tab-button ${activeTab === 'view-courses' ? 'active' : ''}`}
          onClick={() => setActiveTab('view-courses')}
        >
          View Courses
        </button>
        {isAdministrator && (
          <button
            className={`tab-button ${activeTab === 'add-course' ? 'active' : ''}`}
            onClick={() => setActiveTab('add-course')}
          >
            Add Course
          </button>
        )}
        <button
          className={`tab-button ${activeTab === 'course-details' ? 'active' : ''}`}
          onClick={() => setActiveTab('course-details')}
        >
          Course Details
        </button>
      </div>

      {activeTab === 'view-courses' && (
        <div className="view-courses-content">
          <div className="filter-section">
            <label htmlFor="semester-filter">Filter by Semester</label>
            <select
              id="semester-filter"
              className="filter-select"
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(e.target.value)}
            >
              {semesters.map(sem => (
                <option key={sem} value={sem}>{sem}</option>
              ))}
            </select>
          </div>

          <h2 className="courses-heading">Courses ({filteredCourses.length})</h2>

          <div className="courses-table-container">
            <table className="courses-table">
              <thead>
                <tr>
                  <th>Course Code</th>
                  <th>Name</th>
                  <th>Department</th>
                  <th>Semester</th>
                  <th>Credits</th>
                  <th>Contact Hours</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredCourses.length > 0 ? (
                  filteredCourses.map(course => (
                    <tr key={course.id}>
                      <td>{course.courseCode}</td>
                      <td>{course.courseName}</td>
                      <td>{course.department || 'N/A'}</td>
                      <td>{course.semester}</td>
                      <td>{course.credits}</td>
                      <td>{course.contactHoursWeek || course.contactHours || 'N/A'}</td>
                      <td>
                        <button 
                          className="action-button view"
                          onClick={() => handleViewCourse(course)}
                        >
                          View Course
                        </button>
                        {isAdministrator && (
                          <>
                            <button 
                              className="action-button"
                              onClick={() => handleEditCourse(course)}
                            >
                              Edit
                            </button>
                            <button 
                              className="action-button delete"
                              onClick={() => handleDeleteCourse(course.id)}
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
                    <td colSpan="7" className="no-data">No courses found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'add-course' && isAdministrator && (
        <div className="add-course-content">
          <h2 className="course-form-heading">{editingCourse ? 'Edit Course' : 'Add New Course'}</h2>
          <div className="form-container">
            <form className="course-form" onSubmit={handleSubmit}>
              <div className="form-columns">
                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="courseId">
                      Course ID <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="courseId"
                      className="form-input"
                      value={formData.courseId}
                      onChange={(e) => handleInputChange('courseId', e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="courseName">
                      Course Name <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="courseName"
                      className="form-input"
                      value={formData.courseName}
                      onChange={(e) => handleInputChange('courseName', e.target.value)}
                      required
                      placeholder="e.g., Introduction to Computer Science"
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
                      <option value="Faculty of Computing">Faculty of Computing</option>
                      <option value="Faculty of Business">Faculty of Business</option>
                      <option value="Faculty of Sciences">Faculty of Sciences</option>
                      <option value="Faculty of Architecture">Faculty of Architecture</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="courseCode">
                      Course Code <span className="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="courseCode"
                      className="form-input"
                      value={formData.courseCode}
                      onChange={(e) => handleInputChange('courseCode', e.target.value)}
                      required
                      placeholder="e.g., CS101"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="credits">
                      Credits <span className="required">*</span>
                    </label>
                    <div className="number-input-group">
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('credits', -1)}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        id="credits"
                        className="form-input number-input"
                        value={formData.credits}
                        onChange={(e) => handleInputChange('credits', parseInt(e.target.value) || 0)}
                        required
                        min="1"
                        max="6"
                      />
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('credits', 1)}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="contactHoursWeek">
                      Contact Hours/Week <span className="required">*</span>
                    </label>
                    <div className="number-input-group">
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('contactHoursWeek', -0.5)}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        id="contactHoursWeek"
                        className="form-input number-input"
                        step="0.5"
                        min="0"
                        value={formData.contactHoursWeek}
                        onChange={(e) => handleInputChange('contactHoursWeek', parseFloat(e.target.value) || 0)}
                        required
                      />
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('contactHoursWeek', 0.5)}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="form-group checkbox-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={formData.canCombineSections}
                        onChange={(e) => handleInputChange('canCombineSections', e.target.checked)}
                      />
                      <span>Can Combine Sections</span>
                    </label>
                  </div>

                  <div className="form-group">
                    <label htmlFor="courseType">Course Type</label>
                    <select
                      id="courseType"
                      className="form-input"
                      value={formData.courseType}
                      onChange={(e) => handleInputChange('courseType', e.target.value)}
                    >
                      <option value="lecture">Lecture</option>
                      <option value="lab">Lab</option>
                      <option value="seminar">Seminar</option>
                      <option value="workshop">Workshop</option>
                    </select>
                  </div>
                </div>

                <div className="form-column">
                  <div className="form-group">
                    <label htmlFor="requiredQualification" className="label-with-help">
                      Required Qualification <span className="required">*</span>
                      <span className="help-icon" title="Enter the prerequisite course code">?</span>
                    </label>
                    <input
                      type="text"
                      id="requiredQualification"
                      className="form-input"
                      value={formData.requiredQualification}
                      onChange={(e) => handleInputChange('requiredQualification', e.target.value)}
                      required
                      placeholder="e.g., CS101"
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="semester">
                      Semester <span className="required">*</span>
                    </label>
                    <select
                      id="semester"
                      className="form-input"
                      value={formData.semester}
                      onChange={(e) => handleInputChange('semester', e.target.value)}
                      required
                    >
                      <option value="Semester 1">Semester 1</option>
                      <option value="Semester 2">Semester 2</option>
                     
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="expectedEnrollment">
                      Expected Enrollment <span className="required">*</span>
                    </label>
                    <div className="number-input-group">
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('expectedEnrollment', -1)}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        id="expectedEnrollment"
                        className="form-input number-input"
                        value={formData.expectedEnrollment}
                        onChange={(e) => handleInputChange('expectedEnrollment', parseInt(e.target.value) || 0)}
                        required
                        min="1"
                      />
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('expectedEnrollment', 1)}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="maxStudentsSection">
                      Max Students/Section <span className="required">*</span>
                    </label>
                    <div className="number-input-group">
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('maxStudentsSection', -1)}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        id="maxStudentsSection"
                        className="form-input number-input"
                        value={formData.maxStudentsSection}
                        onChange={(e) => handleInputChange('maxStudentsSection', parseInt(e.target.value) || 0)}
                        required
                        min="1"
                      />
                      <button
                        type="button"
                        className="number-button"
                        onClick={() => handleNumberChange('maxStudentsSection', 1)}
                      >
                        +
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="priority">
                      Priority <span className="priority-value">{formData.priority}</span>
                    </label>
                    <input
                      type="range"
                      id="priority"
                      className="priority-slider"
                      min="1"
                      max="10"
                      value={formData.priority}
                      onChange={(e) => handleInputChange('priority', parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button 
                  type="submit" 
                  className="submit-button"
                >
                  {editingCourse ? 'Update Course' : 'Add Course'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {activeTab === 'add-course' && !isAdministrator && (
        <div className="view-courses-content">
          <p className="info-message">You do not have permission to add or edit courses.</p>
        </div>
      )}

      {activeTab === 'course-details' && (
        <div className="course-details-content">
          <h2 className="course-form-heading">Course Details</h2>
          {selectedCourse ? (
            <div className="details-grid">
              <div className="detail-card">
                <h3 className="detail-card-title">{selectedCourse.courseName}</h3>
                <div className="detail-card-content">
                  <div className="detail-item">
                    <span className="detail-label">Course ID:</span>
                    <span className="detail-value">{selectedCourse.courseId || selectedCourse.courseCode || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Course Code:</span>
                    <span className="detail-value">{selectedCourse.courseCode}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Department:</span>
                    <span className="detail-value">{selectedCourse.department || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Semester:</span>
                    <span className="detail-value">{selectedCourse.semester}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Credits:</span>
                    <span className="detail-value">{selectedCourse.credits}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Contact Hours/Week:</span>
                    <span className="detail-value">{selectedCourse.contactHoursWeek || selectedCourse.contactHours || 'N/A'}</span>
                  </div>
                  {selectedCourse.canCombineSections !== undefined && (
                    <div className="detail-item">
                      <span className="detail-label">Can Combine Sections:</span>
                      <span className="detail-value">{selectedCourse.canCombineSections ? 'Yes' : 'No'}</span>
                    </div>
                  )}
                  {selectedCourse.courseType && (
                    <div className="detail-item">
                      <span className="detail-label">Course Type:</span>
                      <span className="detail-value">{selectedCourse.courseType.charAt(0).toUpperCase() + selectedCourse.courseType.slice(1)}</span>
                    </div>
                  )}
                  {selectedCourse.requiredQualification && (
                    <div className="detail-item">
                      <span className="detail-label">Required Qualification:</span>
                      <span className="detail-value">{selectedCourse.requiredQualification}</span>
                    </div>
                  )}
                  {selectedCourse.expectedEnrollment && (
                    <div className="detail-item">
                      <span className="detail-label">Expected Enrollment:</span>
                      <span className="detail-value">{selectedCourse.expectedEnrollment}</span>
                    </div>
                  )}
                  {selectedCourse.maxStudentsSection && (
                    <div className="detail-item">
                      <span className="detail-label">Max Students/Section:</span>
                      <span className="detail-value">{selectedCourse.maxStudentsSection}</span>
                    </div>
                  )}
                  {selectedCourse.priority !== undefined && (
                    <div className="detail-item">
                      <span className="detail-label">Priority:</span>
                      <span className="detail-value">{selectedCourse.priority}</span>
                    </div>
                  )}
                  {selectedCourse.description && (
                    <div className="detail-item">
                      <span className="detail-label">Description:</span>
                      <span className="detail-value">{selectedCourse.description}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <p className="info-message">Click "View Course" on a course from the View Courses tab to see its details here.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default CourseManagement;

