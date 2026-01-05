import { get, post, put, del } from '../utils/api';

export const taskInstanceApi = {
  getAll: (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status', filters.status);
    if (filters.semester) params.append('semester', filters.semester);
    if (filters.academic_year) params.append('academic_year', filters.academic_year);
    const queryString = params.toString();
    return get(`/api/task-instances${queryString ? '?' + queryString : ''}`);
  },
  getApproved: () => get('/api/task-instances/approved'),
  getById: (instanceId) => get(`/api/task-instances/${instanceId}`),
  create: (instanceData) => post('/api/task-instances', instanceData),
  update: (instanceId, instanceData) => put(`/api/task-instances/${instanceId}`, instanceData),
  approve: (instanceId) => post(`/api/task-instances/${instanceId}/approve`),
  delete: (instanceId) => del(`/api/task-instances/${instanceId}`),
};

