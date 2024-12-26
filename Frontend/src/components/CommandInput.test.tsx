import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CommandInput } from './CommandInput';

// Mock WebSocketService
const mockSendMessage = vi.fn();
const mockDisconnect = vi.fn();

vi.mock('../services/websocket', () => ({
  WebSocketService: vi.fn().mockImplementation(() => ({
    sendMessage: mockSendMessage,
    disconnect: mockDisconnect
  }))
}));

describe('CommandInput', () => {
  it('renders input field correctly', () => {
    render(<CommandInput onSubmit={() => {}} />);
    
    const input = screen.getByPlaceholderText(/enter command/i);
    expect(input).toBeInTheDocument();
  });

  it('handles input changes', () => {
    render(<CommandInput onSubmit={() => {}} />);
    
    const input = screen.getByPlaceholderText(/enter command/i);
    fireEvent.change(input, { target: { value: 'test command' } });
    
    expect(input).toHaveValue('test command');
  });

  it('calls onSubmit and sends message when form is submitted', () => {
    const handleSubmit = vi.fn();
    render(<CommandInput onSubmit={handleSubmit} />);
    
    const input = screen.getByPlaceholderText(/enter command/i);
    const form = screen.getByRole('form');
    
    fireEvent.change(input, { target: { value: 'test command' } });
    fireEvent.submit(form);
    
    expect(handleSubmit).toHaveBeenCalledWith('test command');
    expect(mockSendMessage).toHaveBeenCalledWith('test command');
  });

  it('disconnects WebSocket on unmount', () => {
    const { unmount } = render(<CommandInput onSubmit={() => {}} />);
    unmount();
    expect(mockDisconnect).toHaveBeenCalled();
  });
}); 