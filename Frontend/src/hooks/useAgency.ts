import { useState, useEffect } from 'react';
import type { Agent } from '../services/api';
import { agencyApi } from '../services/api';
import { WebSocketService } from '../services/websocket';
import type { Result } from '../components/ResultsDisplay';

interface AgencyState {
  agents: Agent[];
  results: Result[];
  isLoading: boolean;
  error: string | null;
}

interface CommandResult {
  results: Result[];
}

export function useAgency() {
  const [state, setState] = useState<AgencyState>({
    agents: [],
    results: [],
    isLoading: false,
    error: null,
  });

  const [ws] = useState(() => new WebSocketService());

  useEffect(() => {
    // Set up WebSocket event handlers
    ws.on('agent_status', (data) => {
      if ('data' in data && typeof data.data === 'object' && data.data !== null) {
        const agentData = data.data as unknown as Agent;
        if ('name' in agentData && 'status' in agentData) {
          setState(prev => ({
            ...prev,
            agents: prev.agents.map(a => a.name === agentData.name ? agentData : a),
          }));
        }
      }
    });

    ws.on('command_result', (data) => {
      if ('data' in data && typeof data.data === 'object' && data.data !== null) {
        const resultData = data.data as unknown as Result;
        if ('type' in resultData && 'content' in resultData) {
          setState(prev => ({
            ...prev,
            results: [...prev.results, resultData],
          }));
        }
      }
    });

    ws.on('error_event', (data) => {
      if ('data' in data && typeof data.data === 'object' && data.data !== null) {
        const errorData = data.data as { message?: string };
        setState(prev => ({
          ...prev,
          error: errorData.message ?? 'Unknown error occurred',
        }));
      }
    });

    // Fetch initial agents
    void fetchAgents();

    // Cleanup
    return () => {
      ws.disconnect();
    };
  }, [ws]);

  const fetchAgents = async (): Promise<void> => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const agents = await agencyApi.getAgents();
      setState(prev => ({ ...prev, agents, isLoading: false }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to fetch agents',
        isLoading: false,
      }));
    }
  };

  const submitCommand = async (command: string): Promise<void> => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const response = await agencyApi.submitCommand(command) as CommandResult;
      setState(prev => ({
        ...prev,
        results: [...prev.results, ...response.results],
        isLoading: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to execute command',
        isLoading: false,
      }));
    }
  };

  const clearResults = (): void => {
    setState(prev => ({ ...prev, results: [] }));
  };

  const clearError = (): void => {
    setState(prev => ({ ...prev, error: null }));
  };

  return {
    ...state,
    submitCommand,
    clearResults,
    clearError,
  };
} 