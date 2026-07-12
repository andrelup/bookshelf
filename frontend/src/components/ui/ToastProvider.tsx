import { useCallback, useMemo, useState, type ReactNode } from 'react';
import { Toast } from './Toast';
import { ToastContext, type ShowToastInput } from './toast-context';

interface ToastProviderProps {
  children: ReactNode;
  /** How long each toast stays visible before auto-dismissing, in milliseconds. */
  dismissAfterMs?: number;
}

interface ActiveToast extends ShowToastInput {
  id: number;
}

/**
 * Holds the list of active toasts and exposes `showToast` through
 * `ToastContext`. Renders the toasts in a fixed container and auto-dismisses
 * each one after `dismissAfterMs`.
 */
export const ToastProvider = ({ children, dismissAfterMs = 4000 }: ToastProviderProps) => {
  const [toasts, setToasts] = useState<ActiveToast[]>([]);

  const dismissToast = useCallback((id: number) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const showToast = useCallback(
    ({ type, message }: ShowToastInput) => {
      const id = Date.now() + Math.random();
      setToasts((current) => [...current, { id, type, message }]);
      setTimeout(() => dismissToast(id), dismissAfterMs);
    },
    [dismissAfterMs, dismissToast],
  );

  const value = useMemo(() => ({ showToast }), [showToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast) => (
          <Toast
            key={toast.id}
            type={toast.type}
            message={toast.message}
            onDismiss={() => dismissToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
};
