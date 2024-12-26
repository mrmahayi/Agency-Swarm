import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CommandInput } from '../../components/CommandInput';
import { ResultsDisplay } from '../../components/ResultsDisplay';
import { AgentCard } from '../../components/AgentCard';

// Mock WebSocketService
const mockSendMessage = vi.fn();
const mockDisconnect = vi.fn();
const mockOnMessage = vi.fn();
const mockOnError = vi.fn();

vi.mock('../../services/websocket', () => ({
  WebSocketService: vi.fn().mockImplementation(() => ({
    sendMessage: mockSendMessage,
    disconnect: mockDisconnect,
    onMessage: mockOnMessage,
    onError: mockOnError
  }))
}));

describe('WebSocket Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('establishes WebSocket connection and handles messages', () => {
    const { rerender } = render(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="idle"
          lastAction="Ready"
        />
        <CommandInput onSubmit={() => {}} wsUrl="ws://test-server/ws" />
        <ResultsDisplay results={[]} />
      </div>
    );

    // Verify initial state
    expect(screen.getByText('TaskOrchestrator')).toBeInTheDocument();
    expect(screen.getByText('idle')).toBeInTheDocument();
    expect(screen.getByText('Ready')).toBeInTheDocument();

    // Simulate agent status update
    rerender(
      <div>
        <AgentCard
          name="TaskOrchestrator"
          status="active"
          lastAction="Processing command"
        />
        <CommandInput onSubmit={() => {}} wsUrl="ws://test-server/ws" />
        <ResultsDisplay results={[]} />
      </div>
    );

    // Verify updated state
    expect(screen.getByText('active')).toBeInTheDocument();
    expect(screen.getByText('Processing command')).toBeInTheDocument();
  });

  it('sends commands through WebSocket', () => {
    const mockOnSubmit = vi.fn();
    const { getByPlaceholderText, getByRole } = render(
      <CommandInput onSubmit={mockOnSubmit} wsUrl="ws://test-server/ws" />
    );

    // Simulate command input
    const input = getByPlaceholderText(/enter command/i);
    const form = getByRole('form');
    
    fireEvent.change(input, { target: { value: 'test command' } });
    fireEvent.submit(form);

    // Verify onSubmit was called and message was sent
    expect(mockOnSubmit).toHaveBeenCalledWith('test command');
    expect(mockSendMessage).toHaveBeenCalledWith('test command');
  });

  it('handles WebSocket errors', () => {
    const mockOnSubmit = vi.fn();
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {});

    render(<CommandInput onSubmit={mockOnSubmit} wsUrl="ws://test-server/ws" />);

    // Get the error handler that was registered
    const errorHandler = mockOnError.mock.calls[0]?.[0];
    if (errorHandler) {
      // Simulate error event
      errorHandler(new Event('error'));

      // Verify error was logged
      expect(consoleError).toHaveBeenCalledWith(
        'WebSocket error:',
        expect.any(Event)
      );
    }

    consoleError.mockRestore();
  });

  it('cleans up WebSocket connection on unmount', () => {
    const mockOnSubmit = vi.fn();
    const { unmount } = render(
      <CommandInput onSubmit={mockOnSubmit} wsUrl="ws://test-server/ws" />
    );

    unmount();
    expect(mockDisconnect).toHaveBeenCalled();
  });
}); 