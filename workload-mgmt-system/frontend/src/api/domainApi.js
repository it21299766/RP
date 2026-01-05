import { get, post, put, del } from '../utils/api';

export const domainApi = {
  getAll: () => get('/api/domains'),
  getById: (domainId) => get(`/api/domains/${domainId}`),
  create: (domainData) => post('/api/domains', domainData),
  update: (domainId, domainData) => put(`/api/domains/${domainId}`, domainData),
  delete: (domainId) => del(`/api/domains/${domainId}`),
};

