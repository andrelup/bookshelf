import { useNavigate } from 'react-router-dom';
// Cross-cutting exception to the "components/ imports from no feature" rule:
// auth is global Context state (the same reasoning `ProtectedRoute` already
// relies on), so the Sidebar reads it directly via `useAuth()` instead of
// receiving `user`/`onLogout` as props.
import { useAuth } from '@/features/auth';
import { Avatar } from '@/components/ui/Avatar';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';

export interface SidebarProps {
  className?: string;
}

/** Left sidebar shown for logged-in users: avatar, name, and a logout button. */
export const Sidebar = ({ className = '' }: SidebarProps) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside
      className={`flex w-64 flex-col items-center gap-2 border-r border-gray-200 bg-white px-4 py-6 ${className}`}
    >
      {user ? (
        <>
          <Avatar name={user.name} size="lg" />
          <span className="text-center font-medium text-gray-900">{user.name}</span>
        </>
      ) : (
        <Spinner />
      )}
      <div className="flex-1" />
      <Button variant="danger" onClick={handleLogout} className="w-full">
        Log out
      </Button>
    </aside>
  );
};
