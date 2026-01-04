# REST API Endpoints Documentation

This document lists all REST API endpoints required for the Staff Workload System frontend.

**Base URL**: `http://localhost:8000` (configurable via `REACT_APP_API_BASE` environment variable)

---

## 1. Authentication

### POST /api/auth/login
Authenticate user and return role information.

**Request Payload:**
```json
{
  "registrationNumber": "Ad12345",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "role": "Administrator",
  "registrationNumber": "Ad12345",
  "token": "jwt_token_here"
}
```

---

## 2. Dashboard

### GET /api/dashboard
Get dashboard metrics and workload distribution data.

**Request:** No payload required

**Response:**
```json
{
  "metrics": {
    "totalStaff": 5,
    "totalCourses": 8,
    "totalAssignments": 12,
    "assignmentRate": 75.0,
    "unassigned": 2
  },
  "workloadDistribution": [
    {
      "name": "Dr. John Smith",
      "workload": 18,
      "capacity": 20
    },
    {
      "name": "Dr. Sarah Johnson",
      "workload": 15,
      "capacity": 20
    }
  ],
  "workloadFairness": [
    {
      "name": "Dr. John Smith",
      "value": 18
    },
    {
      "name": "Dr. Sarah Johnson",
      "value": 15
    }
  ]
}
```

---

## 3. Staff Management

### GET /api/staff
Get all staff members (with optional filtering).

**Request:** No payload required (query params: `?department=Computer Science&search=john`)

**Response:**
```json
[
  {
    "id": 1,
    "staffId": "STAFF001",
    "name": "Dr. John Smith",
    "email": "john.smith@university.edu",
    "department": "Computer Science",
    "position": "Professor",
    "role": "professor",
    "qualifications": "PhD in Computer Science, CS101, CS201",
    "teachingHours": 12,
    "researchHours": 6,
    "totalHours": 18,
    "minContactHoursYear": 300.00,
    "minContactHoursWeek": 10.00,
    "maxHoursWeek": 30.00,
    "minHoursWeek": 15.00,
    "profilePicture": "data:image/jpeg;base64,..."
  }
]
```

### POST /api/staff
Create a new staff member.

**Request Payload:**
```json
{
  "staffId": "STAFF001",
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "role": "professor",
  "position": "Professor",
  "qualifications": "PhD in Computer Science, CS101, CS201",
  "minContactHoursYear": 300.00,
  "minContactHoursWeek": 10.00,
  "maxHoursWeek": 30.00,
  "minHoursWeek": 15.00,
  "profilePicture": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "id": 1,
  "staffId": "STAFF001",
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "position": "Professor",
  "role": "professor",
  "qualifications": "PhD in Computer Science, CS101, CS201",
  "teachingHours": 10.00,
  "researchHours": 5.00,
  "totalHours": 15.00,
  "minContactHoursYear": 300.00,
  "minContactHoursWeek": 10.00,
  "maxHoursWeek": 30.00,
  "minHoursWeek": 15.00,
  "profilePicture": "data:image/jpeg;base64,..."
}
```

### PUT /api/staff/:id
Update an existing staff member.

**Request Payload:**
```json
{
  "staffId": "STAFF001",
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "role": "professor",
  "position": "Professor",
  "qualifications": "PhD in Computer Science, CS101, CS201, CS301",
  "minContactHoursYear": 320.00,
  "minContactHoursWeek": 12.00,
  "maxHoursWeek": 30.00,
  "minHoursWeek": 18.00,
  "profilePicture": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "id": 1,
  "staffId": "STAFF001",
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "position": "Professor",
  "role": "professor",
  "qualifications": "PhD in Computer Science, CS101, CS201, CS301",
  "teachingHours": 12.00,
  "researchHours": 6.00,
  "totalHours": 18.00,
  "minContactHoursYear": 320.00,
  "minContactHoursWeek": 12.00,
  "maxHoursWeek": 30.00,
  "minHoursWeek": 18.00,
  "profilePicture": "data:image/jpeg;base64,..."
}
```

