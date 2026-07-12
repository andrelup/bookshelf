import type { ReactNode } from 'react';
import { AuthProvider } from '@/features/auth';
import { ToastProvider } from '@/components/ui/ToastProvider';

interface AppProvidersProps {
  children: ReactNode;
}

/** Composes all global providers (toast, auth, etc.) around the app tree. */
export const AppProviders = ({ children }: AppProvidersProps) => (
  <ToastProvider>
    <AuthProvider>{children}</AuthProvider>
  </ToastProvider>
);
