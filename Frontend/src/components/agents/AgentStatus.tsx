import React from 'react';
import { clsx } from 'clsx';
import { AgentStatus as StatusType } from '../../types/agent';

interface AgentStatusProps {
  status: StatusType;
}

export function AgentStatus({ status }: AgentStatusProps) {
  const statusColors = {
    active: 'bg-green-500',
    idle: 'bg-gray-400',
    busy: 'bg-blue-500',
    error: 'bg-red-500'
  };

  const statusText = {
    active: 'Active',
    idle: 'Idle',
    busy: 'Busy',
    error: 'Error'
  };

  return (
    <div className="flex items-center">
      <div className={clsx('h-3 w-3 rounded-full mr-2', statusColors[status])} />
      <span className="text-sm text-gray-600">{statusText[status]}</span>
    </div>
  );
}