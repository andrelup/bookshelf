import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Toast } from './Toast';

describe('Toast', () => {
  it('renders a success toast with role="status"', () => {
    render(<Toast type="success" message="Saved successfully" />);

    const toast = screen.getByRole('status');
    expect(toast).toHaveTextContent('Saved successfully');
  });

  it('renders an error toast with role="alert"', () => {
    render(<Toast type="error" message="Something went wrong" />);

    const toast = screen.getByRole('alert');
    expect(toast).toHaveTextContent('Something went wrong');
  });

  it('calls onDismiss when the dismiss button is clicked', async () => {
    const user = userEvent.setup();
    const onDismiss = vi.fn();

    render(<Toast type="success" message="Saved successfully" onDismiss={onDismiss} />);

    await user.click(screen.getByRole('button', { name: 'Dismiss notification' }));

    expect(onDismiss).toHaveBeenCalledTimes(1);
  });
});
