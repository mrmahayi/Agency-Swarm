import React from 'react';

interface ResultContentProps {
  activeTab: string;
}

export function ResultContent({ activeTab }: ResultContentProps) {
  const content = {
    text: 'No results to display yet. Start by entering a command.',
    visual: 'Visual results will appear here.',
    web: 'Web content will be displayed in this tab.',
    research: 'Research findings will be shown here.'
  };

  return (
    <div className="p-4">
      <div className="text-gray-600 dark:text-gray-300">
        <p>{content[activeTab as keyof typeof content]}</p>
      </div>
    </div>
  );
}