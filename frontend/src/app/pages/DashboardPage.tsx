import { PageContainer } from '@/components/layout/PageContainer';
import { useAuth } from '@/features/auth';

/** Example protected page, only reachable when the user is authenticated. */
const DashboardPage = () => {
  const { user } = useAuth();

  return (
    <PageContainer>
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p className="mt-2 text-gray-600">
        {user ? `Signed in as ${user.email}` : 'Loading user...'}
      </p>
    </PageContainer>
  );
};

// Default export required for React.lazy().
export default DashboardPage;
