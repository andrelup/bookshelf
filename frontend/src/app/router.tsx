import { lazy, Suspense, type ReactNode } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import { Spinner } from '@/components/ui/Spinner';
import { ProtectedRoute } from '@/features/auth';

const HomePage = lazy(() => import('./pages/HomePage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));

const withSuspense = (element: ReactNode) => (
  <Suspense
    fallback={
      <div className="flex h-screen items-center justify-center">
        <Spinner />
      </div>
    }
  >
    {element}
  </Suspense>
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: withSuspense(<HomePage />),
  },
  {
    path: '/login',
    element: withSuspense(<LoginPage />),
  },
  {
    path: '/register',
    element: withSuspense(<RegisterPage />),
  },
  {
    path: '/dashboard',
    element: withSuspense(
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>,
    ),
  },
]);
