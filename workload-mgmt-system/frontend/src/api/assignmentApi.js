import { get, post, put, del } from '../utils/api';

export const assignmentApi = {
  getAll: () => get('/api/assignments'),
  getById: (assignmentId) => get(`/api/assignments/${assignmentId}`),
  create: (assignmentData) => post('/api/assignments', assignmentData),
  update: (assignmentId, assignmentData) => put(`/api/assignments/${assignmentId}`, assignmentData),
  delete: (assignmentId) => del(`/api/assignments/${assignmentId}`),
};

