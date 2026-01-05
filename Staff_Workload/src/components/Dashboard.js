/**
 * Dashboard Component
 * 
 * This is the main dashboard component that displays system-wide metrics and workload visualizations.
 * It serves as the landing page after user login and provides an overview of:
 * - Key system metrics (total staff, courses, assignments, assignment rate)
 * - Workload distribution across staff members
 * - Workload fairness analysis
 * 
 * Features:
 * - Fetches data from backend API (http://localhost:5000/api/dashboard)
 * - Falls back to mock data if backend is unavailable
 * - Displays metrics using MetricsCard components
 * - Visualizes workload data using Recharts components
 * 
 * Dependencies:
 * - MetricsCard: Displays individual metric cards
 * - WorkloadDistributionChart: Bar chart showing workload vs capacity
 * - WorkloadFairnessChart: Bar chart showing workload fairness comparison
 * 
 * State Management:
 * - metrics: Object containing key system metrics
 * - workloadData: Array of staff workload and capacity data
 * - fairnessData: Array of staff workload values for fairness analysis
 */
import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import MetricsCard from './MetricsCard';
import WorkloadDistributionChart from './WorkloadDistributionChart';
import WorkloadFairnessChart from './WorkloadFairnessChart';

const Dashboard = () => {
  /**
   * State: metrics
   * Stores key system metrics including:
   * - totalStaff: Total number of staff members in the system
   * - totalCourses: Total number of courses
   * - totalAssignments: Total number of course/staff assignments
   * - assignmentRate: Percentage of courses assigned to staff
   * - unassigned: Number of unassigned courses
   */
  const [metrics, setMetrics] = useState({
    totalStaff: 0,
    totalCourses: 0,
    totalAssignments: 0,
    assignmentRate: 0,
    unassigned: 0
  });

  /**
   * State: workloadData
   * Array of objects containing staff workload information:
   * Each object has: { name: string, workload: number, capacity: number }
   * Used by WorkloadDistributionChart to display workload vs capacity bars
   */
  const [workloadData, setWorkloadData] = useState([]);

  /**
   * State: fairnessData
   * Array of objects containing staff workload values:
   * Each object has: { name: string, value: number }
   * Used by WorkloadFairnessChart to analyze workload distribution fairness
   */
  const [fairnessData, setFairnessData] = useState([]);

  /**
   * useEffect: Data Loading
   * Runs once on component mount to fetch dashboard data from the backend API.
   * If the API call fails (backend unavailable), it falls back to mock data.
   * This ensures the dashboard always displays data even without a backend connection.
   */
  useEffect(() => {
    // Define async function to load dashboard data
    const loadData = async () => {
      try {
        // Fetch dashboard data from backend API endpoint
        const response = await fetch('http://localhost:5000/api/dashboard');
        // Parse JSON response into JavaScript object
        const data = await response.json();
        
        // Update metrics state with data from API
        setMetrics(data.metrics);
        // Update workload distribution data from API
        setWorkloadData(data.workloadDistribution);
        // Update workload fairness data from API
        setFairnessData(data.workloadFairness);
      } catch (error) {
        // Log error to console for debugging
        console.error('Error fetching dashboard data:', error);
        /**
         * Fallback: Mock Data
         * If the backend API is unavailable, use default mock data to ensure
         * the dashboard remains functional. This is useful for:
         * - Development without backend
         * - Demo purposes
         * - Graceful degradation
         */
        // Set default metrics values
        setMetrics({
          totalStaff: 5, // Total number of staff members
          totalCourses: 8, // Total number of courses
          totalAssignments: 0, // Total number of assignments
          assignmentRate: 0.0, // Assignment rate percentage
          unassigned: 8 // Number of unassigned courses
        });
        // Set default workload distribution data (staff workload vs capacity)
        setWorkloadData([
          { name: 'Dr. Smith', workload: 18, capacity: 20 }, // 18 hours workload, 20 hours capacity
          { name: 'Dr. Johnson', workload: 15, capacity: 20 }, // 15 hours workload, 20 hours capacity
          { name: 'Dr. Williams', workload: 20, capacity: 20 }, // 20 hours workload, 20 hours capacity (at max)
          { name: 'Dr. Brown', workload: 12, capacity: 20 }, // 12 hours workload, 20 hours capacity
          { name: 'Dr. Davis', workload: 16, capacity: 20 } // 16 hours workload, 20 hours capacity
        ]);
        // Set default workload fairness data (individual workload values)
        setFairnessData([
          { name: 'Dr. Smith', value: 18 }, // 18 hours per week
          { name: 'Dr. Johnson', value: 15 }, // 15 hours per week
          { name: 'Dr. Williams', value: 20 }, // 20 hours per week
          { name: 'Dr. Brown', value: 12 }, // 12 hours per week
          { name: 'Dr. Davis', value: 16 } // 16 hours per week
        ]);
      }
    };

    // Call loadData function when component mounts
    loadData();
  }, []); // Empty dependency array means this runs only once on mount

  /**
   * Render: Dashboard Layout
   * The dashboard is divided into three main sections:
   * 1. Key Metrics Section - Displays system-wide statistics
   * 2. Workload Distribution Section - Shows workload vs capacity for each staff
   * 3. Workload Fairness Section - Compares workload distribution across staff
   */
  return (
    <div className="dashboard">
      {/* Dashboard Header */}
      <header className="dashboard-header">
        <span className="dashboard-icon">📊</span>
        <h1>System Dashboard</h1>
      </header>

      {/* Key Metrics Section */}
      {/* Displays four metric cards: Total Staff, Total Courses, Total Assignments, Assignment Rate */}
      {/* Key Metrics Section - Displays four metric cards with system statistics */}
      <div className="key-metrics-section">
        {/* Section header with icon and title */}
        <div className="section-header">
          <span className="section-icon">✓</span> {/* Checkmark icon */}
          <h2>Key Metrics</h2> {/* Section title */}
        </div>
        {/* Container for metric cards in a grid layout */}
        <div className="metrics-container">
          {/* Metric card displaying total number of staff members */}
          <MetricsCard
            title="Total Staff" // Card title
            value={metrics.totalStaff} // Value from metrics state
            icon="👥" // People emoji icon
          />
          {/* Metric card displaying total number of courses */}
          <MetricsCard
            title="Total Courses" // Card title
            value={metrics.totalCourses} // Value from metrics state
            icon="📚" // Books emoji icon
          />
          {/* Metric card displaying total number of assignments */}
          <MetricsCard
            title="Total Assignments" // Card title
            value={metrics.totalAssignments} // Value from metrics state
            icon="📄" // Document emoji icon
          />
          {/* Metric card displaying assignment rate with unassigned count */}
          <MetricsCard
            title="Assignment Rate" // Card title
            value={`${metrics.assignmentRate}%`} // Percentage value with % symbol
            icon="✓" // Checkmark icon
            unassigned={metrics.unassigned} // Number of unassigned courses (shown in footer)
            isAssignmentRate={true} // Special styling flag for assignment rate card
          />
        </div>
      </div>

      {/* Workload Distribution Section */}
      {/* Displays a bar chart comparing current workload vs capacity for each staff member */}
      <div className="workload-distribution-section">
        <div className="section-header">
          <span className="section-icon">🔗</span>
          <h2>Workload Distribution</h2>
        </div>
        <p className="section-subtitle">Workload Distribution by Staff</p>
        <div className="chart-card">
          <WorkloadDistributionChart data={workloadData} />
        </div>
      </div>

      {/* Workload Fairness Section */}
      {/* Displays a bar chart showing workload distribution fairness with average reference line */}
      <div className="workload-fairness-section">
        <div className="section-header">
          <h2>Workload Fairness</h2>
        </div>
        <p className="section-subtitle">Workload Fairness Comparison</p>
        <div className="chart-card">
          <WorkloadFairnessChart data={fairnessData} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

