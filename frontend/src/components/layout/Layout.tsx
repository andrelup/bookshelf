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
      <div className="flex min-h-0 flex-1">
        {token && <Sidebar />}
        <div className="flex min-w-0 flex-1 flex-col">
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
          <Footer />
        </div>
      </div>
    </div>
  );
};
