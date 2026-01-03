/**
 * WorkloadDistributionChart Component
 * 
 * This component displays a bar chart comparing current workload vs capacity for each staff member.
 * It uses color coding to indicate workload levels relative to capacity.
 * 
 * Features:
 * - Dual bar display (workload and capacity)
 * - Color-coded bars based on workload percentage:
 *   - Green: < 50% capacity
 *   - Yellow: 50-75% capacity
 *   - Orange: 75-90% capacity
 *   - Red: ≥ 90% capacity (overload warning)
 * - Responsive container that adapts to parent size
 * - Interactive tooltips showing detailed information
 * - Square-ended bars (no rounded corners)
 * - Customizable bar size (25px)
 * 
 * Props:
 * - data: Array of objects with structure:
 *   - name: String - Staff member name
 *   - workload: Number - Current workload in hours/week
 *   - capacity: Number - Maximum capacity in hours/week
 * 
 * Chart Configuration:
 * - X-axis: Staff member names (angled -45 degrees)
 * - Y-axis: Hours per week (with label)
 * - Bars: Two bars per staff (workload in color, capacity in gray with opacity)
 * - Grid: Dashed grid lines for readability
 * 
 * Color Logic:
 * The workload bar color is determined by the percentage of capacity used:
 * - percentage = (workload / capacity) * 100
 * - Colors change at thresholds: 50%, 75%, 90%
 * 
 * Usage:
 * Used in Dashboard component to visualize workload distribution across staff.
 * 
 * Dependencies:
 * - Recharts: For chart rendering (BarChart, Bar, XAxis, YAxis, etc.)
 */
// Import React library for component creation
import React from 'react';
// Import Recharts components for bar chart rendering
import {
  BarChart, // Main bar chart container component
  Bar, // Individual bar component for data visualization
  XAxis, // Horizontal axis component
  YAxis, // Vertical axis component
  CartesianGrid, // Grid lines component for chart background
  Tooltip, // Interactive tooltip component
  Legend, // Legend component for data series labels
  ResponsiveContainer, // Wrapper that makes chart responsive to container size
  Cell // Individual cell component for custom bar coloring
} from 'recharts';

// Component function that receives data array as prop
const WorkloadDistributionChart = ({ data }) => {
  /**
   * Function: getBarColor
   * Determines bar color based on workload percentage of capacity
   * @param {number} workload - Current workload in hours/week
   * @param {number} capacity - Maximum capacity in hours/week
   * @returns {string} - Hex color code
   */
  const getBarColor = (workload, capacity) => {
    // Calculate percentage of capacity being used
    const percentage = (workload / capacity) * 100;
    // Return red color if workload is 90% or more of capacity (overload warning)
    if (percentage >= 90) return '#ef4444'; // Red for over 90%
    // Return orange color if workload is 75-90% of capacity (high usage)
    if (percentage >= 75) return '#f59e0b'; // Orange for 75-90%
    // Return yellow color if workload is 50-75% of capacity (moderate usage)
    if (percentage >= 50) return '#eab308'; // Yellow for 50-75%
    // Return green color if workload is less than 50% of capacity (low usage)
    return '#10b981'; // Green for under 50%
  };

  // Return JSX structure for the chart
  return (
    // Responsive container that adapts to parent width, fixed height of 400px
    <ResponsiveContainer width="100%" height={400}>
      {/* Main bar chart component with data and margins */}
      <BarChart
        data={data} // Pass data array to chart
        margin={{ top: 20, right: 30, left: 20, bottom: 60 }} // Chart margins in pixels
      >
        {/* Grid lines with dashed pattern, light gray color, 50% opacity */}
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
        {/* X-axis configuration for staff names */}
        <XAxis
          dataKey="name" // Use 'name' property from data objects for labels
          angle={-45} // Rotate labels -45 degrees for readability
          textAnchor="end" // Anchor text at end point
          height={80} // Reserve 80px height for rotated labels
          tick={{ fontSize: 12, fill: '#374151' }} // Tick styling (font size and color)
          interval={0} // Show all labels (no skipping)
        />
        {/* Y-axis configuration for hours */}
        <YAxis
          label={{ // Y-axis label configuration
            value: 'Hours/Week', // Label text
            angle: -90, // Rotate label -90 degrees (vertical)
            position: 'insideLeft', // Position label inside left side
            style: { fontSize: 12, fill: '#374151' } // Label styling
          }}
          tick={{ fontSize: 12, fill: '#6b7280' }} // Tick styling
          domain={[0, 'dataMax + 5']} // Y-axis range: 0 to max value + 5 for padding
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
          formatter={(value, name) => { // Custom formatter function
            // If data series is 'workload', format as "X hours" with label "Current Workload"
            if (name === 'workload') {
              return [`${value} hours`, 'Current Workload'];
            }
            // Otherwise format as "X hours" with label "Capacity"
            return [`${value} hours`, 'Capacity'];
          }}
        />
        {/* Legend component showing data series labels */}
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }} // Add top padding
          iconType="rect" // Use rectangle icons for legend
        />
        {/* Bar series for workload data */}
        <Bar
          dataKey="workload" // Use 'workload' property from data objects
          name="Current Workload" // Display name in legend
          radius={[0, 0, 0, 0]} // Square corners (no rounding) - top-left, top-right, bottom-right, bottom-left
          barSize={25} // Fixed bar width of 25 pixels
        >
          {/* Map over data to create individual colored cells */}
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} // Unique key for React list rendering
              fill={getBarColor(entry.workload, entry.capacity || 20)} // Color based on percentage (default capacity 20 if missing)
            />
          ))}
        </Bar>
        {/* Bar series for capacity data (background reference) */}
        <Bar
          dataKey="capacity" // Use 'capacity' property from data objects
          name="Capacity" // Display name in legend
          fill="#cbd5e1" // Light gray fill color
          radius={[0, 0, 0, 0]} // Square corners
          opacity={0.3} // 30% opacity for subtle background effect
          barSize={25} // Fixed bar width matching workload bars
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

// Export component as default for use in other files
export default WorkloadDistributionChart;

