import { get, post, put, del } from '../utils/api';

export const staffApi = {
  getAll: () => get('/api/staff'),
  getById: (staffId) => get(`/api/staff/${staffId}`),
  create: (staffData) => post('/api/staff', staffData),
  update: (staffId, staffData) => put(`/api/staff/${staffId}`, staffData),
  delete: (staffId) => del(`/api/staff/${staffId}`),
  uploadProfilePicture: (staffId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return post(`/api/staff/${staffId}/profile-picture`, formData);
  },
  deleteProfilePicture: (staffId) => del(`/api/staff/${staffId}/profile-picture`),
  updatePassword: (staffId, currentPassword, newPassword) => 
    put(`/api/staff/${staffId}/password`, { current_password: currentPassword, new_password: newPassword }),
};

