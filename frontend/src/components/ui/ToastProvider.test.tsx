import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ToastProvider } from './ToastProvider';
import { useToast } from '@/hooks/useToast';

const TriggerButton = () => {
  const { showToast } = useToast();

  return (
    <button type="button" onClick={() => showToast({ type: 'success', message: 'Saved!' })}>
      Trigger toast
    </button>
  );
};

describe('ToastProvider', () => {
  beforeEach(() => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('renders a toast when showToast is called', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });

    render(
      <ToastProvider>
        <TriggerButton />
      </ToastProvider>,
    );

    await user.click(screen.getByRole('button', { name: 'Trigger toast' }));

    expect(screen.getByRole('status')).toHaveTextContent('Saved!');
  });

  it('auto-dismisses the toast after the configured timeout', async () => {
    const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });

    render(
      <ToastProvider dismissAfterMs={1000}>
        <TriggerButton />
      </ToastProvider>,
    );

    await user.click(screen.getByRole('button', { name: 'Trigger toast' }));
    expect(screen.getByRole('status')).toBeInTheDocument();

    vi.advanceTimersByTime(1000);

    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });
});
