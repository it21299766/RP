import { get } from '../utils/api';

export const reportsApi = {
  // Staff Workload Summary Report
  getStaffWorkloadSummary: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.staff_id) queryParams.append('staff_id', params.staff_id);
    if (params.semester) queryParams.append('semester', params.semester);
    if (params.department) queryParams.append('department', params.department);
    return get(`/api/reports/staff-workload?${queryParams.toString()}`);
  },

  // Workload by Type Report
  getWorkloadByType: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.staff_id) queryParams.append('staff_id', params.staff_id);
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/workload-by-type?${queryParams.toString()}`);
  },

  // Workload by Domain Report
  getWorkloadByDomain: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.staff_id) queryParams.append('staff_id', params.staff_id);
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/workload-by-domain?${queryParams.toString()}`);
  },

  // Department Summary Report
  getDepartmentSummary: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/department-summary?${queryParams.toString()}`);
  },

  // Program Teaching Load Report
  getProgramTeachingLoad: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.program_id) queryParams.append('program_id', params.program_id);
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/program-teaching-load?${queryParams.toString()}`);
  },

  // Unassigned Tasks Report
  getUnassignedTasks: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.program_id) queryParams.append('program_id', params.program_id);
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/unassigned-tasks?${queryParams.toString()}`);
  },

  // Overload/Underload Distribution Report
  getOverloadUnderloadDistribution: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/overload-underload?${queryParams.toString()}`);
  },

  // GA Optimization Summary Report
  getGAOptimizationSummary: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/ga-result-summary?${queryParams.toString()}`);
  },

  // Change Request Summary Report
  getChangeRequestSummary: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.status) queryParams.append('status', params.status);
    return get(`/api/reports/change-requests?${queryParams.toString()}`);
  },

  // Staff Workload Detail Report
  getStaffWorkloadDetail: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.staff_id) queryParams.append('staff_id', params.staff_id);
    if (params.semester) queryParams.append('semester', params.semester);
    // Use workload-by-type for detailed breakdown
    return get(`/api/reports/workload-by-type?${queryParams.toString()}`);
  },

  // Program Section Teaching Load Report
  getProgramSectionTeachingLoad: (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.program_id) queryParams.append('program_id', params.program_id);
    if (params.semester) queryParams.append('semester', params.semester);
    return get(`/api/reports/program-section-workload?${queryParams.toString()}`);
  },
};

