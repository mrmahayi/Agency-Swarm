import React from 'react';
import { Settings, HelpCircle } from 'lucide-react';
import { Logo } from './Logo';
import { ThemeToggle } from './ThemeToggle';
import { useTheme } from '../utils/theme';

export function Header() {
  const { theme, setTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Logo />
          <div className="flex items-center space-x-4">
            <div className="flex items-center px-3 py-1 rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
              <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
              All Systems Operational
            </div>
            <ThemeToggle theme={theme} onChange={setTheme} />
            <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              <Settings className="h-6 w-6" />
            </button>
            <button className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
              <HelpCircle className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}