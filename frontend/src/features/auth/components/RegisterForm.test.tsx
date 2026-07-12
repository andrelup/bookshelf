import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { ApiError } from '@/types/api';
import { ToastProvider } from '@/components/ui/ToastProvider';
import { AuthProvider } from './AuthProvider';
import { RegisterForm } from './RegisterForm';

vi.mock('@/lib/api-client', () => ({
  apiClient: {
    post: vi.fn(async () => ({
      id: 1,
      email: 'user@example.com',
      name: 'Test User',
      role: 'customer',
    })),
    get: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
  setAuthToken: vi.fn(),
}));

describe('RegisterForm', () => {
  afterEach(() => {
    window.localStorage.clear();
    vi.clearAllMocks();
  });

  it('shows a green toast and redirects to /login after a successful registration', async () => {
    const user = userEvent.setup();

    render(
      <ToastProvider>
        <AuthProvider>
          <MemoryRouter initialEntries={['/register']}>
            <Routes>
              <Route path="/register" element={<RegisterForm />} />
              <Route path="/login" element={<h1>Log in</h1>} />
            </Routes>
          </MemoryRouter>
        </AuthProvider>
      </ToastProvider>,
    );

    await user.type(screen.getByLabelText('Name'), 'Test User');
    await user.type(screen.getByLabelText('Email'), 'user@example.com');
    await user.type(screen.getByLabelText('Password'), 'super-secret');
    await user.click(screen.getByRole('button', { name: 'Register' }));

    expect(await screen.findByRole('status')).toHaveTextContent('Account created successfully');
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Log in' })).toBeInTheDocument();
    });
  });

  it('shows a red toast with the backend error message when registration fails', async () => {
    const { apiClient } = await import('@/lib/api-client');
    vi.mocked(apiClient.post).mockRejectedValueOnce(new ApiError('Email already registered', 409));

    const user = userEvent.setup();

    render(
      <ToastProvider>
        <AuthProvider>
          <MemoryRouter initialEntries={['/register']}>
            <Routes>
              <Route path="/register" element={<RegisterForm />} />
            </Routes>
          </MemoryRouter>
        </AuthProvider>
      </ToastProvider>,
    );

    await user.type(screen.getByLabelText('Name'), 'Test User');
    await user.type(screen.getByLabelText('Email'), 'user@example.com');
    await user.type(screen.getByLabelText('Password'), 'super-secret');
    await user.click(screen.getByRole('button', { name: 'Register' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Email already registered');
  });
});
