/**
 * ReportsDashboard Component
 * 
 * This component provides a dashboard for accessing various system reports.
 * It displays report cards based on user role and handles report generation.
 * 
 * Features:
 * - Role-based report access (Administrators see more reports than Staff)
 * - Report filtering by academic period, semester, program, and section
 * - Report generation with customizable filters
 * - PDF and CSV export functionality
 * - Modal-based filter configuration
 * - Mock data generation for demonstration
 * 
 * Props:
 * - userRole: String - 'Administrator' or 'Staff' (default: 'Administrator')
 * 
 * Report Types:
 * - Administrator Reports:
 *   - Staff Workload Summary
 *   - Program Teaching Load Report
 *   - Task Assignment Report
 *   - Underload/Overload Report
 *   - GA Optimization Output Report
 *   - Change Requests Report
 *   - Module-Level Teaching Report
 * - Staff Reports:
 *   - Staff Workload Summary
 *   - Staff Activity Report
 * 
 * Dependencies:
 * - ReportFiltersModal: Modal for configuring report parameters
 * - ReportViewer: Component for displaying generated reports
 * - reportExports: Utility functions for PDF and CSV export
 */
import React, { useState } from 'react';
import './ReportsDashboard.css';
import ReportFiltersModal from './ReportFiltersModal';
import ReportViewer from './ReportViewer';
import { downloadPDF, downloadCSV } from '../utils/reportExports';

