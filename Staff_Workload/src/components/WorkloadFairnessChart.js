/**
 * WorkloadFairnessChart Component
 * 
 * This component displays a bar chart analyzing workload fairness across staff members.
 * It shows individual workloads with a reference line for the average and color coding
 * based on deviation from the average.
 * 
 * Features:
 * - Single bar per staff member showing their workload
 * - Average reference line (dashed) with label
 * - Color-coded bars based on deviation from average:
 *   - Green: Very fair (within 0.5 standard deviations)
 *   - Yellow: Fair (within 1 standard deviation)
 *   - Orange: Somewhat unfair (within 1.5 standard deviations)
 *   - Red: Unfair (beyond 1.5 standard deviations)
 * - Statistics display (average and standard deviation)
 * - Responsive container
 * - Square-ended bars (no rounded corners)
 * - Customizable bar size (25px)
 * 
 * Props:
 * - data: Array of objects with structure:
 *   - name: String - Staff member name
 *   - value: Number - Workload in hours/week
 * 
 * Statistical Calculations:
 * - Average: Mean of all workload values
 * - Standard Deviation: Measures spread of workload distribution
 * - Deviation Thresholds: Used to determine fairness color coding
 * 
 * Color Logic:
 * The bar color is determined by how far the staff member's workload deviates
 * from the average, relative to the standard deviation:
 * - deviation = |value - average|
 * - Colors change at thresholds: 0.5σ, 1σ, 1.5σ
 * 
 * Chart Configuration:
 * - X-axis: Staff member names (angled -45 degrees)
 * - Y-axis: Hours per week (with label)
 * - Reference Line: Average workload (dashed blue line)
 * - Statistics Box: Shows average and standard deviation in bottom-right corner
 * 
 * Usage:
 * Used in Dashboard component to visualize workload fairness and identify
 * staff members with significantly different workloads.
 * 
 * Dependencies:
 * - Recharts: For chart rendering (BarChart, Bar, XAxis, YAxis, ReferenceLine, etc.)
 */
import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine
} from 'recharts';

const WorkloadFairnessChart = ({ data }) => {
  /**
   * Calculate Average Workload
   * Computes the mean workload across all staff members
   * Uses reduce to sum all values, then divides by count
   */
  const average = data.reduce((sum, item) => sum + (item.value || 0), 0) / data.length;
  
  /**
   * Calculate Standard Deviation
   * Computes the standard deviation to measure workload distribution spread
   * Used to determine fairness thresholds for color coding
   * Formula: sqrt(sum((x - mean)^2) / n)
   */
  const variance = data.reduce((sum, item) => {
    // Calculate difference from average for each data point
    const diff = (item.value || 0) - average;
    // Sum the squared differences (variance calculation)
    return sum + (diff * diff);
  }, 0) / data.length; // Divide by number of items to get variance
  // Calculate standard deviation as square root of variance
  const stdDev = Math.sqrt(variance);
  
  /**
   * Function: getBarColor
   * Determines bar color based on deviation from average workload
   * Uses standard deviation as a threshold for fairness classification
   * @param {number} value - Staff member's workload in hours/week
   * @returns {string} - Hex color code
   */
  const getBarColor = (value) => {
    // Calculate absolute deviation from average (how far from mean)
    const deviation = Math.abs(value - average);
    // Use standard deviation as threshold, default to 1 if stdDev is 0
    const threshold = stdDev || 1;
    
    // Return green if deviation is within 0.5 standard deviations (very fair distribution)
    if (deviation <= threshold * 0.5) return '#10b981'; // Green - very fair
    // Return yellow if deviation is within 1 standard deviation (fair distribution)
    if (deviation <= threshold) return '#eab308'; // Yellow - fair
    // Return orange if deviation is within 1.5 standard deviations (somewhat unfair)
    if (deviation <= threshold * 1.5) return '#f59e0b'; // Orange - somewhat unfair
    // Return red if deviation exceeds 1.5 standard deviations (unfair distribution)
    return '#ef4444'; // Red - unfair
  };

  // Return JSX structure for the chart
  return (
    // Outer div with relative positioning for absolute-positioned statistics box
    <div style={{ position: 'relative' }}>
      {/* Responsive container that adapts to parent width, fixed height of 400px */}
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
            domain={[0, 'dataMax + 2']} // Y-axis range: 0 to max value + 2 for padding
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
            formatter={(value) => [`${value} hours/week`, 'Workload']} // Format tooltip value
            labelFormatter={(label) => `Staff: ${label}`} // Format tooltip label
          />
          {/* Reference line showing average workload */}
          <ReferenceLine 
            y={average} // Y position at average value
            stroke="#6366f1" // Indigo stroke color
            strokeDasharray="5 5" // Dashed line pattern (5px dash, 5px gap)
            strokeWidth={2} // Line width of 2 pixels
            label={{ // Label configuration for reference line
              value: `Average: ${average.toFixed(1)}h`, // Label text with 1 decimal place
              position: 'right', // Position label on right side
              fill: '#6366f1', // Label text color (indigo)
              fontSize: 12, // Font size
              fontWeight: 600 // Semi-bold font weight
            }}
          />
          {/* Bar series for workload data */}
          <Bar
            dataKey="value" // Use 'value' property from data objects
            name="Workload" // Display name in tooltip
            radius={[0, 0, 0, 0]} // Square corners (no rounding)
            barSize={25} // Fixed bar width of 25 pixels
          >
            {/* Map over data to create individual colored cells */}
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} // Unique key for React list rendering
                fill={getBarColor(entry.value || 0)} // Color based on deviation from average
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      {/* Statistics box positioned absolutely in bottom-right corner */}
      <div style={{
        position: 'absolute', // Absolute positioning relative to parent
        bottom: '10px', // 10px from bottom
        right: '30px', // 30px from right
        fontSize: '12px', // Font size
        color: '#6b7280', // Gray text color
        fontWeight: 500, // Medium font weight
        backgroundColor: '#f9fafb', // Light gray background
        padding: '6px 12px', // Internal padding
        borderRadius: '6px', // Rounded corners
        border: '1px solid #e5e7eb' // Light gray border
      }}>
        {/* Display average workload with 1 decimal place */}
        <div style={{ marginBottom: '4px' }}>Average: {average.toFixed(1)}h</div>
        {/* Display standard deviation with 1 decimal place, smaller font */}
        <div style={{ fontSize: '11px', color: '#9ca3af' }}>
          Std Dev: {stdDev.toFixed(1)}h
        </div>
      </div>
    </div>
  );
};

export default WorkloadFairnessChart;

