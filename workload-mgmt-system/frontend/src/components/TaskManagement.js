import React, { useState } from 'react';
import './TaskManagement.css';
import TaskTemplateManagement from './TaskTemplateManagement';
import TaskInstanceManagement from './TaskInstanceManagement';

const TaskManagement = ({ userRole = 'Administrator' }) => {
  const [activeView, setActiveView] = useState('templates'); // 'templates' or 'instances'

  return (
    <div className="task-management">
      <div className="task-header">
        <div className="task-header-left">
          <span className="task-icon">✅</span>
          <h1 className="task-title">Task Management</h1>
        </div>
      </div>

      <div className="task-view-selector" style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button
          className={`tab-button ${activeView === 'templates' ? 'active' : ''}`}
          onClick={() => setActiveView('templates')}
        >
          Task Templates
        </button>
        <button
          className={`tab-button ${activeView === 'instances' ? 'active' : ''}`}
          onClick={() => setActiveView('instances')}
        >
          Task Instances
        </button>
      </div>

      {activeView === 'templates' && (
        <TaskTemplateManagement userRole={userRole} />
      )}

      {activeView === 'instances' && (
        <TaskInstanceManagement userRole={userRole} />
      )}
    </div>
  );
};

export default TaskManagement;
