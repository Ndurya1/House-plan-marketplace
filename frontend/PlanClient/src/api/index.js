const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
export const MEDIA_BASE_URL = BASE_URL.replace(/\/api\/?$/, '');

export const apiClient = async (endpoint, options = {}) => {
  try {
    const token = localStorage.getItem('accessToken');
    const headers = { ...options.headers };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData)) {
      if (!headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
      }
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const text = await response.text();
    return text ? JSON.parse(text) : {};
  } catch (error) {
    console.error("API Request failed:", error);
    throw error;
  }
};

export const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http')) return path;
  return `${MEDIA_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
};

export * from './Catalogue';
export * from './users';
export * from './orders';

