/**
 * MetricsCard Component
 * 
 * This component displays a single metric card in the dashboard.
 * It shows a metric title, value, icon, and optionally an unassigned count.
 * 
 * Features:
 * - Icon display
 * - Title and value display
 * - Optional unassigned count (for assignment rate metric)
 * - Special styling for assignment rate cards
 * 
 * Props:
 * - title: String - Metric title (e.g., "Total Staff", "Assignment Rate")
 * - value: String|Number - Metric value to display
 * - icon: String - Emoji or icon to display
 * - unassigned: Number (optional) - Number of unassigned items (for assignment rate)
 * - isAssignmentRate: Boolean (optional) - Special styling flag for assignment rate cards
 * 
 * Usage:
 * Used in Dashboard component to display key system metrics:
 * - Total Staff
 * - Total Courses
 * - Total Assignments
 * - Assignment Rate (with unassigned count)
 * 
 * Dependencies:
 * - None (standalone card component)
 */
// Import React library for component creation
import React from 'react';
// Import CSS styles specific to this component
import './MetricsCard.css';

// Component function that receives props via destructuring
const MetricsCard = ({ title, value, icon, unassigned, isAssignmentRate }) => {
  // Return JSX structure for the metric card
  return (
    // Main container div with CSS class for styling
    <div className="metrics-card">
      {/* Header section containing icon and title */}
      <div className="metrics-card-header">
        {/* Conditional rendering: if isAssignmentRate is true, use special icon class */}
        {isAssignmentRate ? (
          // Icon span with special assignment-rate styling
          <span className="metrics-icon assignment-rate-icon">{icon}</span>
        ) : (
          // Standard icon span for non-assignment-rate metrics
          <span className="metrics-icon">{icon}</span>
        )}
        {/* Title heading displaying the metric name */}
        <h3 className="metrics-title">{title}</h3>
      </div>
      {/* Value section displaying the metric value */}
      <div className="metrics-value">{value}</div>
      {/* Conditional rendering: only show footer if unassigned count is provided */}
      {unassigned !== undefined && (
        // Footer section for additional information
        <div className="metrics-footer">
          {/* Display unassigned count with up arrow indicator */}
          <span className="unassigned-text">↑ {unassigned} unassigned</span>
        </div>
      )}
    </div>
  );
};

// Export component as default for use in other files
export default MetricsCard;

