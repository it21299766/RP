import { get, post, put, del } from '../utils/api';

export const programApi = {
  getAll: () => get('/api/programs'),
  getById: (programId) => get(`/api/programs/${programId}`),
  create: (programData) => post('/api/programs', programData),
  update: (programId, programData) => put(`/api/programs/${programId}`, programData),
  delete: (programId) => del(`/api/programs/${programId}`),
};

