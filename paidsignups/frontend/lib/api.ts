import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== 'undefined') {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            const response = await axios.post(`${API_URL}/auth/refresh/`, {
              refresh: refreshToken,
            });
            const { access } = response.data;
            localStorage.setItem('access_token', access);
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return api(originalRequest);
          } catch (err) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
          }
        }
      }
    }

    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login/', { email, password }),
  register: (data: any) => api.post('/auth/register/', data),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data: any) => api.patch('/auth/profile/', data),
  changePassword: (data: any) => api.put('/auth/change-password/', data),
};

// Forms APIs
export const formsAPI = {
  list: (params?: any) => api.get('/forms/', { params }),
  get: (id: string) => api.get(`/forms/${id}/`),
  create: (data: any) => api.post('/forms/', data),
  update: (id: string, data: any) => api.patch(`/forms/${id}/`, data),
  delete: (id: string) => api.delete(`/forms/${id}/`),
  duplicate: (id: string) => api.post(`/forms/${id}/duplicate/`),
  togglePublish: (id: string) => api.post(`/forms/${id}/toggle_publish/`),
  getPublic: (id: string) => api.get(`/forms/${id}/public/`),
  stats: () => api.get('/forms/stats/'),
};

// Landing Pages APIs
export const landingPagesAPI = {
  list: (params?: any) => api.get('/landing-pages/', { params }),
  get: (id: string) => api.get(`/landing-pages/${id}/`),
  create: (data: any) => api.post('/landing-pages/', data),
  update: (id: string, data: any) => api.patch(`/landing-pages/${id}/`, data),
  delete: (id: string) => api.delete(`/landing-pages/${id}/`),
  duplicate: (id: string) => api.post(`/landing-pages/${id}/duplicate/`),
  togglePublish: (id: string) => api.post(`/landing-pages/${id}/toggle_publish/`),
  getPublic: (id: string) => api.get(`/landing-pages/${id}/public/`),
};

// Leads APIs
export const leadsAPI = {
  list: (params?: any) => api.get('/leads/', { params }),
  get: (id: string) => api.get(`/leads/${id}/`),
  update: (id: string, data: any) => api.patch(`/leads/${id}/`, data),
  delete: (id: string) => api.delete(`/leads/${id}/`),
  stats: () => api.get('/leads/stats/'),
  submit: (data: any) => axios.post(`${API_URL}/submit/`, data), // Public endpoint
};

// Subscriptions APIs
export const subscriptionsAPI = {
  list: () => api.get('/subscriptions/'),
  get: (id: string) => api.get(`/subscriptions/${id}/`),
  create: (data: any) => api.post('/subscriptions/', data),
  cancel: (id: string, reason?: string) =>
    api.post(`/subscriptions/${id}/cancel/`, { reason }),
  current: () => api.get('/subscriptions/current/'),
  plans: () => api.get('/subscriptions/plans/'),
};

// Users APIs
export const usersAPI = {
  stats: () => api.get('/users/stats/'),
};

export default api;
