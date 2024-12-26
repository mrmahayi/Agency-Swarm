import React, { useState, useEffect } from 'react';
import { WebSocketService } from '../services/websocket';

interface CommandInputProps {
  onSubmit: (command: string) => void;
  wsUrl?: string;
}

export const CommandInput: React.FC<CommandInputProps> = ({
  onSubmit,
  wsUrl = 'ws://localhost:8000/ws'
}) => {
  const [command, setCommand] = useState('');
  const [ws] = useState(() => new WebSocketService(wsUrl));

  useEffect(() => {
    return () => {
      ws.disconnect();
    };
  }, [ws]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim()) {
      onSubmit(command);
      ws.sendMessage(command);
      setCommand('');
    }
  };

  return (
    <form
      role="form"
      onSubmit={handleSubmit}
      className="flex items-center space-x-2 p-4 bg-white dark:bg-gray-800 border-t dark:border-gray-700"
    >
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter command..."
        className="flex-1 p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Send
      </button>
    </form>
  );
};

export default CommandInput;