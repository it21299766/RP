import React, { useState } from 'react';
import './ReportFiltersModal.css';

const ReportFiltersModal = ({ reportId, initialFilters, onGenerate, onClose }) => {
  const [filters, setFilters] = useState({
    semester: initialFilters.semester || '',
    program: initialFilters.program || '',
    programSection: initialFilters.programSection || '',
    staff: '',
    domains: {
      teaching: true,
      research: true,
      admin: true,
      exams: true,
      service: true
    },
    include: {
      preparationHours: true,
      markingHours: true,
      researchHours: true,
      adminHours: true
    },
    displayFormat: 'table'
  });

  const handleInputChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFilters(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      setFilters(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const handleDomainToggle = (domain) => {
    setFilters(prev => ({
      ...prev,
      domains: {
        ...prev.domains,
        [domain]: !prev.domains[domain]
      }
    }));
  };

  const handleIncludeToggle = (include) => {
    setFilters(prev => ({
      ...prev,
      include: {
        ...prev.include,
        [include]: !prev.include[include]
      }
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!filters.semester) {
      alert('Please select a semester');
      return;
    }
    onGenerate(filters);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Report Parameters</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form className="modal-form" onSubmit={handleSubmit}>
          <div className="form-section">
            <h3 className="section-title">Basic Filters</h3>
            
            <div className="form-group">
              <label htmlFor="semester">
                Semester <span className="required">*</span>
              </label>
              <select
                id="semester"
                className="form-input"
                value={filters.semester}
                onChange={(e) => handleInputChange('semester', e.target.value)}
                required
              >
                <option value="">Select Semester</option>
                <option value="Semester 1">Semester 1</option>
                <option value="Semester 2">Semester 2</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="program">Program (Optional)</label>
              <select
                id="program"
                className="form-input"
                value={filters.program}
                onChange={(e) => handleInputChange('program', e.target.value)}
              >
                <option value="">All Programs</option>
                <option value="CS">Computer Science</option>
                <option value="MATH">Mathematics</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="program-section">Program Section (Optional)</label>
              <select
                id="program-section"
                className="form-input"
                value={filters.programSection}
                onChange={(e) => handleInputChange('programSection', e.target.value)}
              >
                <option value="">All Sections</option>
                <option value="A">Section A</option>
                <option value="B">Section B</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="staff">Staff (Optional)</label>
              <select
                id="staff"
                className="form-input"
                value={filters.staff}
                onChange={(e) => handleInputChange('staff', e.target.value)}
              >
                <option value="">All Staff</option>
                <option value="1">Dr. John Smith</option>
                <option value="2">Dr. Sarah Johnson</option>
              </select>
            </div>
          </div>

          <div className="form-section">
            <h3 className="section-title">Select Domains</h3>
            <div className="checkbox-group">
              {Object.entries(filters.domains).map(([domain, checked]) => (
                <label key={domain} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => handleDomainToggle(domain)}
                  />
                  <span className="checkbox-text">
                    {domain.charAt(0).toUpperCase() + domain.slice(1)}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div className="form-section">
            <h3 className="section-title">Include</h3>
            <div className="checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.include.preparationHours}
                  onChange={() => handleIncludeToggle('preparationHours')}
                />
                <span className="checkbox-text">Preparation Hours</span>
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.include.markingHours}
                  onChange={() => handleIncludeToggle('markingHours')}
                />
                <span className="checkbox-text">Marking Hours</span>
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.include.researchHours}
                  onChange={() => handleIncludeToggle('researchHours')}
                />
                <span className="checkbox-text">Research Hours</span>
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={filters.include.adminHours}
                  onChange={() => handleIncludeToggle('adminHours')}
                />
                <span className="checkbox-text">Admin Hours</span>
              </label>
            </div>
          </div>

          <div className="form-section">
            <h3 className="section-title">Display Format</h3>
            <div className="radio-group">
              <label className="radio-label">
                <input
                  type="radio"
                  name="displayFormat"
                  value="table"
                  checked={filters.displayFormat === 'table'}
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)}
                />
                <span className="radio-text">Table</span>
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  name="displayFormat"
                  value="chart"
                  checked={filters.displayFormat === 'chart'}
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)}
                />
                <span className="radio-text">Chart</span>
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  name="displayFormat"
                  value="table+chart"
                  checked={filters.displayFormat === 'table+chart'}
                  onChange={(e) => handleInputChange('displayFormat', e.target.value)}
                />
                <span className="radio-text">Table + Chart</span>
              </label>
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-cancel" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-generate">
              Generate Report
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReportFiltersModal;

