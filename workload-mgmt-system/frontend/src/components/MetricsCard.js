import React from 'react';
import './MetricsCard.css';

const MetricsCard = ({ title, value, icon, unassigned, isAssignmentRate }) => {
  return (
    <div className="metrics-card">
      <div className="metrics-card-header">
        {isAssignmentRate ? (
          <span className="metrics-icon assignment-rate-icon">{icon}</span>
        ) : (
          <span className="metrics-icon">{icon}</span>
        )}
        <h3 className="metrics-title">{title}</h3>
      </div>
      <div className="metrics-value">{value}</div>
      {unassigned !== undefined && (
        <div className="metrics-footer">
          <span className="unassigned-text">↑ {unassigned} unassigned</span>
        </div>
      )}
    </div>
  );
};

export default MetricsCard;

