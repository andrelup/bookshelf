import { afterEach, describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from '@/features/auth';
import { ToastProvider } from '@/components/ui/ToastProvider';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';

describe('auth pages navigation', () => {
  afterEach(() => {
    window.localStorage.clear();
  });

  it('navigates between the login and register pages via their links', async () => {
    const user = userEvent.setup();

    render(
      <ToastProvider>
        <AuthProvider>
          <MemoryRouter initialEntries={['/login']}>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
            </Routes>
          </MemoryRouter>
        </AuthProvider>
      </ToastProvider>,
    );

    expect(screen.getByRole('heading', { name: 'Log in' })).toBeInTheDocument();

    await user.click(screen.getByRole('link', { name: 'Regístrate' }));

    expect(screen.getByRole('heading', { name: 'Create account' })).toBeInTheDocument();

    await user.click(screen.getByRole('link', { name: 'Inicia sesión' }));

    expect(screen.getByRole('heading', { name: 'Log in' })).toBeInTheDocument();
  });
});
