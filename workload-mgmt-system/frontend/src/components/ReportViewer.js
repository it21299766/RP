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
    { name: 'Teaching', value: summary.teachingPercent },
    { name: 'Admin', value: summary.adminPercent },
    { name: 'Research', value: summary.researchPercent }
  ];

  // Prepare bar chart data for task assignment report
  const getBarChartData = () => {
    if (reportType === 'task-assignment' && tableData.length > 0) {
      return tableData.map(item => ({
        name: item.staffName || item.taskName || 'N/A',
        hours: item.totalHours || item.hoursPerWeek || 0
      }));
    }
    return chartData.length > 0 ? chartData : [{ name: 'Sample', hours: 0 }];
  };

  const barChartData = getBarChartData();

  const handleDownloadPDF = async () => {
    // Collect chart container references only if charts are visible
    const chartRefs = [];
    if ((filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart')) {
      // Wait a bit for charts to fully render
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
          <div className="summary-value">{summary.hoursAssigned}h</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Teaching</div>
          <div className="summary-value">{summary.teachingPercent}%</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Admin</div>
          <div className="summary-value">{summary.adminPercent}%</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Research</div>
          <div className="summary-value">{summary.researchPercent}%</div>
        </div>
        <div className={`summary-card ${summary.overload ? 'overload' : ''}`}>
          <div className="summary-label">Overload?</div>
          <div className="summary-value">{summary.overload ? 'Yes' : 'No'}</div>
        </div>
      </div>

      {(filters.displayFormat === 'table' || filters.displayFormat === 'table+chart') && (
        <div className="report-table-section">
          <h2 className="section-title">Report Data</h2>
          <div className="table-container">
            <table className="report-table">
              <thead>
                <tr>
                  {reportType === 'task-assignment' ? (
                    <>
                      <th>Task Name</th>
                      <th>Staff Name</th>
                      <th>Domain</th>
                      <th>Hours per Week</th>
                      <th>Total Hours</th>
                      <th>Assignment Method</th>
                    </>
                  ) : (
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
                  )}
                </tr>
              </thead>
              <tbody>
                {tableData.length > 0 ? (
                  tableData.map((row, index) => (
                    <tr key={index}>
                      {reportType === 'task-assignment' ? (
                        <>
                          <td>{row.taskName || 'N/A'}</td>
                          <td>{row.staffName || 'N/A'}</td>
                          <td>{row.domain || 'N/A'}</td>
                          <td>{row.hoursPerWeek || 0}h/week</td>
                          <td>{row.totalHours || 0}h</td>
                          <td>{row.assignmentMethod || 'Manual'}</td>
                        </>
                      ) : (
                        <>
                          <td>{row.staffName || 'N/A'}</td>
                          <td>{row.domain || 'N/A'}</td>
                          <td>{row.tasks || 0}</td>
                          <td>{row.totalHours || 0}h</td>
                          <td>{row.teachingHours || 0}h</td>
                          <td>{row.adminHours || 0}h</td>
                          <td>{row.researchHours || 0}h</td>
                          <td>
                            <span className={`status-badge ${row.status || 'normal'}`}>
                              {row.status || 'Normal'}
                            </span>
                          </td>
                        </>
                      )}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={reportType === 'task-assignment' ? 6 : 8} className="no-data">
                      No data available. Please generate a report with valid filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart') && (
        <div className="report-charts-section">
          <h2 className="section-title">Charts</h2>
          <div className="charts-grid">
            {reportType !== 'task-assignment' && (
              <div className="chart-card" ref={pieChartRef}>
                <h3 className="chart-title">Domain Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}

            <div className="chart-card" ref={barChartRef}>
              <h3 className="chart-title">
                {reportType === 'task-assignment' ? 'Hours per Week by Task/Staff' : 'Hours per Week'}
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart 
                  data={barChartData}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
                  <XAxis 
                    dataKey="name" 
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    tick={{ fontSize: 12, fill: '#374151' }}
                  />
                  <YAxis 
                    label={{ 
                      value: 'Hours/Week', 
                      angle: -90, 
                      position: 'insideLeft',
                      style: { fontSize: 12, fill: '#374151' }
                    }}
                    tick={{ fontSize: 12, fill: '#6b7280' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      padding: '12px',
                      fontSize: '13px',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                    }}
                    formatter={(value) => [`${value} hours/week`, 'Hours']}
                  />
                  <Legend />
                  <Bar 
                    dataKey="hours" 
                    fill="#2563eb"
                    radius={[0, 0, 0, 0]}
                    barSize={reportType === 'task-assignment' ? 30 : 25}
                  />
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

