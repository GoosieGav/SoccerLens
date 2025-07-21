import axios from 'axios';
import { Player, ApiResponse, LeaderboardResponse, SimilarPlayersResponse, SortOptionsResponse, PlayerFilters } from '../types';

// Dynamic API URL that works in different environments
const getApiBaseUrl = () => {
  // In development, use the local network IP
  if (__DEV__) {
    return 'http://192.168.68.101:8000/api';
  }
  // In production, use the production URL
  return 'https://your-production-api.com/api';
};

const API_BASE_URL = getApiBaseUrl();

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Increased timeout for mobile networks
  headers: {
    'Content-Type': 'application/json',
  },
  // Add retry logic for network issues
  validateStatus: (status) => {
    return status >= 200 && status < 300; // Accept 2xx status codes
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'NETWORK_ERROR') {
      console.error('Network Error - Check if Django server is running and accessible');
    }
    return Promise.reject(error);
  }
);

// API service class
export class ApiService {
  // Get all players with optional filters and sorting
  static async getPlayers(
    filters?: PlayerFilters,
    sortBy?: string,
    sortOrder: 'asc' | 'desc' = 'desc',
    page: number = 1,
    pageSize: number = 20,
    searchQuery?: string
  ): Promise<ApiResponse<Player>> {
    const params = new URLSearchParams();
    
    // Add search query if provided
    if (searchQuery) {
      params.append('search', searchQuery);
    }
    
    // Add filters
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }
    
    // Add sorting
    if (sortBy) {
      params.append('sort_by', sortBy);
      params.append('sort_order', sortOrder);
    }
    
    // Add pagination
    params.append('page', page.toString());
    params.append('page_size', pageSize.toString());
    
    const response = await api.get(`/players/?${params.toString()}`);
    return response.data;
  }

  // Search players
  static async searchPlayers(
    query: string,
    filters?: PlayerFilters,
    page: number = 1,
    pageSize: number = 20
  ): Promise<ApiResponse<Player>> {
    const params = new URLSearchParams();
    params.append('q', query);
    params.append('page', page.toString());
    params.append('page_size', pageSize.toString());
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString());
        }
      });
    }
    
    const response = await api.get(`/players/search/?${params.toString()}`);
    return response.data;
  }

  // Get player by ID
  static async getPlayer(id: number): Promise<Player> {
    const response = await api.get(`/players/${id}/`);
    return response.data;
  }

  // Get similar players
  static async getSimilarPlayers(
    playerId: number,
    method: 'statistical' | 'nlp' | 'hybrid' = 'hybrid',
    limit: number = 10
  ): Promise<SimilarPlayersResponse> {
    const params = new URLSearchParams();
    params.append('method', method);
    params.append('limit', limit.toString());
    
    const response = await api.get(`/players/${playerId}/similar/?${params.toString()}`);
    return response.data;
  }

  // Get leaderboards
  static async getLeaderboard(
    stat: string,
    limit: number = 20
  ): Promise<LeaderboardResponse> {
    const params = new URLSearchParams();
    params.append('stat', stat);
    params.append('limit', limit.toString());
    
    const response = await api.get(`/players/leaderboard/?${params.toString()}`);
    return response.data;
  }

  // Get sorting options
  static async getSortOptions(category?: string): Promise<SortOptionsResponse> {
    const params = category ? `?category=${category}` : '';
    const response = await api.get(`/players/sort_options/${params}`);
    return response.data;
  }

  // Get sort options by category
  static async getSortOptionsByCategory(): Promise<{ [category: string]: any }> {
    const response = await api.get('/players/sort_options_by_category/');
    return response.data;
  }

  // Get available positions
  static async getPositions(): Promise<string[]> {
    const response = await api.get('/players/positions/');
    return response.data;
  }

  // Get available competitions
  static async getCompetitions(): Promise<string[]> {
    const response = await api.get('/players/competitions/');
    return response.data;
  }

  // Get available teams
  static async getTeams(): Promise<string[]> {
    const response = await api.get('/players/teams/');
    return response.data;
  }

  // Get available nations
  static async getNations(): Promise<string[]> {
    const response = await api.get('/players/nations/');
    return response.data;
  }

  // Get API root info
  static async getApiInfo(): Promise<any> {
    const response = await api.get('/');
    return response.data;
  }
}

// Network connectivity check
export const checkApiConnectivity = async (): Promise<boolean> => {
  try {
    const response = await api.get('/players/?page_size=1', { timeout: 5000 });
    return true;
  } catch (error: any) {
    console.error('API connectivity check failed:', error.message);
    return false;
  }
};

// Error handling utility
export const handleApiError = (error: any): string => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    if (data?.error) {
      return data.error;
    }
    return `Server error (${status})`;
  } else if (error.request) {
    // Network error
    return 'Network error. Please check your connection and ensure the Django server is running.';
  } else {
    // Other error
    return error.message || 'An unexpected error occurred.';
  }
};

export default ApiService; 