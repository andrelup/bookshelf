import type { ReactNode } from 'react';

interface PageContainerProps {
  children: ReactNode;
}

export const PageContainer = ({ children }: PageContainerProps) => (
  <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-8">{children}</main>
);
