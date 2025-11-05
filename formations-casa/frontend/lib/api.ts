import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await api.post('/token/', { username, password });
    return response.data;
  },
  register: async (data: any) => {
    const response = await api.post('/accounts/users/register/', data);
    return response.data;
  },
  getProfile: async () => {
    const response = await api.get('/accounts/users/me/');
    return response.data;
  },
};

// Formations API
export const formationsAPI = {
  list: async (params?: any) => {
    const response = await api.get('/formations/formations/', { params });
    return response.data;
  },
  get: async (slug: string) => {
    const response = await api.get(`/formations/formations/${slug}/`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/formations/formations/', data);
    return response.data;
  },
  update: async (slug: string, data: any) => {
    const response = await api.patch(`/formations/formations/${slug}/`, data);
    return response.data;
  },
};

// Centers API
export const centersAPI = {
  list: async (params?: any) => {
    const response = await api.get('/centers/centers/', { params });
    return response.data;
  },
  get: async (slug: string) => {
    const response = await api.get(`/centers/centers/${slug}/`);
    return response.data;
  },
};

export default api;