const ReportsDashboard = ({ userRole = 'Administrator' }) => {
  const [selectedReport, setSelectedReport] = useState(null);
  const [showFiltersModal, setShowFiltersModal] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [filters, setFilters] = useState({
    academicPeriod: '',
    semester: '',
    program: '',
    programSection: ''
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
      name: 'Staff Workload Summary',
      description: 'Hours by category + overload flags',
      icon: '📊',
      availableFor: ['Administrator', 'Staff']
    },
    {
      id: 'staff-activity',
      name: 'Staff Activity Report',
      description: 'Tasks assigned to that staff',
      icon: '📋',
      availableFor: ['Staff']
    }
  ];

  const reports = isAdministrator ? adminReports : staffReports;

  const handleViewReport = (reportId) => {
    setSelectedReport(reportId);
    setShowFiltersModal(true);
  };

  const handleGenerateReport = (reportFilters) => {
    setFilters(reportFilters);
    setShowFiltersModal(false);
    
    // TODO: Fetch report data from API
    // For now, using mock data
    let mockTableData = [];
    let mockChartData = [];
    
    // Generate mock data based on report type
    if (selectedReport === 'task-assignment') {
      mockTableData = [
        { taskName: 'Review Course Materials', staffName: 'Dr. John Smith', domain: 'Teaching', hoursPerWeek: 8, totalHours: 40 },
        { taskName: 'Prepare Exam Questions', staffName: 'Dr. Sarah Johnson', domain: 'Assessment', hoursPerWeek: 5, totalHours: 20 },
        { taskName: 'Update Syllabus', staffName: 'Dr. Michael Williams', domain: 'Admin', hoursPerWeek: 3, totalHours: 15 },
        { taskName: 'Research Paper Review', staffName: 'Dr. Emily Brown', domain: 'Research', hoursPerWeek: 6, totalHours: 30 },
        { taskName: 'Student Consultation', staffName: 'Dr. David Davis', domain: 'Teaching', hoursPerWeek: 4, totalHours: 20 }
      ];
      mockChartData = mockTableData.map(item => ({
        name: `${item.taskName} - ${item.staffName}`,
        hours: item.hoursPerWeek
      }));
    } else {
      mockTableData = [
        { staffName: 'Dr. John Smith', domain: 'Teaching', tasks: 3, totalHours: 18, teachingHours: 12, adminHours: 4, researchHours: 2, status: 'normal' },
        { staffName: 'Dr. Sarah Johnson', domain: 'Teaching', tasks: 2, totalHours: 15, teachingHours: 10, adminHours: 3, researchHours: 2, status: 'normal' },
        { staffName: 'Dr. Michael Williams', domain: 'Admin', tasks: 4, totalHours: 20, teachingHours: 8, adminHours: 8, researchHours: 4, status: 'normal' }
      ];
      mockChartData = mockTableData.map(item => ({
        name: item.staffName,
        hours: item.totalHours
      }));
    }
    
    const mockData = {
      reportType: selectedReport,
      filters: reportFilters,
      summary: {
        hoursAssigned: 18,
        teachingPercent: 60,
        adminPercent: 25,
        researchPercent: 15,
        overload: false
      },
      tableData: mockTableData,
      chartData: mockChartData
    };
    
    setReportData(mockData);
  };

  const handleDownloadPDF = (reportId) => {
    // Generate mock data for the report
    let mockTableData = [];
    let mockChartData = [];
    
    if (reportId === 'task-assignment') {
      mockTableData = [
        { taskName: 'Review Course Materials', staffName: 'Dr. John Smith', domain: 'Teaching', hoursPerWeek: 8, totalHours: 40 },
        { taskName: 'Prepare Exam Questions', staffName: 'Dr. Sarah Johnson', domain: 'Assessment', hoursPerWeek: 5, totalHours: 20 },
        { taskName: 'Update Syllabus', staffName: 'Dr. Michael Williams', domain: 'Admin', hoursPerWeek: 3, totalHours: 15 }
      ];
    } else {
      mockTableData = [
        { staffName: 'Dr. John Smith', domain: 'Teaching', tasks: 3, totalHours: 18, teachingHours: 12, adminHours: 4, researchHours: 2, status: 'normal' }
      ];
    }
    
    const mockData = {
      reportType: reportId,
      filters: filters,
      summary: {
        hoursAssigned: 18,
        teachingPercent: 60,
        adminPercent: 25,
        researchPercent: 15,
        overload: false
      },
      tableData: mockTableData,
      chartData: mockChartData
    };
    
    downloadPDF(mockData);
  };

  const handleDownloadCSV = (reportId) => {
    // Generate mock data for the report
    let mockTableData = [];
    let mockChartData = [];
    
    if (reportId === 'task-assignment') {
      mockTableData = [
        { taskName: 'Review Course Materials', staffName: 'Dr. John Smith', domain: 'Teaching', hoursPerWeek: 8, totalHours: 40 },
        { taskName: 'Prepare Exam Questions', staffName: 'Dr. Sarah Johnson', domain: 'Assessment', hoursPerWeek: 5, totalHours: 20 },
        { taskName: 'Update Syllabus', staffName: 'Dr. Michael Williams', domain: 'Admin', hoursPerWeek: 3, totalHours: 15 }
      ];
    } else {
      mockTableData = [
        { staffName: 'Dr. John Smith', domain: 'Teaching', tasks: 3, totalHours: 18, teachingHours: 12, adminHours: 4, researchHours: 2, status: 'normal' }
      ];
    }
    
    const mockData = {
      reportType: reportId,
      filters: filters,
      summary: {
        hoursAssigned: 18,
        teachingPercent: 60,
        adminPercent: 25,
        researchPercent: 15,
        overload: false
      },
      tableData: mockTableData,
      chartData: mockChartData
    };
    
    downloadCSV(mockData);
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
            <option value="Semester 1">Semester 1</option>
            <option value="Semester 2">Semester 2</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="program">Program (Optional)</label>
          <select
            id="program"
            className="filter-select"
            value={filters.program}
            onChange={(e) => setFilters({ ...filters, program: e.target.value })}
          >
            <option value="">All Programs</option>
            <option value="CS">Computer Science</option>
            <option value="MATH">Mathematics</option>
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
            <option value="A">Section A</option>
            <option value="B">Section B</option>
          </select>
        </div>
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
                  onClick={() => handleDownloadPDF(report.id)}
                >
                  📥 Download PDF
                </button>
                <button
                  className="action-btn download-btn"
                  onClick={() => handleDownloadCSV(report.id)}
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

