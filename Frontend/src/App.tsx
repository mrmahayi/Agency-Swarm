import React from 'react';
import { useAgency } from './hooks/useAgency';
import AgentCard from './components/AgentCard';
import CommandInput from './components/CommandInput';
import ResultsDisplay from './components/ResultsDisplay';
import { Toaster, toast } from 'react-hot-toast';

export default function App() {
  const { agents, results, isLoading, error, submitCommand, clearError } = useAgency();

  React.useEffect(() => {
    if (error) {
      toast.error(error);
      clearError();
    }
  }, [error, clearError]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Agency Swarm</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-6">
        {/* Agents Grid */}
        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <AgentCard key={agent.name} {...agent} />
          ))}
        </div>

        {/* Command Input */}
        <div className="mb-8">
          <CommandInput onSubmit={submitCommand} />
          {isLoading && (
            <p className="mt-2 text-sm text-gray-600">Processing command...</p>
          )}
        </div>

        {/* Results Display */}
        <div className="rounded-lg border bg-white shadow">
          <ResultsDisplay results={results} />
        </div>
      </main>
    </div>
  );
}