import React from 'react';
import { Wrench } from 'lucide-react';

interface AgentToolsProps {
  tools: string[];
}

export function AgentTools({ tools }: AgentToolsProps) {
  return (
    <div className="mt-3 border-t border-gray-200 dark:border-gray-700 pt-2">
      <div className="flex items-center text-sm text-gray-600 dark:text-gray-300 mb-1">
        <Wrench className="h-4 w-4 mr-1" />
        <span>Tools:</span>
      </div>
      <div className="flex flex-wrap gap-1">
        {tools.map((tool) => (
          <span
            key={tool}
            className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs rounded-full text-gray-600 dark:text-gray-300"
          >
            {tool}
          </span>
        ))}
      </div>
    </div>
  );
}