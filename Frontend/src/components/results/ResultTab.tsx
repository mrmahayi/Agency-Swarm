import React from 'react';
import { Result } from '../ResultsDisplay';

interface ResultTabProps {
  result: Result;
  isActive: boolean;
  onClick: () => void;
}

export const ResultTab: React.FC<ResultTabProps> = ({
  result,
  isActive,
  onClick
}) => {
  return (
    <button
      className={`px-4 py-2 text-sm font-medium ${
        isActive
          ? 'border-b-2 border-blue-500 text-blue-600'
          : 'text-gray-500 hover:text-gray-700'
      }`}
      onClick={onClick}
    >
      {result.type === 'text' ? 'Text' : 'Image'}
    </button>
  );
};