import { io, Socket } from 'socket.io-client';

export interface WebSocketMessage {
  type: string;
  data: {
    name?: string;
    status?: string;
    lastAction?: string;
    message?: string;
    taskId?: string;
    [key: string]: string | undefined;
  };
}

interface ServerToClientEvents {
  message: (data: WebSocketMessage) => void;
  error: (error: Error) => void;
  agent_status: (data: WebSocketMessage) => void;
  task_progress: (data: WebSocketMessage) => void;
  command_result: (data: WebSocketMessage) => void;
  error_event: (data: WebSocketMessage) => void;
}

interface ClientToServerEvents {
  message: (data: string) => void;
  command: (data: string) => void;
}

export class WebSocketService {
  private socket: Socket<ServerToClientEvents, ClientToServerEvents>;
  private messageHandler?: (data: WebSocketMessage) => void;
  private errorHandler?: (error: Event) => void;

  constructor(url: string = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws') {
    this.socket = io(url, {
      transports: ['websocket'],
      autoConnect: true
    });

    this.socket.on('message', (data: WebSocketMessage) => {
      this.messageHandler?.(data);
    });

    this.socket.on('error', (error: Error) => {
      if (this.errorHandler) {
        this.errorHandler(new ErrorEvent('error', { error }));
      }
    });
  }

  public on(event: keyof ServerToClientEvents, handler: (data: WebSocketMessage | Error) => void): void {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    this.socket.on(event, handler as any);
  }

  public off(event: keyof ServerToClientEvents, handler: (data: WebSocketMessage | Error) => void): void {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    this.socket.off(event, handler as any);
  }

  public onMessage(handler: (data: WebSocketMessage) => void): void {
    this.messageHandler = handler;
  }

  public onError(handler: (error: Event) => void): void {
    this.errorHandler = handler;
  }

  public sendMessage(message: string): void {
    this.socket.emit('message', message);
  }

  public disconnect(): void {
    this.socket.disconnect();
  }
}

export const agencyWs = new WebSocketService(); 