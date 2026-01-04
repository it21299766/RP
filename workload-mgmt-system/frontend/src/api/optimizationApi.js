import { post } from '../utils/api';

export const optimizationApi = {
  run: (optimizationData) => post('/api/optimization/run', optimizationData),
};

