import { get, post, put } from '../utils/api';

export const changeRequestApi = {
  getAll: () => get('/api/change-requests'),
  getById: (requestId) => get(`/api/change-requests/${requestId}`),
  create: (changeRequestData) => post('/api/change-requests', changeRequestData),
  approve: (requestId, adminComment) => put(`/api/change-requests/${requestId}/approve`, { admin_comment: adminComment || '' }),
  reject: (requestId, adminComment) => put(`/api/change-requests/${requestId}/reject`, { admin_comment: adminComment || '' }),
};

