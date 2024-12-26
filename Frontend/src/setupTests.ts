import '@testing-library/jest-dom';
import { vi } from 'vitest';
import { WebSocketMessage } from './services/websocket';

// Mock WebSocket
vi.mock('./hooks/useWebSocket', () => ({
  useWebSocket: ({ onMessage, onError }: {
    onMessage?: (data: WebSocketMessage) => void;
    onError?: (error: Event) => void;
  }) => {
    return {
      sendMessage: vi.fn(),
      onMessage,
      onError
    };
  }
}));

// Mock environment variables
vi.stubEnv('VITE_WS_URL', 'ws://test-server/ws'); 