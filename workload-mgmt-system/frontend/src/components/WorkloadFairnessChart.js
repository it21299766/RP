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
  // Calculate average
  const average = data.reduce((sum, item) => sum + (item.value || 0), 0) / data.length;
  
  // Calculate standard deviation for fairness indicator
  const variance = data.reduce((sum, item) => {
    const diff = (item.value || 0) - average;
    return sum + (diff * diff);
  }, 0) / data.length;
  const stdDev = Math.sqrt(variance);
  
  // Color function based on deviation from average
  const getBarColor = (value) => {
    const deviation = Math.abs(value - average);
    const threshold = stdDev || 1;
    
    if (deviation <= threshold * 0.5) return '#10b981'; // Green - very fair
    if (deviation <= threshold) return '#eab308'; // Yellow - fair
    if (deviation <= threshold * 1.5) return '#f59e0b'; // Orange - somewhat unfair
    return '#ef4444'; // Red - unfair
  };

  return (
    <div style={{ position: 'relative' }}>
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
            domain={[0, 'dataMax + 2']}
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
            formatter={(value) => [`${value} hours/week`, 'Workload']}
            labelFormatter={(label) => `Staff: ${label}`}
          />
          <ReferenceLine 
            y={average} 
            stroke="#6366f1" 
            strokeDasharray="5 5" 
            strokeWidth={2}
            label={{ 
              value: `Average: ${average.toFixed(1)}h`, 
              position: 'right',
              fill: '#6366f1',
              fontSize: 12,
              fontWeight: 600
            }}
          />
          <Bar
            dataKey="value"
            name="Workload"
            radius={[0, 0, 0, 0]}
            barSize={25}
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={getBarColor(entry.value || 0)} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div style={{
        position: 'absolute',
        bottom: '10px',
        right: '30px',
        fontSize: '12px',
        color: '#6b7280',
        fontWeight: 500,
        backgroundColor: '#f9fafb',
        padding: '6px 12px',
        borderRadius: '6px',
        border: '1px solid #e5e7eb'
      }}>
        <div style={{ marginBottom: '4px' }}>Average: {average.toFixed(1)}h</div>
        <div style={{ fontSize: '11px', color: '#9ca3af' }}>
          Std Dev: {stdDev.toFixed(1)}h
        </div>
      </div>
    </div>
  );
};

export default WorkloadFairnessChart;

