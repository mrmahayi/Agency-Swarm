import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ResultsDisplay from './ResultsDisplay';
import type { Result } from './ResultsDisplay';

describe('ResultsDisplay', () => {
  it('renders empty state correctly', () => {
    render(<ResultsDisplay results={[]} />);
    expect(screen.getByText(/no results/i)).toBeInTheDocument();
  });

  it('renders text results correctly', () => {
    const results: Result[] = [
      { type: 'text' as const, content: 'Test result 1' },
      { type: 'text' as const, content: 'Test result 2' }
    ];

    render(<ResultsDisplay results={results} />);
    
    expect(screen.getByText('Test result 1')).toBeInTheDocument();
    expect(screen.getByText('Test result 2')).toBeInTheDocument();
  });

  it('renders image results correctly', () => {
    const results: Result[] = [
      { type: 'image' as const, content: 'test-image.jpg', alt: 'Test image' }
    ];

    render(<ResultsDisplay results={results} />);
    
    const image = screen.getByAltText('Test image');
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute('src', 'test-image.jpg');
  });

  it('handles mixed result types', () => {
    const results: Result[] = [
      { type: 'text' as const, content: 'Text result' },
      { type: 'image' as const, content: 'image.jpg', alt: 'Image result' }
    ];

    render(<ResultsDisplay results={results} />);
    
    expect(screen.getByText('Text result')).toBeInTheDocument();
    expect(screen.getByAltText('Image result')).toBeInTheDocument();
  });
}); 