import React from 'react';

export interface Result {
  type: 'text' | 'image';
  content: string;
  alt?: string;
}

interface ResultsDisplayProps {
  results: Result[];
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  if (results.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <p className="text-gray-500">No results to display</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4">
      {results.map((result, index) => {
        if (result.type === 'text') {
          return (
            <div key={index} className="rounded-lg bg-white p-4 shadow-sm">
              <p className="text-gray-800">{result.content}</p>
            </div>
          );
        }

        if (result.type === 'image') {
          return (
            <div key={index} className="rounded-lg bg-white p-4 shadow-sm">
              <img
                src={result.content}
                alt={result.alt || 'Result image'}
                className="max-h-96 w-full rounded-lg object-contain"
              />
            </div>
          );
        }

        return null;
      })}
    </div>
  );
};

export default ResultsDisplay;