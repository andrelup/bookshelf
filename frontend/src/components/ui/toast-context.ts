import { createContext } from 'react';
import type { ToastType } from './Toast';

export interface ShowToastInput {
  type: ToastType;
  message: string;
}

export interface ToastContextValue {
  showToast: (toast: ShowToastInput) => void;
}

export const ToastContext = createContext<ToastContextValue | null>(null);
