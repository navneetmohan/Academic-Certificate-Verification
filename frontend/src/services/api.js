import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't auto-redirect on verification page errors
      if (!window.location.pathname.startsWith('/verify')) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(email, password) {
    const res = await api.post('/auth/login', { email, password });
    localStorage.setItem('auth_token', res.data.access_token);
    localStorage.setItem('auth_user', JSON.stringify(res.data.institution));
    return res.data;
  },
  async getMe() {
    const res = await api.get('/auth/me');
    return res.data;
  },
  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  },
  getCurrentUser() {
    const user = localStorage.getItem('auth_user');
    return user ? JSON.parse(user) : null;
  },
  isAuthenticated() {
    return !!localStorage.getItem('auth_token');
  }
};

export const certificateService = {
  async issue(certificateData) {
    const res = await api.post('/certificates', certificateData);
    return res.data;
  },
  async list() {
    const res = await api.get('/certificates');
    return res.data;
  },
  async get(id) {
    const res = await api.get(`/certificates/${id}`);
    return res.data;
  },
  async revoke(id) {
    const res = await api.post(`/certificates/${id}/revoke`);
    return res.data;
  },
  async getOnchainStatus(id) {
    const res = await api.get(`/certificates/${id}/status`);
    return res.data;
  },
  getDownloadUrl(id) {
    return `${API_BASE_URL}/certificates/${id}/download`;
  }
};

export const verifyService = {
  async verifyById(certificateId) {
    const res = await api.get(`/verify/${certificateId}`);
    return res.data;
  },
  async verifyFile(file, certificateId = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (certificateId) {
      formData.append('certificate_id', certificateId);
    }
    const res = await api.post('/verify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },
  async testTamper(certificateId) {
    const res = await api.post(`/verify/tamper-test/${certificateId}`);
    return res.data;
  }
};

export const blockchainService = {
  async getTransaction(txHash) {
    const res = await api.get(`/blockchain/transaction/${txHash}`);
    return res.data;
  }
};

export const statsService = {
  async getDashboardStats() {
    const res = await api.get('/stats');
    return res.data;
  }
};

export default api;
