/**
 * ReportViewer Component
 * 
 * This component displays generated reports with tables, charts, and summary information.
 * It supports multiple display formats (table, chart, or both) and export functionality.
 * 
 * Features:
 * - Report summary boxes (hours assigned, percentages, overload status)
 * - Data table display with role-specific columns
 * - Pie chart for domain distribution (Teaching, Admin, Research)
 * - Bar chart for hours visualization
 * - PDF export with chart images
 * - CSV export with chart data
 * - Chart image capture using refs for PDF generation
 * 
 * Props:
 * - reportData: Object containing report data (reportType, filters, summary, tableData, chartData)
 * - userRole: String - 'Administrator' or 'Staff'
 * - onBack: Function to navigate back to reports dashboard
 * 
 * Display Formats:
 * - 'table': Shows only data table
 * - 'chart': Shows only charts
 * - 'table+chart': Shows both table and charts
 * 
 * Chart Types:
 * - Pie Chart: Domain distribution (not shown for task-assignment reports)
 * - Bar Chart: Hours per week visualization (customized for task-assignment reports)
 * 
 * Dependencies:
 * - Recharts: For chart rendering (PieChart, BarChart, etc.)
 * - reportExports: Utility functions for PDF and CSV export
 * - html2canvas: Used by reportExports to capture chart images (loaded dynamically)
 */
// Import React and useRef hook for DOM element references
import React, { useRef } from 'react';
// Import CSS styles for this component
import './ReportViewer.css';
// Import Recharts components for chart rendering
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
// Import utility functions for PDF and CSV export
import { downloadPDF, downloadCSV } from '../utils/reportExports';

