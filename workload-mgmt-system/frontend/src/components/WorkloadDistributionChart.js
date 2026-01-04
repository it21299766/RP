import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

const WorkloadDistributionChart = ({ data }) => {
  // Color function based on workload percentage
  const getBarColor = (workload, capacity) => {
    const percentage = (workload / capacity) * 100;
    if (percentage >= 90) return '#ef4444'; // Red for over 90%
    if (percentage >= 75) return '#f59e0b'; // Orange for 75-90%
    if (percentage >= 50) return '#eab308'; // Yellow for 50-75%
    return '#10b981'; // Green for under 50%
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
        <XAxis
          dataKey="name"
          angle={-45}
          textAnchor="end"
          height={80}
          tick={{ fontSize: 12, fill: '#374151' }}
          interval={0}
        />
        <YAxis
          label={{ 
            value: 'Hours/Week', 
            angle: -90, 
            position: 'insideLeft', 
            style: { fontSize: 12, fill: '#374151' } 
          }}
          tick={{ fontSize: 12, fill: '#6b7280' }}
          domain={[0, 'dataMax + 5']}
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
          formatter={(value, name) => {
            if (name === 'workload') {
              return [`${value} hours`, 'Current Workload'];
            }
            return [`${value} hours`, 'Capacity'];
          }}
        />
        <Legend 
          wrapperStyle={{ paddingTop: '20px' }}
          iconType="rect"
        />
        <Bar
          dataKey="workload"
          name="Current Workload"
          radius={[0, 0, 0, 0]}
          barSize={25}
        >
          {data.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={getBarColor(entry.workload, entry.capacity || 20)} 
            />
          ))}
        </Bar>
        <Bar
          dataKey="capacity"
          name="Capacity"
          fill="#cbd5e1"
          radius={[0, 0, 0, 0]}
          opacity={0.3}
          barSize={25}
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default WorkloadDistributionChart;

