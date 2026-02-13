import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1', // The base URL is proxied by Vite to the backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add the token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const api = {
  // Auth
  login(username, password) {
    return apiClient.post('/auth/login', { username, password });
  },

  // 5.1 集成接口模块
  getInterfaceStatus() {
    return apiClient.get('/interfaces/status');
  },
  getInterfaceLogs() {
    return apiClient.get('/interfaces/logs');
  },
  getInterfaceConfig() {
    return apiClient.get('/interfaces/config');
  },
  saveInterfaceConfig(config) {
    return apiClient.post('/interfaces/config', config);
  },

  // 5.3 可视化模块
  getDashboardCoreMetrics() {
    return apiClient.get('/dashboard/core_metrics');
  },
  getDashboardFusionScore() {
    return apiClient.get('/dashboard/fusion_score');
  },
  getDrillingDesign() {
    return apiClient.get('/visualize/drilling_design');
  },
  getBoreholeFractureData(boreholeId) {
    return apiClient.get(`/visualization/fracture-data/${boreholeId}`);
  },
  getMicroseismicPoints() {
    return apiClient.get('/visualization/microseismic-points');
  },
  getPressureTrendData(range) {
    return apiClient.get('/trends/pressure', { params: { range } });
  },
  getMicroseismicFrequency(range) {
    return apiClient.get('/trends/microseismic_frequency', { params: { range } });
  },
  getDeformationTrend(range) {
    return apiClient.get('/trends/deformation', { params: { range } });
  },

  // 5.4 压裂效果评价模块
  getEvaluationReport(boreholeId) {
    return apiClient.get(`/evaluation/report/${boreholeId}`);
  },

  // 5.5 辅助功能模块
  getAlarmHistory() {
    return apiClient.get('/alarms/history');
  },
  getAlarmConfig() {
    return apiClient.get('/alarms/config');
  },
  saveAlarmConfig(config) {
    return apiClient.post('/alarms/config', config);
  },
  queryData(params) {
    return apiClient.post('/query', params);
  },

  // Data Management
  getManageableTables() {
    return apiClient.get('/management/tables');
  },
  getDataList(tableName, params) {
    return apiClient.get(`/management/${tableName}`, { params });
  },
  createData(tableName, data) {
    return apiClient.post(`/management/${tableName}`, data);
  },
  updateData(tableName, id, data) {
    return apiClient.put(`/management/${tableName}/${id}`, data);
  },
  deleteData(tableName, id) {
    return apiClient.delete(`/management/${tableName}/${id}`);
  },
  bulkDeleteData(tableName, ids) {
    return apiClient.post(`/management/bulk-delete/${tableName}`, { ids });
  },
  importData(tableName, file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post(`/management/import/${tableName}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};

export default api;