### DELETE /api/staff/:id
Delete a staff member.

**Request:** No payload required

**Response:**
```json
{
  "success": true,
  "message": "Staff member deleted successfully"
}
```

---

## 4. Course Management

### GET /api/courses
Get all courses (with optional filtering).

**Request:** No payload required (query params: `?semester=Semester 1&department=Computer Science`)

**Response:**
```json
[
  {
    "id": 1,
    "courseId": "COURSE001",
    "courseCode": "CS101",
    "courseName": "Introduction to Computer Science",
    "department": "Computer Science",
    "semester": "Semester 1",
    "credits": 3,
    "contactHoursWeek": 3.00,
    "contactHours": 3,
    "canCombineSections": false,
    "courseType": "lecture",
    "requiredQualification": "CS100",
    "expectedEnrollment": 50,
    "maxStudentsSection": 50,
    "priority": 5,
    "description": "Fundamental concepts of computer science"
  }
]
```

### POST /api/courses
Create a new course.

**Request Payload:**
```json
{
  "courseId": "COURSE001",
  "courseCode": "CS101",
  "courseName": "Introduction to Computer Science",
  "department": "Faculty of Computing",
  "credits": 3,
  "contactHoursWeek": 3.00,
  "canCombineSections": false,
  "courseType": "lecture",
  "requiredQualification": "CS100",
  "semester": "Semester 1",
  "expectedEnrollment": 50,
  "maxStudentsSection": 50,
  "priority": 5,
  "description": "Fundamental concepts of computer science"
}
```

**Response:**
```json
{
  "id": 1,
  "courseId": "COURSE001",
  "courseCode": "CS101",
  "courseName": "Introduction to Computer Science",
  "department": "Faculty of Computing",
  "semester": "Semester 1",
  "credits": 3,
  "contactHoursWeek": 3.00,
  "canCombineSections": false,
  "courseType": "lecture",
  "requiredQualification": "CS100",
  "expectedEnrollment": 50,
  "maxStudentsSection": 50,
  "priority": 5,
  "description": "Fundamental concepts of computer science"
}
```

### PUT /api/courses/:id
Update an existing course.

**Request Payload:**
```json
{
  "courseId": "COURSE001",
  "courseCode": "CS101",
  "courseName": "Introduction to Computer Science",
  "department": "Faculty of Computing",
  "credits": 4,
  "contactHoursWeek": 4.00,
  "canCombineSections": true,
  "courseType": "lecture",
  "requiredQualification": "CS100",
  "semester": "Semester 1",
  "expectedEnrollment": 60,
  "maxStudentsSection": 60,
  "priority": 7,
  "description": "Fundamental concepts of computer science - Updated"
}
```

**Response:**
```json
{
  "id": 1,
  "courseId": "COURSE001",
  "courseCode": "CS101",
  "courseName": "Introduction to Computer Science",
  "department": "Faculty of Computing",
  "semester": "Semester 1",
  "credits": 4,
  "contactHoursWeek": 4.00,
  "canCombineSections": true,
  "courseType": "lecture",
  "requiredQualification": "CS100",
  "expectedEnrollment": 60,
  "maxStudentsSection": 60,
  "priority": 7,
  "description": "Fundamental concepts of computer science - Updated"
}
```

### DELETE /api/courses/:id
Delete a course.

**Request:** No payload required

**Response:**
```json
{
  "success": true,
  "message": "Course deleted successfully"
}
```

---

## 5. Task Management

### GET /api/tasks
Get all tasks.

**Request:** No payload required (query params: `?category=academic&department=Computer Science`)

