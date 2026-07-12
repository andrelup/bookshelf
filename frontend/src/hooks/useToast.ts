import { useContext } from 'react';
import { ToastContext } from '@/components/ui/toast-context';

/**
 * Generic hook to trigger toasts from anywhere in the app. Must be used
 * within a `ToastProvider` — throws otherwise.
 *
 * @example
 * const { showToast } = useToast();
 * showToast({ type: 'success', message: 'Saved!' });
 */
export const useToast = () => {
  const context = useContext(ToastContext);
  if (context === null) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};
