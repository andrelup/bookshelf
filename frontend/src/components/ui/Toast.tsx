export type ToastType = 'success' | 'error';

export interface ToastProps {
  type: ToastType;
  message: string;
  onDismiss?: () => void;
}

const variantClasses: Record<ToastType, string> = {
  success: 'bg-green-600 text-white',
  error: 'bg-red-600 text-white',
};

const roleByType: Record<ToastType, 'status' | 'alert'> = {
  success: 'status',
  error: 'alert',
};

export const Toast = ({ type, message, onDismiss }: ToastProps) => {
  const baseClasses = 'flex items-center justify-between gap-4 rounded px-4 py-3 shadow-lg';

  return (
    <div role={roleByType[type]} className={`${baseClasses} ${variantClasses[type]}`}>
      <span className="text-sm font-medium">{message}</span>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          aria-label="Dismiss notification"
          className="text-white/80 hover:text-white"
        >
          &times;
        </button>
      )}
    </div>
  );
};