**Response:**
```json
[
  {
    "id": 1,
    "taskId": "T001",
    "taskName": "Review Course Materials",
    "description": "Review and update course materials for CS101",
    "category": "academic",
    "hoursNeeded": "40",
    "noOfStaff": "2",
    "staffQualificationCriteria": "PhD in Computer Science, 5+ years teaching experience",
    "department": "Computer Science",
    "programme": "Bachelor of Science",
    "module": "Module 1"
  }
]
```

### POST /api/tasks
Create a new task.

**Request Payload:**
```json
{
  "taskId": "T001",
  "taskName": "Review Course Materials",
  "description": "Review and update course materials for CS101",
  "category": "academic",
  "hoursNeeded": "40",
  "noOfStaff": "2",
  "staffQualificationCriteria": "PhD in Computer Science, 5+ years teaching experience",
  "department": "Computer Science",
  "programme": "Bachelor of Science",
  "module": "Module 1"
}
```

**Response:**
```json
{
  "id": 1,
  "taskId": "T001",
  "taskName": "Review Course Materials",
  "description": "Review and update course materials for CS101",
  "category": "academic",
  "hoursNeeded": "40",
  "noOfStaff": "2",
  "staffQualificationCriteria": "PhD in Computer Science, 5+ years teaching experience",
  "department": "Computer Science",
  "programme": "Bachelor of Science",
  "module": "Module 1"
}
```

### PUT /api/tasks/:id
Update an existing task.

**Request Payload:**
```json
{
  "taskId": "T001",
  "taskName": "Review Course Materials",
  "description": "Review and update course materials for CS101 and CS201",
  "category": "academic",
  "hoursNeeded": "50",
  "noOfStaff": "3",
  "staffQualificationCriteria": "PhD in Computer Science, 5+ years teaching experience",
  "department": "Computer Science",
  "programme": "Bachelor of Science",
  "module": "Module 1"
}
```

**Response:**
```json
{
  "id": 1,
  "taskId": "T001",
  "taskName": "Review Course Materials",
  "description": "Review and update course materials for CS101 and CS201",
  "category": "academic",
  "hoursNeeded": "50",
  "noOfStaff": "3",
  "staffQualificationCriteria": "PhD in Computer Science, 5+ years teaching experience",
  "department": "Computer Science",
  "programme": "Bachelor of Science",
  "module": "Module 1"
}
```

### DELETE /api/tasks/:id
Delete a task.

**Request:** No payload required

**Response:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

---

## 6. Workload Allocation

### POST /api/workload/allocate
Run workload allocation algorithm.

**Request Payload:**
```json
{
  "semester": "Semester 1",
  "department": "All"
}
```

**Response:**
```json
{
  "success": true,
  "allocationId": "ALLOC_2024_001",
  "message": "Allocation completed successfully",
  "results": {
    "totalAssignments": 12,
    "totalStaff": 5,
    "totalCourses": 8,
    "allocationRate": 100.0,
    "allocations": [
      {
        "staffId": 1,
        "staffName": "Dr. John Smith",
        "courseId": 1,
        "courseCode": "CS101",
        "courseName": "Introduction to Computer Science",
        "hours": 3,
        "taskId": null,
        "taskName": null
      }
    ]
  }
}
```

### GET /api/workload/results
Get allocation results (optional: by allocationId).

**Request:** No payload required (query params: `?allocationId=ALLOC_2024_001&semester=Semester 1`)

**Response:**
```json
{
  "allocationId": "ALLOC_2024_001",
  "semester": "Semester 1",
  "department": "All",
  "createdAt": "2024-01-15T10:30:00Z",
  "results": {
    "totalAssignments": 12,
    "totalStaff": 5,
    "totalCourses": 8,
    "allocationRate": 100.0,
    "allocations": [
      {
        "staffId": 1,
        "staffName": "Dr. John Smith",
        "courseId": 1,
        "courseCode": "CS101",
        "courseName": "Introduction to Computer Science",
        "hours": 3,
        "taskId": null,
        "taskName": null
      }
    ]
  }
}
```

