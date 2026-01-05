import { get, post, put, del } from '../utils/api';

export const taskTemplateApi = {
  getAll: (activeOnly = false) => get(`/api/task-templates?active_only=${activeOnly}`),
  getById: (templateId) => get(`/api/task-templates/${templateId}`),
  create: (templateData) => post('/api/task-templates', templateData),
  update: (templateId, templateData) => put(`/api/task-templates/${templateId}`, templateData),
  delete: (templateId) => del(`/api/task-templates/${templateId}`),
};

