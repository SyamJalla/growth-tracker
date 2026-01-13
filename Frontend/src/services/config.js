// API Configuration
// Update this URL based on your environment
export const API_CONFIG = {
    // Local development
    LOCAL: 'http://localhost:8000/api',

    // Production
    PRODUCTION: 'https://your-production-url.com/api',

    // Docker
    DOCKER: 'http://host.docker.internal:8000/api',
};

// Set the current environment
export const CURRENT_ENV = 'LOCAL';

// Export the base URL based on environment
export const BASE_URL = API_CONFIG[CURRENT_ENV];
