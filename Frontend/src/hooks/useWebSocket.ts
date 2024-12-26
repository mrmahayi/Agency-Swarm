import { useEffect, useCallback, useState } from 'react';
import { WebSocketService, WebSocketMessage } from '../services/websocket';

interface WebSocketHookOptions {
  url: string;
  onMessage?: (data: WebSocketMessage) => void;
  onError?: (error: Event) => void;
}

export function useWebSocket({ url, onMessage, onError }: WebSocketHookOptions) {
  const [ws] = useState(() => new WebSocketService(url));

  useEffect(() => {
    if (onMessage) {
      ws.onMessage(onMessage);
    }
    if (onError) {
      ws.onError(onError);
    }

    return () => {
      ws.disconnect();
    };
  }, [ws, onMessage, onError]);

  const sendMessage = useCallback((message: string) => {
    ws.sendMessage(message);
  }, [ws]);

  return { sendMessage };
} 