import { get } from '../utils/api';

export const workloadApi = {
  getMyAssignments: () => get('/api/workload/my-assignments'),
};

