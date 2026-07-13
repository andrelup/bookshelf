import type { ReactNode } from 'react';
import { NavLink } from 'react-router-dom';
// Cross-cutting exception to the "components/ imports from no feature" rule:
// auth is global Context state (the same reasoning `Sidebar`/`Header` already
// rely on), so the tab bar reads it directly via `useAuth()` instead of
// receiving `user` as a prop.
import { useAuth } from '@/features/auth';

const HomeIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M3 11l9-7 9 7" />
    <path d="M5 10v9a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-9" />
  </svg>
);

const DashboardIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <rect x="3" y="4" width="18" height="4" rx="1" />
    <rect x="3" y="11" width="10" height="9" rx="1" />
    <rect x="15" y="11" width="6" height="9" rx="1" />
  </svg>
);

const CatalogIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <rect x="3" y="3" width="7" height="7" rx="1.5" />
    <rect x="14" y="3" width="7" height="7" rx="1.5" />
    <rect x="3" y="14" width="7" height="7" rx="1.5" />
    <rect x="14" y="14" width="7" height="7" rx="1.5" />
  </svg>
);

const AccountIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <circle cx="12" cy="8" r="4" />
    <path d="M4 20c0-4 3.6-6 8-6s8 2 8 6" />
  </svg>
);

const CartTabIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <circle cx="9" cy="20" r="1.3" />
    <circle cx="17" cy="20" r="1.3" />
    <path d="M2 3h3l2.3 12.1a1.5 1.5 0 0 0 1.5 1.2h8a1.5 1.5 0 0 0 1.5-1.2L22 7H6" />
  </svg>
);

const FavoritesIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8Z" />
  </svg>
);

const PlusIcon = () => (
  <svg
    className="h-5 w-5"
    viewBox="0 0 24 24"
    fill="none"
    stroke="#fff"
    strokeWidth={2.3}
    strokeLinecap="round"
    aria-hidden="true"
  >
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const tabClassName = (isActive: boolean) =>
  `flex flex-col items-center justify-center gap-[3px] text-[10px] ${
    isActive ? 'text-primary-dark font-bold' : 'text-muted'
  }`;

// Used by tabs living in a `justify-around` group (seller's left/right cells),
// which size themselves to their content.
const navLinkClassName = ({ isActive }: { isActive: boolean }) => tabClassName(isActive);

// Used by tabs that must share the bar equally (customer's 5-tab row).
const navLinkClassNameFlex = ({ isActive }: { isActive: boolean }) =>
  `flex-1 ${tabClassName(isActive)}`;

interface InactiveTabProps {
  label: string;
  icon: ReactNode;
  badge?: number;
  className?: string;
}

// Visual-only tab: no page exists yet for it, so it is not wrapped in a
// `NavLink`. Turn it into a real `NavLink` once its route exists.
const InactiveTab = ({ label, icon, badge, className = '' }: InactiveTabProps) => (
  <div
    className={`flex flex-col items-center justify-center gap-[3px] text-[10px] text-muted ${className}`}
  >
    <span className="relative">
      {icon}
      {badge !== undefined && (
        <span className="absolute -right-2 -top-1 flex h-3.5 w-3.5 items-center justify-center rounded-full border border-surface bg-primary text-[8px] font-bold text-white">
          {badge}
        </span>
      )}
    </span>
    <span>{label}</span>
  </div>
);

const barClassName =
  'md:hidden fixed inset-x-0 bottom-0 z-40 h-16 bg-surface border-t border-border';

const SellerTabBar = () => (
  <>
    {/*
      BACKLOG: once "Mis libros", "Ventas y pedidos", "Mensajes" and
      "Ajustes" have their own screens, group them inside the "Cuenta" tab
      (as a menu screen) instead of reintroducing the hamburger menu.
    */}
    <nav aria-label="Navegación móvil" className={barClassName}>
      <div className="grid h-full grid-cols-[1fr_64px_1fr] items-stretch">
        <div className="flex items-center justify-around px-3.5">
          <NavLink to="/" end className={navLinkClassName}>
            <HomeIcon />
            <span>Inicio</span>
          </NavLink>
          <NavLink to="/dashboard" className={navLinkClassName}>
            <DashboardIcon />
            <span>Dashboard</span>
          </NavLink>
        </div>

        <div />

        <div className="flex items-center justify-around px-3.5">
          <InactiveTab label="Catálogo" icon={<CatalogIcon />} />
          <InactiveTab label="Cuenta" icon={<AccountIcon />} />
        </div>
      </div>

      <button
        type="button"
        // TODO: open "Publicar libro"
        className="absolute bottom-[23px] left-1/2 flex -translate-x-1/2 flex-col items-center gap-[5px]"
      >
        <span className="flex h-12 w-12 items-center justify-center rounded-full border-4 border-bg bg-primary shadow-float">
          <PlusIcon />
        </span>
        <span className="text-[8.5px] font-semibold text-primary-dark">Añadir libro</span>
      </button>
    </nav>
  </>
);

const CustomerTabBar = () => (
  <nav aria-label="Navegación móvil" className={barClassName}>
    <div className="flex h-full items-stretch">
      <NavLink to="/" end className={navLinkClassNameFlex}>
        <HomeIcon />
        <span>Inicio</span>
      </NavLink>
      <InactiveTab label="Catálogo" icon={<CatalogIcon />} className="flex-1" />
      {/* TODO: connect to real cart count when the cart feature exists */}
      <InactiveTab label="Carrito" icon={<CartTabIcon />} badge={3} className="flex-1" />
      <InactiveTab label="Favoritos" icon={<FavoritesIcon />} className="flex-1" />
      <InactiveTab label="Cuenta" icon={<AccountIcon />} className="flex-1" />
    </div>
  </nav>
);

/**
 * Bottom tab bar shown on mobile (`max-width: 768px`) instead of the
 * `Sidebar`. Renders a role-aware layout: 4 tabs + a central "Añadir libro"
 * FAB for sellers, or 5 equal tabs for customers.
 */
export const MobileTabBar = () => {
  const { user } = useAuth();

  // Avoid a flash of the wrong variant before the role is known.
  if (!user) {
    return null;
  }

  return user.role === 'seller' ? <SellerTabBar /> : <CustomerTabBar />;
};
