/**
 * Dashboard Component
 * 
 * Main dashboard page displaying system metrics and workload analytics.
 * 
 * Features:
 * - Key metrics cards (total staff, courses, assignments, assignment rate)
 * - Workload distribution chart (by staff)
 * - Workload fairness chart (comparison)
 * 
 * Data is fetched from /api/dashboard endpoint on component mount.
 */

import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import MetricsCard from './MetricsCard';
import WorkloadDistributionChart from './WorkloadDistributionChart';
import WorkloadFairnessChart from './WorkloadFairnessChart';
import { get } from '../utils/api';

const Dashboard = () => {
  // Key metrics state: summary statistics
  const [metrics, setMetrics] = useState({
    totalStaff: 0,        // Total number of staff members
    totalCourses: 0,      // Total number of courses
    totalAssignments: 0,  // Total number of task assignments
    assignmentRate: 0,    // Percentage of tasks assigned (0-100)
    unassigned: 0         // Number of unassigned tasks
  });

  // Chart data state: workload analytics
  const [workloadData, setWorkloadData] = useState([]);  // Workload distribution by staff
  const [fairnessData, setFairnessData] = useState([]);   // Workload fairness comparison

  /**
   * Effect: Load dashboard data on component mount
   * 
   * Fetches metrics and chart data from backend API.
   * On error, resets to default values (graceful degradation).
   */
  useEffect(() => {
    // Fetch data from backend API
    const loadData = async () => {
      try {
        // GET /api/dashboard returns:
        // { metrics: {...}, workloadDistribution: [...], workloadFairness: [...] }
        const data = await get('/api/dashboard');
        
        // Update state with fetched data
        setMetrics(data.metrics);
        setWorkloadData(data.workloadDistribution || []);
        setFairnessData(data.workloadFairness || []);
      } catch (error) {
        // Handle errors gracefully: log error and reset to defaults
        console.error('Error fetching dashboard data:', error);
        // Set to zero/empty if backend is not available (no hardcoded values)
        setMetrics({
          totalStaff: 0,
          totalCourses: 0,
          totalAssignments: 0,
          assignmentRate: 0.0,
          unassigned: 0
        });
        setWorkloadData([]);
        setFairnessData([]);
      }
    };

    // Load data when component mounts
    loadData();
  }, []);  // Empty dependency array: run only on mount

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <span className="dashboard-icon">📊</span>
        <h1>System Dashboard</h1>
      </header>

      <div className="key-metrics-section">
        <div className="section-header">
          <span className="section-icon">✓</span>
          <h2>Key Metrics</h2>
        </div>
        <div className="metrics-container">
          <MetricsCard
            title="Total Staff"
            value={metrics.totalStaff}
            icon="👥"
          />
          <MetricsCard
            title="Total Courses"
            value={metrics.totalCourses}
            icon="📚"
          />
          <MetricsCard
            title="Total Assignments"
            value={metrics.totalAssignments}
            icon="📄"
          />
          <MetricsCard
            title="Assignment Rate"
            value={`${metrics.assignmentRate}%`}
            icon="✓"
            unassigned={metrics.unassigned}
            isAssignmentRate={true}
          />
        </div>
      </div>

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