// Component function that receives props via destructuring
const ReportViewer = ({ reportData, userRole, onBack }) => {
  // Destructure reportData object to extract individual properties
  const { reportType, filters, summary, tableData, chartData } = reportData;
  // Ref for pie chart DOM element (used to capture chart image for PDF)
  const pieChartRef = useRef(null);
  // Ref for bar chart DOM element (used to capture chart image for PDF)
  const barChartRef = useRef(null);

  // Array of color codes for chart elements (blue, green, orange, red, purple)
  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  /**
   * Pie Chart Data
   * Array of objects for pie chart showing domain distribution percentages
   */
  const pieData = [
    { name: 'Teaching', value: summary.teachingPercent }, // Teaching percentage
    { name: 'Admin', value: summary.adminPercent }, // Admin percentage
    { name: 'Research', value: summary.researchPercent } // Research percentage
  ];

  /**
   * Function: getBarChartData
   * Prepares data for bar chart visualization
   * For task-assignment reports, extracts data from tableData
   * For other reports, uses chartData from reportData
   * @returns {Array} - Array of objects with name and hours properties
   */
  const getBarChartData = () => {
    // Check if this is a task-assignment report and tableData exists
    if (reportType === 'task-assignment' && tableData.length > 0) {
      // Map tableData to bar chart format
      return tableData.map(item => ({
        name: item.staffName || item.taskName || 'N/A', // Use staffName, taskName, or 'N/A' as label
        hours: item.totalHours || item.hoursPerWeek || 0 // Use totalHours, hoursPerWeek, or 0 as value
      }));
    }
    // For other report types, use chartData if available, otherwise use sample data
    return chartData.length > 0 ? chartData : [{ name: 'Sample', hours: 0 }];
  };

  // Get bar chart data by calling the function
  const barChartData = getBarChartData();

  /**
   * Handler: handleDownloadPDF
   * Processes PDF download with chart image capture
   * Collects chart refs if charts are visible, waits for rendering, then exports
   */
  const handleDownloadPDF = async () => {
    // Initialize array to store chart references for image capture
    const chartRefs = [];
    // Check if charts should be displayed (chart or table+chart format)
    if ((filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart')) {
      // Wait 500ms for charts to fully render before capturing
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Add pie chart ref if it exists and report is not task-assignment (pie chart not shown for task-assignment)
      if (reportType !== 'task-assignment' && pieChartRef.current) {
        chartRefs.push(pieChartRef); // Add pie chart ref to array
      }
      // Add bar chart ref if it exists
      if (barChartRef.current) {
        chartRefs.push(barChartRef); // Add bar chart ref to array
      }
    }
    
    // Call downloadPDF utility with report data and chart refs (or null if no charts)
    await downloadPDF(reportData, chartRefs.length > 0 ? chartRefs : null);
  };

  /**
   * Handler: handleDownloadCSV
   * Processes CSV download
   * Calls downloadCSV utility with report data
   */
  const handleDownloadCSV = () => {
    // Call downloadCSV utility with report data
    downloadCSV(reportData);
  };

  /**
   * Function: getReportTitle
   * Returns the display title for the current report type
   * @returns {string} - Report title string
   */
  const getReportTitle = () => {
    // Object mapping report type IDs to display titles
    const titles = {
      'staff-workload-summary': 'Staff Workload Summary', // Staff workload summary report
      'program-teaching-load': 'Program Teaching Load Report', // Program teaching load report
      'task-assignment': 'Task Assignment Report', // Task assignment report
      'underload-overload': 'Underload/Overload Report', // Underload/overload report
      'ga-optimization': 'GA Optimization Output Report', // GA optimization report
      'change-requests': 'Change Requests Report', // Change requests report
      'module-teaching': 'Module-Level Teaching Report', // Module teaching report
      'staff-activity': 'Staff Activity Report' // Staff activity report
    };
    // Return title for current report type, or 'Report' as fallback
    return titles[reportType] || 'Report';
  };

  // Return JSX structure for the report viewer
  return (
    // Main report viewer container
    <div className="report-viewer">
      {/* Report header section with title, metadata, and download buttons */}
      <div className="report-header">
        {/* Left side of header */}
        <div className="report-header-left">
          {/* Back button to return to reports dashboard */}
          <button className="back-button" onClick={onBack}>
            {/* Left arrow and button text */}
            ← Back to Reports
          </button>
          {/* Title and metadata section */}
          <div className="report-title-section">
            {/* Report title (dynamically generated based on report type) */}
            <h1 className="report-title">{getReportTitle()}</h1>
            {/* Metadata container */}
            <div className="report-meta">
              {/* Academic period metadata item */}
              <span className="meta-item">
                {/* Label */}
                <strong>Academic Period:</strong> {/* Display academic period or 'N/A' */}
                {filters.academicPeriod || 'N/A'}
              </span>
              {/* Semester metadata item */}
              <span className="meta-item">
                {/* Label */}
                <strong>Semester:</strong> {/* Display semester */}
                {filters.semester}
              </span>
              {/* Generation timestamp metadata item */}
              <span className="meta-item">
                {/* Label */}
                <strong>Generated:</strong> {/* Display current date and time */}
                {new Date().toLocaleString()}
              </span>
            </div>
          </div>
        </div>
        {/* Right side of header */}
        <div className="report-header-right">
          {/* Download PDF button */}
          <button className="download-btn" onClick={handleDownloadPDF}>
            {/* Download icon and button text */}
            📥 Download PDF
          </button>
          {/* Download CSV button */}
          <button className="download-btn" onClick={handleDownloadCSV}>
            {/* Document icon and button text */}
            📄 Download CSV
          </button>
        </div>
      </div>

      {/* Summary boxes section displaying key metrics */}
      <div className="report-summary-boxes">
        {/* Hours Assigned summary card */}
        <div className="summary-card">
          {/* Label text */}
          <div className="summary-label">Hours Assigned</div>
          {/* Value display with 'h' suffix */}
          <div className="summary-value">{summary.hoursAssigned}h</div>
        </div>
        {/* Teaching percentage summary card */}
        <div className="summary-card">
          {/* Label text */}
          <div className="summary-label">Teaching</div>
          {/* Value display with '%' suffix */}
          <div className="summary-value">{summary.teachingPercent}%</div>
        </div>
        {/* Admin percentage summary card */}
        <div className="summary-card">
          {/* Label text */}
          <div className="summary-label">Admin</div>
          {/* Value display with '%' suffix */}
          <div className="summary-value">{summary.adminPercent}%</div>
        </div>
        {/* Research percentage summary card */}
        <div className="summary-card">
          {/* Label text */}
          <div className="summary-label">Research</div>
          {/* Value display with '%' suffix */}
          <div className="summary-value">{summary.researchPercent}%</div>
        </div>
        {/* Overload status summary card (with conditional styling) */}
        <div className={`summary-card ${summary.overload ? 'overload' : ''}`}>
          {/* Label text */}
          <div className="summary-label">Overload?</div>
          {/* Value display: 'Yes' or 'No' based on overload boolean */}
          <div className="summary-value">{summary.overload ? 'Yes' : 'No'}</div>
        </div>
      </div>

      {/* Conditional rendering: Show table if displayFormat is 'table' or 'table+chart' */}
      {(filters.displayFormat === 'table' || filters.displayFormat === 'table+chart') && (
        <div className="report-table-section">
          {/* Section title */}
          <h2 className="section-title">Report Data</h2>
          {/* Table container with scrollable content */}
          <div className="table-container">
            {/* Main report table */}
            <table className="report-table">
              {/* Table header row */}
              <thead>
                <tr>
                  {/* Conditional rendering: Different column headers for task-assignment vs other reports */}
                  {reportType === 'task-assignment' ? (
                    // Task assignment report columns
                    <>
                      <th>Task Name</th> {/* Column header for task name */}
                      <th>Staff Name</th> {/* Column header for staff name */}
                      <th>Domain</th> {/* Column header for domain */}
                      <th>Hours per Week</th> {/* Column header for hours per week */}
                      <th>Total Hours</th> {/* Column header for total hours */}
                      <th>Assignment Method</th> {/* Column header for assignment method */}
                    </>
                  ) : (
                    // Other report types columns
                    <>
                      <th>Staff Name</th> {/* Column header for staff name */}
                      <th>Domain</th> {/* Column header for domain */}
                      <th>Tasks</th> {/* Column header for number of tasks */}
                      <th>Total Hours</th> {/* Column header for total hours */}
                      <th>Teaching Hours</th> {/* Column header for teaching hours */}
                      <th>Admin Hours</th> {/* Column header for admin hours */}
                      <th>Research Hours</th> {/* Column header for research hours */}
                      <th>Status</th> {/* Column header for status */}
                    </>
                  )}
                </tr>
              </thead>
              {/* Table body with data rows */}
              <tbody>
                {/* Conditional rendering: Show data rows if tableData exists, otherwise show empty message */}
                {tableData.length > 0 ? (
                  // Map over tableData array to create table rows
                  tableData.map((row, index) => (
                    // Table row for each data item
                    <tr key={index}>
                      {/* Conditional rendering: Different cell content for task-assignment vs other reports */}
                      {reportType === 'task-assignment' ? (
                        // Task assignment report cells
                        <>
                          <td>{row.taskName || 'N/A'}</td> {/* Task name or 'N/A' */}
                          <td>{row.staffName || 'N/A'}</td> {/* Staff name or 'N/A' */}
                          <td>{row.domain || 'N/A'}</td> {/* Domain or 'N/A' */}
                          <td>{row.hoursPerWeek || 0}h/week</td> {/* Hours per week with 'h/week' suffix */}
                          <td>{row.totalHours || 0}h</td> {/* Total hours with 'h' suffix */}
                          <td>{row.assignmentMethod || 'Manual'}</td> {/* Assignment method or 'Manual' */}
                        </>
                      ) : (
                        // Other report types cells
                        <>
                          <td>{row.staffName || 'N/A'}</td> {/* Staff name or 'N/A' */}
                          <td>{row.domain || 'N/A'}</td> {/* Domain or 'N/A' */}
                          <td>{row.tasks || 0}</td> {/* Number of tasks or 0 */}
                          <td>{row.totalHours || 0}h</td> {/* Total hours with 'h' suffix */}
                          <td>{row.teachingHours || 0}h</td> {/* Teaching hours with 'h' suffix */}
                          <td>{row.adminHours || 0}h</td> {/* Admin hours with 'h' suffix */}
                          <td>{row.researchHours || 0}h</td> {/* Research hours with 'h' suffix */}
                          <td>
                            {/* Status badge with dynamic class based on status */}
                            <span className={`status-badge ${row.status || 'normal'}`}>
                              {/* Display status or 'Normal' as default */}
                              {row.status || 'Normal'}
                            </span>
                          </td>
                        </>
                      )}
                    </tr>
                  ))
                ) : (
                  // Empty state row when no data available
                  <tr>
                    {/* Cell spanning all columns (6 for task-assignment, 8 for others) */}
                    <td colSpan={reportType === 'task-assignment' ? 6 : 8} className="no-data">
                      {/* Empty state message */}
                      No data available. Please generate a report with valid filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Conditional rendering: Show charts if displayFormat is 'chart' or 'table+chart' */}
      {(filters.displayFormat === 'chart' || filters.displayFormat === 'table+chart') && (
        <div className="report-charts-section">
          {/* Section title */}
          <h2 className="section-title">Charts</h2>
          {/* Charts grid container */}
          <div className="charts-grid">
            {/* Conditional rendering: Show pie chart only if report is NOT task-assignment */}
            {reportType !== 'task-assignment' && (
              // Pie chart card with ref for image capture
              <div className="chart-card" ref={pieChartRef}>
                {/* Chart title */}
                <h3 className="chart-title">Domain Distribution</h3>
                {/* Responsive container that adapts to parent width, fixed height of 300px */}
                <ResponsiveContainer width="100%" height={300}>
                  {/* Pie chart component */}
                  <PieChart>
                    {/* Pie chart data series */}
                    <Pie
                      data={pieData} // Data array for pie chart
                      cx="50%" // X position of pie center (50% = center horizontally)
                      cy="50%" // Y position of pie center (50% = center vertically)
                      labelLine={false} // Disable label lines
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`} // Label format: "Name XX%"
                      outerRadius={80} // Outer radius of pie in pixels
                      fill="#8884d8" // Default fill color (overridden by Cell colors)
                      dataKey="value" // Property name to use for values
                    >
                      {/* Map over pieData to create colored cells */}
                      {pieData.map((entry, index) => (
                        // Individual cell with color from COLORS array
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    {/* Tooltip component for hover information */}
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Bar chart card with ref for image capture */}
            <div className="chart-card" ref={barChartRef}>
              {/* Chart title (dynamic based on report type) */}
              <h3 className="chart-title">
                {/* Conditional title: Different for task-assignment vs other reports */}
                {reportType === 'task-assignment' ? 'Hours per Week by Task/Staff' : 'Hours per Week'}
              </h3>
              {/* Responsive container that adapts to parent width, fixed height of 300px */}
              <ResponsiveContainer width="100%" height={300}>
                {/* Bar chart component */}
                <BarChart 
                  data={barChartData} // Data array for bar chart
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }} // Chart margins in pixels
                >
                  {/* Grid lines with dashed pattern, light gray color, 50% opacity */}
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
                  {/* X-axis configuration */}
                  <XAxis 
                    dataKey="name" // Use 'name' property from data objects for labels
                    angle={-45} // Rotate labels -45 degrees for readability
                    textAnchor="end" // Anchor text at end point
                    height={80} // Reserve 80px height for rotated labels
                    tick={{ fontSize: 12, fill: '#374151' }} // Tick styling (font size and color)
                  />
                  {/* Y-axis configuration */}
                  <YAxis 
                    label={{ // Y-axis label configuration
                      value: 'Hours/Week', // Label text
                      angle: -90, // Rotate label -90 degrees (vertical)
                      position: 'insideLeft', // Position label inside left side
                      style: { fontSize: 12, fill: '#374151' } // Label styling
                    }}
                    tick={{ fontSize: 12, fill: '#6b7280' }} // Tick styling
                  />
                  {/* Tooltip configuration for hover information */}
                  <Tooltip
                    contentStyle={{ // Styling for tooltip container
                      backgroundColor: '#ffffff', // White background
                      border: '1px solid #e5e7eb', // Light gray border
                      borderRadius: '8px', // Rounded corners
                      padding: '12px', // Internal padding
                      fontSize: '13px', // Font size
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' // Subtle shadow
                    }}
                    formatter={(value) => [`${value} hours/week`, 'Hours']} // Format tooltip value
                  />
                  {/* Legend component showing data series labels */}
                  <Legend />
                  {/* Bar series for hours data */}
                  <Bar 
                    dataKey="hours" // Use 'hours' property from data objects
                    fill="#2563eb" // Blue fill color
                    radius={[0, 0, 0, 0]} // Square corners (no rounding) - top-left, top-right, bottom-right, bottom-left
                    barSize={reportType === 'task-assignment' ? 30 : 25} // Bar width: 30px for task-assignment, 25px for others
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

// Export component as default for use in other files
export default ReportViewer;

