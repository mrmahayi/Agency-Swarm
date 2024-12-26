import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import AgentCard from './AgentCard';

describe('AgentCard', () => {
  it('renders agent information correctly', () => {
    const agent = {
      name: 'Test Agent',
      status: 'idle' as const,
      lastAction: 'No recent actions'
    };

    render(<AgentCard {...agent} />);

    expect(screen.getByText('Test Agent')).toBeInTheDocument();
    expect(screen.getByText('idle')).toBeInTheDocument();
    expect(screen.getByText('No recent actions')).toBeInTheDocument();
  });

  it('shows correct status indicator', () => {
    const agent = {
      name: 'Test Agent',
      status: 'active' as const,
      lastAction: 'Processing task'
    };

    render(<AgentCard {...agent} />);

    const statusElement = screen.getByText('active');
    expect(statusElement).toHaveClass('text-green-500');
  });
}); 