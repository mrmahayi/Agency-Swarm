import axios from 'axios';
import { Result } from '../components/ResultsDisplay';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Agent {
  name: string;
  status: 'idle' | 'active' | 'error';
  lastAction: string;
}

export interface CommandResponse {
  results: Result[];
  error?: string;
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const agencyApi = {
  // Get all agents and their status
  getAgents: async (): Promise<Agent[]> => {
    const response = await api.get('/api/agents');
    return response.data;
  },

  // Submit a command to the agency
  submitCommand: async (command: string): Promise<CommandResponse> => {
    const response = await api.post('/api/command', { command });
    return response.data;
  },

  // Get task results
  getResults: async (taskId: string): Promise<Result[]> => {
    const response = await api.get(`/api/results/${taskId}`);
    return response.data;
  },

  // Upload files (for image analysis, etc.)
  uploadFile: async (file: File): Promise<string> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.url;
  },
}; 