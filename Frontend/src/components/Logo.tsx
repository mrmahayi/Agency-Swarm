import React from 'react';
import { Network } from 'lucide-react';

export function Logo() {
  return (
    <div className="flex items-center">
      <Network className="h-8 w-8 text-blue-600 dark:text-blue-400" />
      <span className="ml-2 text-xl font-bold text-gray-900 dark:text-white">
        Agency-Swarm
      </span>
    </div>
  );
}