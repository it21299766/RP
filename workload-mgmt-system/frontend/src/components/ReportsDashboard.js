import React, { useState, useContext } from 'react';
import './ReportsDashboard.css';
import ReportFiltersModal from './ReportFiltersModal';
import ReportViewer from './ReportViewer';
import { downloadPDF, downloadCSV } from '../utils/reportExports';
import { reportsApi } from '../api/reportsApi';
import { AuthContext } from '../context/AuthContext';

const ReportsDashboard = ({ userRole = 'Administrator' }) => {
  const { user: currentUser } = useContext(AuthContext);
  const [selectedReport, setSelectedReport] = useState(null);
  const [showFiltersModal, setShowFiltersModal] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [filters, setFilters] = useState({
    academicPeriod: '',
    semester: '',
    program: '',
    programSection: '',
    staff: ''
  });

  const isAdministrator = userRole === 'Administrator';
  const isStaff = userRole === 'Staff';

  // Define report types based on role
  const adminReports = [
    {
      id: 'staff-workload-summary',
      name: 'Staff Workload Summary',
      description: 'Hours by category + overload flags',
      icon: '📊',
      availableFor: ['Administrator', 'Staff']
    },
    {
      id: 'program-teaching-load',
      name: 'Program Teaching Load Report',
      description: 'Teaching demand vs staff availability',
      icon: '📚',
      availableFor: ['Administrator']
    },
    {
      id: 'task-assignment',
      name: 'Task Assignment Report',
      description: 'All tasks with staff assignments',
      icon: '✅',
      availableFor: ['Administrator']
    },
    {
      id: 'underload-overload',
      name: 'Underload/Overload Report',
      description: 'Staff needing adjustments',
      icon: '⚖️',
      availableFor: ['Administrator']
    },
    {
      id: 'ga-optimization',
      name: 'GA Optimization Output Report',
      description: 'Before/After GA comparison',
      icon: '🔬',
      availableFor: ['Administrator']
    },
    {
      id: 'change-requests',
      name: 'Change Requests Report',
      description: 'All pending/approved/rejected CRs',
      icon: '📝',
      availableFor: ['Administrator']
    },
    {
      id: 'module-teaching',
      name: 'Module-Level Teaching Report',
      description: 'Teaching hours + sections',
      icon: '📖',
      availableFor: ['Administrator']
    }
  ];

  const staffReports = [
    {
      id: 'staff-workload-summary',
      name: 'My Workload Summary',
      description: 'Your hours by category + overload flags',
      icon: '📊',
      availableFor: ['Administrator', 'Staff']
    }
  ];

  const reports = isAdministrator ? adminReports : staffReports;

  const handleViewReport = (reportId) => {
    setSelectedReport(reportId);
    setShowFiltersModal(true);
  };

  const handleGenerateReport = async (reportFilters) => {
    setFilters(reportFilters);
    setShowFiltersModal(false);
    
    try {
      const params = {
        semester: reportFilters.semester || undefined,
        program_id: reportFilters.program ? parseInt(reportFilters.program) : undefined,
        department: reportFilters.department || undefined,
        staff_id: isStaff ? currentUser.staff_id : (reportFilters.staff ? parseInt(reportFilters.staff) : undefined)
      };

      let apiResponse = null;
      let workloadByTypeData = null;
      
      switch (selectedReport) {
        case 'staff-workload-summary':
          apiResponse = await reportsApi.getStaffWorkloadSummary(params);
          workloadByTypeData = await reportsApi.getWorkloadByType(params);
          break;
        case 'program-teaching-load':
          apiResponse = await reportsApi.getProgramTeachingLoad(params);
          break;
        case 'task-assignment':
          // Use workload-by-type for task assignment report
          apiResponse = await reportsApi.getWorkloadByType(params);
          break;
        case 'underload-overload':
          apiResponse = await reportsApi.getOverloadUnderloadDistribution(params);
          break;
        case 'ga-optimization':
          apiResponse = await reportsApi.getGAOptimizationSummary(params);
          break;
        case 'change-requests':
          apiResponse = await reportsApi.getChangeRequestSummary(params);
          break;
        case 'module-teaching':
          apiResponse = await reportsApi.getProgramSectionTeachingLoad(params);
          break;
        default:
          console.error('Unknown report type:', selectedReport);
          return;
      }

      // Transform API response based on report type
      let transformedTableData = [];
      let transformedChartData = [];
      let transformedSummary = {};

      if (selectedReport === 'staff-workload-summary') {
        // Create a map of staff_id to task type hours breakdown
        const staffTypeHoursMap = {};
        if (workloadByTypeData && workloadByTypeData.data) {
          workloadByTypeData.data.forEach(item => {
            const staffId = item.staff_id;
            if (!staffTypeHoursMap[staffId]) {
              staffTypeHoursMap[staffId] = { teaching: 0, admin: 0, research: 0 };
            }
            const taskType = (item.task_type || '').toLowerCase();
            const hours = item.type_hours || 0;
            if (taskType === 'lecture' || taskType === 'lab' || taskType === 'tutorial' || taskType === 'exam') {
              staffTypeHoursMap[staffId].teaching += hours;
            } else if (taskType === 'admin' || taskType === 'administrative') {
              staffTypeHoursMap[staffId].admin += hours;
            } else if (taskType === 'research') {
              staffTypeHoursMap[staffId].research += hours;
            }
          });
        }
        
        transformedTableData = (apiResponse.data || []).map(item => {
          const staffId = item.staff_id;
          const typeHours = staffTypeHoursMap[staffId] || { teaching: 0, admin: 0, research: 0 };
          
          return {
            ...item,
            staffName: item.full_name || item.staff_name || item.name || 'Unknown',
            totalHours: item.total_assigned_hours || item.total_hours || item.hours || 0,
            domain: item.domain_name || item.department || item.domain || 'N/A',
            tasks: item.total_assignments || item.task_count || item.tasks || 0,
            teachingHours: typeHours.teaching || item.teaching_hours || 0,
            adminHours: typeHours.admin || item.admin_hours || 0,
            researchHours: typeHours.research || item.research_hours || 0,
            status: item.workload_status || item.status || 'Normal'
          };
        });

        transformedChartData = transformedTableData.map(item => ({
          name: item.staffName || 'Unknown',
          hours: item.totalHours || 0
        }));

        const totalHours = transformedTableData.reduce((sum, item) => sum + (item.totalHours || 0), 0);
        const totalTeaching = transformedTableData.reduce((sum, item) => sum + (item.teachingHours || 0), 0);
        const totalAdmin = transformedTableData.reduce((sum, item) => sum + (item.adminHours || 0), 0);
        const totalResearch = transformedTableData.reduce((sum, item) => sum + (item.researchHours || 0), 0);
        
        transformedSummary = {
          hoursAssigned: totalHours || 0,
          teachingPercent: totalHours > 0 ? Math.round((totalTeaching / totalHours) * 100) : 0,
          adminPercent: totalHours > 0 ? Math.round((totalAdmin / totalHours) * 100) : 0,
          researchPercent: totalHours > 0 ? Math.round((totalResearch / totalHours) * 100) : 0,
          overload: transformedTableData.some(item => item.status === 'OVERLOADED')
        };
      } else if (selectedReport === 'program-teaching-load') {
        transformedTableData = (apiResponse.data || []).map(item => ({
          programName: item.program_name || item.program_code || 'N/A',
          programCode: item.program_code || 'N/A',
          domain: item.domain_name || 'N/A',
          totalTasks: item.total_task_instances || 0,
          assignedTasks: item.assigned_tasks || 0,
          unassignedTasks: item.unassigned_tasks || 0,
          totalHours: item.total_program_hours || 0,
          assignedHours: item.assigned_hours || 0
        }));

        transformedChartData = transformedTableData.map(item => ({
          name: item.programName || 'Unknown',
          hours: item.assignedHours || 0
        }));

        const totalHours = transformedTableData.reduce((sum, item) => sum + (item.assignedHours || 0), 0);
        transformedSummary = {
          hoursAssigned: totalHours || 0,
          teachingPercent: 100,
          adminPercent: 0,
          researchPercent: 0,
          overload: false
        };
      } else if (selectedReport === 'task-assignment') {
        transformedTableData = (apiResponse.data || []).map(item => ({
          staffName: item.full_name || item.staff_name || 'Unknown',
          taskType: item.task_type || 'N/A',
          hours: item.type_hours || 0,
          taskCount: item.task_count || 0,
          staffId: item.staff_id
        }));

        transformedChartData = transformedTableData.map(item => ({
          name: `${item.staffName} - ${item.taskType}`,
          hours: item.hours || 0
        }));

        const totalHours = transformedTableData.reduce((sum, item) => sum + (item.hours || 0), 0);
        transformedSummary = {
          hoursAssigned: totalHours || 0,
          teachingPercent: 0,
          adminPercent: 0,
          researchPercent: 0,
          overload: false
        };
      } else if (selectedReport === 'underload-overload') {
        transformedTableData = (apiResponse.data || []).map(item => ({
          status: item.workload_status || 'UNKNOWN',
          staffCount: item.staff_count || 0
        }));

        transformedChartData = transformedTableData.map(item => ({
          name: item.status || 'Unknown',
          value: item.staffCount || 0
        }));

        const totalStaff = transformedTableData.reduce((sum, item) => sum + (item.staffCount || 0), 0);
        transformedSummary = {
          hoursAssigned: 0,
          teachingPercent: 0,
          adminPercent: 0,
          researchPercent: 0,
          overload: transformedTableData.some(item => item.status === 'OVERLOADED' && item.staffCount > 0)
        };
      } else if (selectedReport === 'ga-optimization') {
        // GA optimization returns a dictionary directly, not wrapped in data
        const gaData = apiResponse;
        transformedTableData = [gaData]; // Single row with summary data
        transformedChartData = [
          { name: 'System Assignments', value: gaData.system_assignments || 0 },
          { name: 'Admin Assignments', value: gaData.admin_assignments || 0 }
        ];
        transformedSummary = {
          hoursAssigned: gaData.total_assigned_hours || 0,
          teachingPercent: 0,
          adminPercent: 0,
          researchPercent: 0,
          overload: false,
          totalAssignedTasks: gaData.total_assigned_tasks || 0,
          totalStaff: gaData.total_staff_with_assignments || 0,
          averageHoursPerTask: gaData.average_hours_per_task || 0,
          systemAssignments: gaData.system_assignments || 0,
          adminAssignments: gaData.admin_assignments || 0
        };
      } else if (selectedReport === 'change-requests') {
        transformedTableData = (apiResponse.data || []).map(item => ({
          status: item.status || 'UNKNOWN',
          totalRequests: item.total_requests || 0,
          uniqueStaffCount: item.unique_staff_count || 0
        }));

        transformedChartData = transformedTableData.map(item => ({
          name: item.status || 'Unknown',
          value: item.totalRequests || 0
        }));

        const totalRequests = transformedTableData.reduce((sum, item) => sum + (item.totalRequests || 0), 0);
        transformedSummary = {
          hoursAssigned: 0,
          teachingPercent: 0,
          adminPercent: 0,
          researchPercent: 0,
          overload: false,
          totalRequests: totalRequests
        };
      } else if (selectedReport === 'module-teaching') {
        transformedTableData = (apiResponse.data || []).map(item => ({
          programCode: item.program_code || 'N/A',
          programName: item.program_name || 'N/A',
          sectionCode: item.section_code || 'N/A',
          academicYear: item.academic_year || 'N/A',
          totalTasks: item.total_tasks || 0,
          assignedTasks: item.assigned_tasks || 0,
          totalHours: item.total_hours || 0,
          assignedHours: item.assigned_hours || 0,
          assignedStaffCount: item.assigned_staff_count || 0
        }));

        transformedChartData = transformedTableData.map(item => ({
          name: `${item.programCode} - ${item.sectionCode}`,
          hours: item.assignedHours || 0
        }));

        const totalHours = transformedTableData.reduce((sum, item) => sum + (item.assignedHours || 0), 0);
        transformedSummary = {
          hoursAssigned: totalHours || 0,
          teachingPercent: 100,
          adminPercent: 0,
          researchPercent: 0,
          overload: false
        };
      }

      const reportData = {
        reportType: selectedReport,
        filters: reportFilters,
        summary: transformedSummary,
        tableData: transformedTableData,
        chartData: transformedChartData,
        rawData: apiResponse
      };

      setReportData(reportData);
    } catch (error) {
      console.error('Error fetching report data:', error);
      alert(`Error loading report: ${error.message || 'Unknown error'}`);
    }
  };

  const handleDownloadPDF = () => {
    if (reportData) {
      downloadPDF(reportData);
    } else {
      alert('Please generate a report first before downloading.');
    }
  };

  const handleDownloadCSV = () => {
    if (reportData) {
      downloadCSV(reportData);
    } else {
      alert('Please generate a report first before downloading.');
    }
  };

  const handleBackToDashboard = () => {
    setReportData(null);
    setSelectedReport(null);
  };

  if (reportData) {
    return (
      <ReportViewer
        reportData={reportData}
        userRole={userRole}
        onBack={handleBackToDashboard}
      />
    );
  }

  return (
    <div className="reports-dashboard">
      <div className="reports-header">
        <h1 className="reports-title">
          <span className="reports-icon">📊</span>
          Reports
        </h1>
      </div>

      <div className="reports-filters-bar">
        <div className="filter-group">
          <label htmlFor="academic-period">Academic Period</label>
          <select
            id="academic-period"
            className="filter-select"
            value={filters.academicPeriod}
            onChange={(e) => setFilters({ ...filters, academicPeriod: e.target.value })}
          >
            <option value="">Select Period</option>
            <option value="2024-2025">2024-2025</option>
            <option value="2025-2026">2025-2026</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="semester">Semester</label>
          <select
            id="semester"
            className="filter-select"
            value={filters.semester}
            onChange={(e) => setFilters({ ...filters, semester: e.target.value })}
          >
            <option value="">Select Semester</option>
            <option value="2025S1">2025 Semester 1</option>
            <option value="2025S2">2025 Semester 2</option>
            <option value="2024S1">2024 Semester 1</option>
            <option value="2024S2">2024 Semester 2</option>
          </select>
        </div>

        {!isStaff && (
          <>
            <div className="filter-group">
              <label htmlFor="program">Program (Optional)</label>
              <select
                id="program"
                className="filter-select"
                value={filters.program}
                onChange={(e) => setFilters({ ...filters, program: e.target.value })}
              >
                <option value="">All Programs</option>
                <option value="1">Computer Science</option>
                <option value="2">Mathematics</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="program-section">Program Section (Optional)</label>
              <select
                id="program-section"
                className="filter-select"
                value={filters.programSection}
                onChange={(e) => setFilters({ ...filters, programSection: e.target.value })}
              >
                <option value="">All Sections</option>
                <option value="1">Section A</option>
                <option value="2">Section B</option>
              </select>
            </div>
          </>
        )}
      </div>

      <div className="reports-section">
        <h2 className="section-title">Report Categories</h2>
        <div className="reports-grid">
          {reports.map((report) => (
            <div key={report.id} className="report-card">
              <div className="report-card-header">
                <span className="report-icon">{report.icon}</span>
                <h3 className="report-card-title">{report.name}</h3>
              </div>
              <p className="report-card-description">{report.description}</p>
              <div className="report-card-actions">
                <button
                  className="action-btn view-btn"
                  onClick={() => handleViewReport(report.id)}
                >
                  🔘 View Report
                </button>
                <button
                  className="action-btn download-btn"
                  onClick={handleDownloadPDF}
                >
                  📥 Download PDF
                </button>
                <button
                  className="action-btn download-btn"
                  onClick={handleDownloadCSV}
                >
                  📄 Download CSV
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showFiltersModal && (
        <ReportFiltersModal
          reportId={selectedReport}
          initialFilters={filters}
          onGenerate={handleGenerateReport}
          onClose={() => setShowFiltersModal(false)}
        />
      )}
    </div>
  );
};

export default ReportsDashboard;
