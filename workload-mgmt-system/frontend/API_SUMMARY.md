# API Endpoints Quick Reference

## Base URL
`http://localhost:8000`

---

## 1. Authentication
- **POST** `/api/auth/login`
  - Payload: `{ "registrationNumber": "Ad12345", "password": "password123" }`

## 2. Dashboard
- **GET** `/api/dashboard`
  - Returns: metrics, workloadDistribution, workloadFairness

## 3. Staff Management
- **GET** `/api/staff` - List all staff
- **POST** `/api/staff` - Create staff
  - Payload: `{ staffId, name, email, department, role, qualifications, minContactHoursYear, minContactHoursWeek, maxHoursWeek, minHoursWeek, profilePicture }`
- **PUT** `/api/staff/:id` - Update staff
- **DELETE** `/api/staff/:id` - Delete staff

## 4. Course Management
- **GET** `/api/courses` - List all courses
- **POST** `/api/courses` - Create course
  - Payload: `{ courseId, courseCode, courseName, department, credits, contactHoursWeek, canCombineSections, courseType, requiredQualification, semester, expectedEnrollment, maxStudentsSection, priority, description }`
- **PUT** `/api/courses/:id` - Update course
- **DELETE** `/api/courses/:id` - Delete course

## 5. Task Management
- **GET** `/api/tasks` - List all tasks
- **POST** `/api/tasks` - Create task
  - Payload: `{ taskId, taskName, description, category, hoursNeeded, noOfStaff, staffQualificationCriteria, department, programme, module }`
- **PUT** `/api/tasks/:id` - Update task
- **DELETE** `/api/tasks/:id` - Delete task

## 6. Workload Allocation
- **POST** `/api/workload/allocate` - Run allocation
  - Payload: `{ semester, department }`
- **GET** `/api/workload/results` - Get allocation results

## 7. Reports
- **POST** `/api/reports/generate` - Generate report
  - Payload: `{ reportType, filters: { academicPeriod, semester, program, programSection, staffId, department } }`
- **GET** `/api/reports/:reportId` - Get report by ID
- **GET** `/api/reports/download/:reportId` - Download report (PDF/CSV)

## 8. Additional
- **GET** `/api/departments` - List departments
- **GET** `/api/programmes` - List programmes
- **GET** `/api/staff/:id/workload` - Get staff workload details

---

## Report Types
1. `staff-workload-summary` - Staff Workload Summary
2. `program-teaching-load` - Program Teaching Load Report
3. `task-assignment` - Task Assignment Report
4. `underload-overload` - Underload/Overload Report
5. `ga-optimization` - GA Optimization Output Report
6. `change-requests` - Change Requests Report
7. `module-teaching` - Module-Level Teaching Report
8. `staff-activity` - Staff Activity Report

---

## Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

For detailed payload structures and response formats, see `API_ENDPOINTS.md`.



