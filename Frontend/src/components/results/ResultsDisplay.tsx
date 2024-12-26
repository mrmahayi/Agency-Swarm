import React, { useState } from 'react';
import { FileText, Image, Globe, BookOpen } from 'lucide-react';
import { ResultTab } from './ResultTab';
import { ResultContent } from './ResultContent';

const tabs = [
  { id: 'text', label: 'Text', icon: FileText },
  { id: 'visual', label: 'Visual', icon: Image },
  { id: 'web', label: 'Web', icon: Globe },
  { id: 'research', label: 'Research', icon: BookOpen },
];

export function ResultsDisplay() {
  const [activeTab, setActiveTab] = useState('text');

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm h-full">
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex space-x-4 px-4" aria-label="Tabs">
          {tabs.map((tab) => (
            <ResultTab
              key={tab.id}
              {...tab}
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            />
          ))}
        </nav>
      </div>
      <ResultContent activeTab={activeTab} />
    </div>
  );
}