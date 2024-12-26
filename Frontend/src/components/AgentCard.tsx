import React from 'react';
import { clsx } from 'clsx';

interface AgentCardProps {
  name: string;
  status: 'idle' | 'active' | 'error';
  lastAction: string;
}

export const AgentCard: React.FC<AgentCardProps> = ({ name, status, lastAction }) => {
  const statusColor = {
    idle: 'text-gray-500',
    active: 'text-green-500',
    error: 'text-red-500'
  }[status];

  return (
    <div className="rounded-lg border p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">{name}</h3>
        <span className={clsx('text-sm font-medium', statusColor)}>{status}</span>
      </div>
      <p className="mt-2 text-sm text-gray-600">{lastAction}</p>
    </div>
  );
};

export default AgentCard;