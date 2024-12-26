import React from 'react';
import { Power, MoreVertical, AlertCircle } from 'lucide-react';
import { Agent } from '../../types/agent';
import { AgentStatus } from './AgentStatus';
import { AgentTools } from './AgentTools';

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-gray-900 dark:text-white mb-1">{agent.name}</h3>
          <AgentStatus status={agent.status} />
        </div>
        <div className="flex space-x-2">
          <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <Power className="h-5 w-5" />
          </button>
          <button className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <MoreVertical className="h-5 w-5" />
          </button>
        </div>
      </div>
      
      <div className="mt-3">
        {agent.currentTask && (
          <p className="text-sm text-gray-600 dark:text-gray-300">
            <span className="font-medium">Current Task:</span> {agent.currentTask}
          </p>
        )}
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Last action: {agent.lastAction}</p>
      </div>

      <AgentTools tools={agent.tools} />

      {agent.status === 'error' && (
        <div className="mt-3 flex items-center text-red-600 dark:text-red-400 text-sm">
          <AlertCircle className="h-4 w-4 mr-1" />
          <span>Error detected</span>
        </div>
      )}
    </div>
  );
}