---

## 7. Reports

### POST /api/reports/generate
Generate a report based on filters.

**Request Payload:**
```json
{
  "reportType": "staff-workload-summary",
  "filters": {
    "academicPeriod": "2024-2025",
    "semester": "Semester 1",
    "program": "CS",
    "programSection": "A",
    "staffId": null,
    "department": "Computer Science"
  }
}
```

**Response:**
```json
{
  "reportType": "staff-workload-summary",
  "filters": {
    "academicPeriod": "2024-2025",
    "semester": "Semester 1",
    "program": "CS",
    "programSection": "A"
  },
  "summary": {
    "hoursAssigned": 18,
    "teachingPercent": 60,
    "adminPercent": 25,
    "researchPercent": 15,
    "overload": false
  },
  "tableData": [
    {
      "staffName": "Dr. John Smith",
      "domain": "Teaching",
      "tasks": 3,
      "totalHours": 18,
      "teachingHours": 12,
      "adminHours": 4,
      "researchHours": 2,
      "status": "normal"
    }
  ],
  "chartData": [
    {
      "name": "Dr. John Smith",
      "hours": 18
    }
  ]
}
```

**Available Report Types:**
- `staff-workload-summary` - Staff Workload Summary
- `program-teaching-load` - Program Teaching Load Report
- `task-assignment` - Task Assignment Report
- `underload-overload` - Underload/Overload Report
- `ga-optimization` - GA Optimization Output Report
- `change-requests` - Change Requests Report
- `module-teaching` - Module-Level Teaching Report
- `staff-activity` - Staff Activity Report

### GET /api/reports/:reportId
Get a previously generated report by ID.

**Request:** No payload required

**Response:** Same as POST /api/reports/generate

### GET /api/reports/download/:reportId
Download report in specified format.

**Request:** No payload required (query params: `?format=pdf` or `?format=csv`)

**Response:** File download (PDF or CSV)

---

## 8. Additional Endpoints (Optional)

### GET /api/departments
Get list of all departments.

**Request:** No payload required

**Response:**
```json
[
  "Computer Science",
  "Mathematics",
  "Physics",
  "Chemistry",
  "Biology"
]
```

### GET /api/programmes
Get list of all programmes.

**Request:** No payload required

**Response:**
```json
[
  "Bachelor of Science",
  "Bachelor of Arts",
  "Master of Science",
  "Master of Arts",
  "PhD",
  "Diploma"
]
```

### GET /api/staff/:id/workload
Get workload details for a specific staff member.

**Request:** No payload required

**Response:**
```json
{
  "staffId": 1,
  "staffName": "Dr. John Smith",
  "totalHours": 18,
  "teachingHours": 12,
  "researchHours": 6,
  "adminHours": 0,
  "allocations": [
    {
      "courseId": 1,
      "courseCode": "CS101",
      "courseName": "Introduction to Computer Science",
      "hours": 3
    }
  ],
  "tasks": [
    {
      "taskId": 1,
      "taskName": "Review Course Materials",
      "hours": 5
    }
  ]
}
```

---

## Error Responses

All endpoints should return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "error": "Validation failed",
  "message": "Missing required field: name",
  "details": {
    "field": "name",
    "reason": "required"
  }
}
```

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

**403 Forbidden:**
```json
{
  "error": "Forbidden",
  "message": "You do not have permission to perform this action"
}
```

**404 Not Found:**
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

## Authentication

Most endpoints (except login) should include an authentication token in the request headers:

```
Authorization: Bearer <token>
```

---

## Notes

1. All dates should be in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:mm:ssZ)
2. All numeric values should be sent as numbers, not strings (except where explicitly noted)
3. Profile pictures should be sent as base64-encoded data URLs
4. Pagination can be added using query parameters: `?page=1&limit=10`
5. Filtering can be done via query parameters for GET requests
6. All endpoints should support CORS for frontend access

