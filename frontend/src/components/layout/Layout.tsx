import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import { useAuth } from '@/features/auth';
import { Spinner } from '@/components/ui/Spinner';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { PageContainer } from '@/components/layout/PageContainer';
import { Sidebar } from '@/components/layout/Sidebar';

export const Layout = () => {
  const { token } = useAuth();

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <div className="flex flex-1">
        {token && <Sidebar />}
        <PageContainer>
          <Suspense
            fallback={
              <div className="flex h-full items-center justify-center">
                <Spinner />
              </div>
            }
          >
            <Outlet />
          </Suspense>
        </PageContainer>
      </div>
      <Footer />
    </div>
  );
};
