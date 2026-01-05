import React, { useRef } from 'react';
import './ReportViewer.css';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { downloadPDF, downloadCSV } from '../utils/reportExports';

const ReportViewer = ({ reportData, userRole, onBack }) => {
  const { reportType, filters, summary, tableData, chartData } = reportData;
  const pieChartRef = useRef(null);
  const barChartRef = useRef(null);

  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  const pieData = [
    { name: 'Teaching', value: summary.teachingPercent || 0 },
    { name: 'Admin', value: summary.adminPercent || 0 },
    { name: 'Research', value: summary.researchPercent || 0 }
  ];

  // Prepare bar chart data
  const getBarChartData = () => {
    if (reportType === 'underload-overload' || reportType === 'change-requests') {
      // For distribution reports, use value instead of hours
      return chartData.map(item => ({
        name: item.name || 'Unknown',
        value: item.value || item.hours || 0
      }));
    }
    return chartData.length > 0 ? chartData : [{ name: 'Sample', hours: 0 }];
  };

  const barChartData = getBarChartData();

  const handleDownloadPDF = async () => {
    const chartRefs = [];
    if ((filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart')) {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      if (reportType !== 'task-assignment' && pieChartRef.current) {
        chartRefs.push(pieChartRef);
      }
      if (barChartRef.current) {
        chartRefs.push(barChartRef);
      }
    }
    
    await downloadPDF(reportData, chartRefs.length > 0 ? chartRefs : null);
  };

  const handleDownloadCSV = () => {
    downloadCSV(reportData);
  };

  const getReportTitle = () => {
    const titles = {
      'staff-workload-summary': 'Staff Workload Summary',
      'program-teaching-load': 'Program Teaching Load Report',
      'task-assignment': 'Task Assignment Report',
      'underload-overload': 'Underload/Overload Report',
      'ga-optimization': 'GA Optimization Output Report',
      'change-requests': 'Change Requests Report',
      'module-teaching': 'Module-Level Teaching Report',
      'staff-activity': 'Staff Activity Report'
    };
    return titles[reportType] || 'Report';
  };

  // Get table headers and render function based on report type
  const getTableHeaders = () => {
    switch (reportType) {
      case 'program-teaching-load':
        return (
          <>
            <th>Program Code</th>
            <th>Program Name</th>
            <th>Domain</th>
            <th>Total Tasks</th>
            <th>Assigned Tasks</th>
            <th>Unassigned Tasks</th>
            <th>Total Hours</th>
            <th>Assigned Hours</th>
          </>
        );
      case 'task-assignment':
        return (
          <>
            <th>Staff Name</th>
            <th>Task Type</th>
            <th>Hours</th>
            <th>Task Count</th>
          </>
        );
      case 'underload-overload':
        return (
          <>
            <th>Workload Status</th>
            <th>Staff Count</th>
          </>
        );
      case 'ga-optimization':
        return (
          <>
            <th>Metric</th>
            <th>Value</th>
          </>
        );
      case 'change-requests':
        return (
          <>
            <th>Status</th>
            <th>Total Requests</th>
            <th>Unique Staff</th>
          </>
        );
      case 'module-teaching':
        return (
          <>
            <th>Program Code</th>
            <th>Program Name</th>
            <th>Section Code</th>
            <th>Academic Year</th>
            <th>Total Tasks</th>
            <th>Assigned Tasks</th>
            <th>Total Hours</th>
            <th>Assigned Hours</th>
            <th>Assigned Staff</th>
          </>
        );
      default: // staff-workload-summary
        return (
          <>
            <th>Staff Name</th>
            <th>Domain</th>
            <th>Tasks</th>
            <th>Total Hours</th>
            <th>Teaching Hours</th>
            <th>Admin Hours</th>
            <th>Research Hours</th>
            <th>Status</th>
          </>
        );
    }
  };

  const getTableRows = () => {
    if (tableData.length === 0) {
      return (
        <tr>
          <td colSpan={8} className="no-data">
            No data available. Please generate a report with valid filters.
          </td>
        </tr>
      );
    }

    return tableData.map((row, index) => {
      switch (reportType) {
        case 'program-teaching-load':
          return (
            <tr key={index}>
              <td>{row.programCode || 'N/A'}</td>
              <td>{row.programName || 'N/A'}</td>
              <td>{row.domain || 'N/A'}</td>
              <td>{row.totalTasks || 0}</td>
              <td>{row.assignedTasks || 0}</td>
              <td>{row.unassignedTasks || 0}</td>
              <td>{row.totalHours || 0}h</td>
              <td>{row.assignedHours || 0}h</td>
            </tr>
          );
        case 'task-assignment':
          return (
            <tr key={index}>
              <td>{row.staffName || 'N/A'}</td>
              <td>{row.taskType || 'N/A'}</td>
              <td>{row.hours || 0}h</td>
              <td>{row.taskCount || 0}</td>
            </tr>
          );
        case 'underload-overload':
          return (
            <tr key={index}>
              <td>
                <span className={`status-badge ${(row.status || '').toLowerCase()}`}>
                  {row.status || 'UNKNOWN'}
                </span>
              </td>
              <td>{row.staffCount || 0}</td>
            </tr>
          );
        case 'ga-optimization':
          // GA optimization is a single row with summary data
          const gaRow = row;
          return (
            <React.Fragment key={index}>
              <tr>
                <td>Total Assigned Tasks</td>
                <td>{gaRow.total_assigned_tasks || 0}</td>
              </tr>
              <tr>
                <td>Total Staff with Assignments</td>
                <td>{gaRow.total_staff_with_assignments || 0}</td>
              </tr>
              <tr>
                <td>Total Task Instances</td>
                <td>{gaRow.total_task_instances || 0}</td>
              </tr>
              <tr>
                <td>Total Assigned Hours</td>
                <td>{gaRow.total_assigned_hours || 0}h</td>
              </tr>
              <tr>
                <td>Average Hours per Task</td>
                <td>{gaRow.average_hours_per_task || 0}h</td>
              </tr>
              <tr>
                <td>System Assignments</td>
                <td>{gaRow.system_assignments || 0}</td>
              </tr>
              <tr>
                <td>Admin Assignments</td>
                <td>{gaRow.admin_assignments || 0}</td>
              </tr>
            </React.Fragment>
          );
        case 'change-requests':
          return (
            <tr key={index}>
              <td>
                <span className={`status-badge ${(row.status || '').toLowerCase()}`}>
                  {row.status || 'UNKNOWN'}
                </span>
              </td>
              <td>{row.totalRequests || 0}</td>
              <td>{row.uniqueStaffCount || 0}</td>
            </tr>
          );
        case 'module-teaching':
          return (
            <tr key={index}>
              <td>{row.programCode || 'N/A'}</td>
              <td>{row.programName || 'N/A'}</td>
              <td>{row.sectionCode || 'N/A'}</td>
              <td>{row.academicYear || 'N/A'}</td>
              <td>{row.totalTasks || 0}</td>
              <td>{row.assignedTasks || 0}</td>
              <td>{row.totalHours || 0}h</td>
              <td>{row.assignedHours || 0}h</td>
              <td>{row.assignedStaffCount || 0}</td>
            </tr>
          );
        default: // staff-workload-summary
          return (
            <tr key={index}>
              <td>{row.staffName || 'N/A'}</td>
              <td>{row.domain || 'N/A'}</td>
              <td>{row.tasks || 0}</td>
              <td>{row.totalHours || 0}h</td>
              <td>{row.teachingHours || 0}h</td>
              <td>{row.adminHours || 0}h</td>
              <td>{row.researchHours || 0}h</td>
              <td>
                <span className={`status-badge ${(row.status || 'normal').toLowerCase()}`}>
                  {row.status || 'Normal'}
                </span>
              </td>
            </tr>
          );
      }
    });
  };

  const getColSpan = () => {
    switch (reportType) {
      case 'program-teaching-load':
        return 8;
      case 'task-assignment':
        return 4;
      case 'underload-overload':
        return 2;
      case 'ga-optimization':
        return 2;
      case 'change-requests':
        return 3;
      case 'module-teaching':
        return 9;
      default:
        return 8;
    }
  };

  return (
    <div className="report-viewer">
      <div className="report-header">
        <div className="report-header-left">
          <button className="back-button" onClick={onBack}>
            ← Back to Reports
          </button>
          <div className="report-title-section">
            <h1 className="report-title">{getReportTitle()}</h1>
            <div className="report-meta">
              <span className="meta-item">
                <strong>Academic Period:</strong> {filters.academicPeriod || 'N/A'}
              </span>
              <span className="meta-item">
                <strong>Semester:</strong> {filters.semester}
              </span>
              <span className="meta-item">
                <strong>Generated:</strong> {new Date().toLocaleString()}
              </span>
            </div>
          </div>
        </div>
        <div className="report-header-right">
          <button className="download-btn" onClick={handleDownloadPDF}>
            📥 Download PDF
          </button>
          <button className="download-btn" onClick={handleDownloadCSV}>
            📄 Download CSV
          </button>
        </div>
      </div>

      <div className="report-summary-boxes">
        <div className="summary-card">
          <div className="summary-label">Hours Assigned</div>
          <div className="summary-value">{summary.hoursAssigned || 0}h</div>
        </div>
        {reportType !== 'underload-overload' && reportType !== 'change-requests' && reportType !== 'ga-optimization' && (
          <>
            <div className="summary-card">
              <div className="summary-label">Teaching</div>
              <div className="summary-value">{summary.teachingPercent || 0}%</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Admin</div>
              <div className="summary-value">{summary.adminPercent || 0}%</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Research</div>
              <div className="summary-value">{summary.researchPercent || 0}%</div>
            </div>
            <div className={`summary-card ${summary.overload ? 'overload' : ''}`}>
              <div className="summary-label">Overload?</div>
              <div className="summary-value" style={{fontSize: '1rem'}}>{summary.overload ? 'Yes' : 'No'}</div>
            </div>
          </>
        )}
        {reportType === 'ga-optimization' && (
          <>
            <div className="summary-card">
              <div className="summary-label">Total Tasks</div>
              <div className="summary-value">{summary.totalAssignedTasks || 0}</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Total Staff</div>
              <div className="summary-value">{summary.totalStaff || 0}</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">System Assignments</div>
              <div className="summary-value">{summary.systemAssignments || 0}</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Admin Assignments</div>
              <div className="summary-value">{summary.adminAssignments || 0}</div>
            </div>
          </>
        )}
        {reportType === 'change-requests' && summary.totalRequests !== undefined && (
          <div className="summary-card">
            <div className="summary-label">Total Requests</div>
            <div className="summary-value">{summary.totalRequests || 0}</div>
          </div>
        )}
      </div>

      {(filters.displayFormat === 'table' || filters.displayFormat === 'table+chart') && (
        <div className="report-table-section">
          <h2 className="section-title">Report Data</h2>
          <div className="table-container">
            <table className="report-table">
              <thead>
                <tr>
                  {getTableHeaders()}
                </tr>
              </thead>
              <tbody>
                {getTableRows()}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart') && (
        <div className="report-charts-section">
          <h2 className="section-title">Visualizations</h2>
          <div className="charts-container">
            {reportType !== 'task-assignment' && reportType !== 'underload-overload' && reportType !== 'change-requests' && reportType !== 'ga-optimization' && (
              <div className="chart-card" ref={pieChartRef}>
                <h3>Workload Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}

            <div className="chart-card" ref={barChartRef}>
              <h3>
                {reportType === 'underload-overload' || reportType === 'change-requests' 
                  ? 'Distribution' 
                  : reportType === 'ga-optimization'
                  ? 'Assignment Method Comparison'
                  : 'Hours by ' + (reportType === 'task-assignment' ? 'Task Type' : 'Program/Staff')}
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  data={barChartData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {reportType === 'underload-overload' || reportType === 'change-requests' ? (
                    <Bar dataKey="value" fill="#8884d8" />
                  ) : (
                    <Bar dataKey="hours" fill="#8884d8" />
                  )}
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportViewer;
