import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '@/features/auth';
import { MobileTabBar } from './MobileTabBar';

const rawSellerUser = { id: 1, email: 'ada@example.com', name: 'Ada Lovelace', role: 'seller' };
const rawCustomerUser = { id: 2, email: 'bob@example.com', name: 'Bob Smith', role: 'customer' };

vi.mock('@/lib/api-client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
  setAuthToken: vi.fn(),
}));

const renderTabBar = (initialEntries: string[] = ['/']) =>
  render(
    <AuthProvider>
      <MemoryRouter initialEntries={initialEntries}>
        <MobileTabBar />
      </MemoryRouter>
    </AuthProvider>,
  );

describe('MobileTabBar', () => {
  afterEach(() => {
    window.localStorage.clear();
    vi.clearAllMocks();
  });

  it('renders nothing when there is no session', () => {
    const { container } = renderTabBar();

    expect(container).toBeEmptyDOMElement();
  });

  it('shows the seller tabs (4 tabs + FAB), without Carrito or Favoritos', async () => {
    const { apiClient } = await import('@/lib/api-client');
    vi.mocked(apiClient.get).mockResolvedValueOnce(rawSellerUser);
    window.localStorage.setItem('auth-token', JSON.stringify('test-token'));

    renderTabBar();

    expect(await screen.findByText('Añadir libro')).toBeInTheDocument();
    expect(screen.getByText('Inicio')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Catálogo')).toBeInTheDocument();
    expect(screen.getByText('Cuenta')).toBeInTheDocument();
    expect(screen.queryByText('Carrito')).not.toBeInTheDocument();
    expect(screen.queryByText('Favoritos')).not.toBeInTheDocument();
  });

  it('shows the 5 customer tabs, without the "Añadir libro" FAB', async () => {
    const { apiClient } = await import('@/lib/api-client');
    vi.mocked(apiClient.get).mockResolvedValueOnce(rawCustomerUser);
    window.localStorage.setItem('auth-token', JSON.stringify('test-token'));

    renderTabBar();

    expect(await screen.findByText('Inicio')).toBeInTheDocument();
    expect(screen.getByText('Catálogo')).toBeInTheDocument();
    expect(screen.getByText('Carrito')).toBeInTheDocument();
    expect(screen.getByText('Favoritos')).toBeInTheDocument();
    expect(screen.getByText('Cuenta')).toBeInTheDocument();
    expect(screen.queryByText('Añadir libro')).not.toBeInTheDocument();
  });

  it('marks the "Inicio" tab as active on the home route', async () => {
    const { apiClient } = await import('@/lib/api-client');
    vi.mocked(apiClient.get).mockResolvedValueOnce(rawCustomerUser);
    window.localStorage.setItem('auth-token', JSON.stringify('test-token'));

    renderTabBar(['/']);

    const inicioLabel = await screen.findByText('Inicio');
    const inicioLink = inicioLabel.closest('a');

    expect(inicioLink).toHaveAttribute('aria-current', 'page');
  });
});
