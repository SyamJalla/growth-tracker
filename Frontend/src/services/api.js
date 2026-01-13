import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Base API URL - Update this to your backend server URL
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token if needed
api.interceptors.request.use(
    async (config) => {
        const token = await AsyncStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            console.error('API Error:', error.response.data);
        } else if (error.request) {
            console.error('Network Error:', error.message);
        }
        return Promise.reject(error);
    }
);

// Health API
export const healthApi = {
    checkHealth: () => api.get('/health'),
    checkDbHealth: () => api.get('/health/db'),
};

// Dashboard API
export const dashboardApi = {
    getKPIs: () => api.get('/dashboard/kpis'),
    getWeeklyProgress: () => api.get('/dashboard/weekly-progress'),
    getTrends: () => api.get('/dashboard/trends'),
};

// Workout Tracker API
export const workoutApi = {
    getAllWorkouts: () => api.get('/workouts'),
    getWorkoutById: (id) => api.get(`/workouts/${id}`),
    logWorkout: (data) => api.post('/workouts', data),
    updateWorkout: (id, data) => api.put(`/workouts/${id}`, data),
    deleteWorkout: (id) => api.delete(`/workouts/${id}`),
    getWeeklyStats: () => api.get('/workouts/stats/weekly'),
    getMonthlyStats: () => api.get('/workouts/stats/monthly'),
};

// Smoking Tracker API
export const smokingApi = {
    getAllEntries: () => api.get('/smoking'),
    getEntryById: (id) => api.get(`/smoking/${id}`),
    logEntry: (data) => api.post('/smoking', data),
    updateEntry: (id, data) => api.put(`/smoking/${id}`, data),
    deleteEntry: (id) => api.delete(`/smoking/${id}`),
    getWeeklyStats: () => api.get('/smoking/stats/weekly'),
    getMonthlyStats: () => api.get('/smoking/stats/monthly'),
    getStreakInfo: () => api.get('/smoking/stats/streak'),
};

// Database Tasks API
export const dbApi = {
    clearAllData: () => api.delete('/db/clear'),
    exportData: () => api.get('/db/export'),
    importData: (data) => api.post('/db/import', data),
};

export default api;
