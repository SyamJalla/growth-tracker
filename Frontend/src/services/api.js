import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Base API URL for local testing
const API_BASE_URL = 'http://localhost:8000';

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
        console.log('🚀 API Request:', config.method.toUpperCase(), config.url);
        return config;
    },
    (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => {
        console.log('✅ API Response:', response.config.url, '- Status:', response.status);
        return response;
    },
    (error) => {
        if (error.response) {
            console.error('❌ API Error Response:', error.response.status, error.response.data);
        } else if (error.request) {
            console.error('❌ Network Error - No Response:', error.message);
            console.error('Check if backend is running at:', API_BASE_URL);
        } else {
            console.error('❌ API Error:', error.message);
        }
        return Promise.reject(error);
    }
);

// Health API
export const healthApi = {
    checkHealth: () => api.get('/api/health/'),
    checkDbHealth: () => api.get('/api/health/db'),
};

// Dashboard API - Single endpoint returns all stats
export const dashboardApi = {
    getDashboard: () => api.get('/api/dashboard/'),
    getKPIs: () => api.get('/api/dashboard/'),
    getWeeklyProgress: () => api.get('/api/dashboard/'),
    getTrends: () => api.get('/api/dashboard/'),
};

// Workout Tracker API
export const workoutApi = {
    // Get all workouts (with optional date range)
    getAllWorkouts: (startDate, endDate) => {
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;
        return api.get('/api/workouts/history/', { params });
    },

    // Get workout by specific date
    getWorkoutById: (date) => api.get(`/api/workouts/${date}`),

    // Create new workout (fails if date exists)
    logWorkout: (data) => api.post('/api/workouts/', data),

    // Update existing workout
    updateWorkout: (date, data) => api.put(`/api/workouts/${date}`, data),

    // Create or update workout (no duplicate error)
    upsertWorkout: (data) => api.post('/api/workouts/upsert/', data),

    // Delete workout
    deleteWorkout: (date) => api.delete(`/api/workouts/${date}`),

    // Get weekly stats (returns dashboard data)
    getWeeklyStats: () => api.get('/api/dashboard/'),

    // Get monthly stats (returns dashboard data)
    getMonthlyStats: () => api.get('/api/dashboard/'),

    // Alias methods for backward compatibility
    getHistory: (startDate, endDate) => {
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;
        return api.get('/api/workouts/history/', { params });
    },
    create: (data) => api.post('/api/workouts/', data),
    update: (date, data) => api.put(`/api/workouts/${date}`, data),
    upsert: (data) => api.post('/api/workouts/upsert/', data),
    getByDate: (date) => api.get(`/api/workouts/${date}`),
    delete: (date) => api.delete(`/api/workouts/${date}`),
};

// Smoking Tracker API
export const smokingApi = {
    // Get all entries (with optional date range)
    getAllEntries: (startDate, endDate) => {
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;
        return api.get('/api/smoking/history/', { params });
    },

    // Get entry by specific date
    getEntryById: (date) => api.get(`/api/smoking/${date}`),

    // Create new entry (fails if date exists)
    logEntry: (data) => api.post('/api/smoking/', data),

    // Update existing entry
    updateEntry: (date, data) => api.put(`/api/smoking/${date}`, data),

    // Create or update entry (no duplicate error)
    upsertEntry: (data) => api.post('/api/smoking/upsert/', data),

    // Delete entry
    deleteEntry: (date) => api.delete(`/api/smoking/${date}`),

    // Get weekly stats (returns dashboard data)
    getWeeklyStats: () => api.get('/api/dashboard/'),

    // Get monthly stats (returns dashboard data)
    getMonthlyStats: () => api.get('/api/dashboard/'),

    // Get streak information (returns dashboard data)
    getStreakInfo: () => api.get('/api/dashboard/'),

    // Alias methods for backward compatibility
    getHistory: (startDate, endDate) => {
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;
        return api.get('/api/smoking/history/', { params });
    },
    create: (data) => api.post('/api/smoking/', data),
    update: (date, data) => api.put(`/api/smoking/${date}`, data),
    upsert: (data) => api.post('/api/smoking/upsert/', data),
    getByDate: (date) => api.get(`/api/smoking/${date}`),
    delete: (date) => api.delete(`/api/smoking/${date}`),
};

// Database Tasks API
export const dbApi = {
    createDatabase: (dbName) => api.post('/db/create_database', { db_name: dbName }),
    createTables: () => api.post('/db/create_tables'),
    initHealthCheck: () => api.post('/db/init_health_check'),
};

export default api;
