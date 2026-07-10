import type { ReactNode } from 'react';

interface PageContainerProps {
  children: ReactNode;
}

export const PageContainer = ({ children }: PageContainerProps) => (
  <main className="mx-auto max-w-5xl px-4 py-8">{children}</main>
);
