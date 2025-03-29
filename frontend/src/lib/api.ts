import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface Aircraft {
  id: number;
  type: string;
  model: string;
  registration: string;
  status: 'available' | 'maintenance' | 'in_use';
  total_hours: number;
  last_maintenance: string;
}

export interface Student {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
  created_at: string;
}

export interface Booking {
  id: number;
  student_id: number;
  aircraft_id: number;
  instructor_id: number;
  start_time: string;
  duration: number;
  status: 'scheduled' | 'completed' | 'cancelled';
  notes?: string;
}

export const aircraftApi = {
  getAll: () => api.get<Aircraft[]>('/aircraft'),
  getById: (id: number) => api.get<Aircraft>(`/aircraft/${id}`),
  create: (data: Omit<Aircraft, 'id'>) => api.post<Aircraft>('/aircraft', data),
  update: (id: number, data: Partial<Aircraft>) => api.put<Aircraft>(`/aircraft/${id}`, data),
  delete: (id: number) => api.delete(`/aircraft/${id}`),
};

export const studentApi = {
  getAll: () => api.get<Student[]>('/students'),
  getById: (id: number) => api.get<Student>(`/students/${id}`),
  create: (data: Omit<Student, 'id'>) => api.post<Student>('/students', data),
  update: (id: number, data: Partial<Student>) => api.put<Student>(`/students/${id}`, data),
  delete: (id: number) => api.delete(`/students/${id}`),
};

export const bookingApi = {
  getAll: () => api.get<Booking[]>('/bookings'),
  getById: (id: number) => api.get<Booking>(`/bookings/${id}`),
  create: (data: Omit<Booking, 'id'>) => api.post<Booking>('/bookings', data),
  update: (id: number, data: Partial<Booking>) => api.put<Booking>(`/bookings/${id}`, data),
  delete: (id: number) => api.delete(`/bookings/${id}`),
};

export const authApi = {
  login: (email: string, password: string) => api.post('/auth/login', { email, password }),
  register: (data: { email: string; password: string; first_name: string; last_name: string }) =>
    api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
}; 