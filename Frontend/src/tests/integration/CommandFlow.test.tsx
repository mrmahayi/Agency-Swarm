import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CommandInput } from '../../components/CommandInput';
import { ResultsDisplay } from '../../components/ResultsDisplay';
import { AgentCard } from '../../components/AgentCard';
import type { Result } from '../../components/ResultsDisplay';

// Mock WebSocketService
const mockSendMessage = vi.fn();
const mockDisconnect = vi.fn();

vi.mock('../../services/websocket', () => ({
  WebSocketService: vi.fn().mockImplementation(() => ({
    sendMessage: mockSendMessage,
    disconnect: mockDisconnect
  }))
}));

describe('Command Flow Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('handles complete command flow with agent updates and results', () => {
    // Initial agent state
    const agent = {
      name: 'TaskOrchestrator',
      status: 'idle' as const,
      lastAction: 'Waiting for command'
    };

    // Mock onSubmit handler
    const mockOnSubmit = vi.fn();

    // Render components
    const { rerender } = render(
      <div>
        <AgentCard {...agent} />
        <CommandInput onSubmit={mockOnSubmit} />
        <ResultsDisplay results={[]} />
      </div>
    );

    // Verify initial state
    expect(screen.getByText('TaskOrchestrator')).toBeInTheDocument();
    expect(screen.getByText('idle')).toBeInTheDocument();
    expect(screen.getByText('Waiting for command')).toBeInTheDocument();
    expect(screen.getByText(/no results/i)).toBeInTheDocument();

    // Simulate command input
    const input = screen.getByPlaceholderText(/enter command/i);
    const form = screen.getByRole('form');
    fireEvent.change(input, { target: { value: 'analyze image' } });
    fireEvent.submit(form);

    // Verify onSubmit was called and message was sent
    expect(mockOnSubmit).toHaveBeenCalledWith('analyze image');
    expect(mockSendMessage).toHaveBeenCalledWith('analyze image');

    // Simulate agent status update
    rerender(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="active"
          lastAction="Processing: analyze image"
        />
        <CommandInput onSubmit={mockOnSubmit} />
        <ResultsDisplay results={[]} />
      </div>
    );

    // Verify agent status update
    expect(screen.getByText('active')).toBeInTheDocument();
    expect(screen.getByText('Processing: analyze image')).toBeInTheDocument();

    // Simulate results received
    const results: Result[] = [
      { type: 'text', content: 'Analysis started' },
      { type: 'image', content: 'result.jpg', alt: 'Analysis result' }
    ];

    rerender(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="idle"
          lastAction="Analysis complete"
        />
        <CommandInput onSubmit={mockOnSubmit} />
        <ResultsDisplay results={results} />
      </div>
    );

    // Verify final state
    expect(screen.getByText('idle')).toBeInTheDocument();
    expect(screen.getByText('Analysis complete')).toBeInTheDocument();
    expect(screen.getByText('Analysis started')).toBeInTheDocument();
    expect(screen.getByAltText('Analysis result')).toBeInTheDocument();
  });

  it('handles error states in the command flow', () => {
    // Mock onSubmit handler
    const mockOnSubmit = vi.fn();

    // Initial render
    const { rerender } = render(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="idle"
          lastAction="Ready"
        />
        <CommandInput onSubmit={mockOnSubmit} />
        <ResultsDisplay results={[]} />
      </div>
    );

    // Simulate command input
    const input = screen.getByPlaceholderText(/enter command/i);
    const form = screen.getByRole('form');
    fireEvent.change(input, { target: { value: 'invalid command' } });
    fireEvent.submit(form);

    // Verify onSubmit was called and message was sent
    expect(mockOnSubmit).toHaveBeenCalledWith('invalid command');
    expect(mockSendMessage).toHaveBeenCalledWith('invalid command');

    // Simulate error state
    rerender(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="error"
          lastAction="Error: Invalid command format"
        />
        <CommandInput onSubmit={mockOnSubmit} />
        <ResultsDisplay
          results={[
            {
              type: 'text',
              content: 'Error: Command could not be processed'
            }
          ]}
        />
      </div>
    );

    // Verify error state
    expect(screen.getByText('error')).toBeInTheDocument();
    expect(screen.getByText('Error: Invalid command format')).toBeInTheDocument();
    expect(
      screen.getByText('Error: Command could not be processed')
    ).toBeInTheDocument();
  });
}); 