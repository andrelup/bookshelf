import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
}

export const Card = ({ children, className = '' }: CardProps) => (
  <div className={`rounded-lg border border-gray-200 bg-white p-4 shadow-sm ${className}`}>
    {children}
  </div>
);
