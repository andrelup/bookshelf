import { PageContainer } from '@/components/layout/PageContainer';

const HomePage = () => (
  <PageContainer>
    <h1 className="text-2xl font-bold text-gray-900">Welcome to BookShelf</h1>
    <p className="mt-2 text-gray-600">Your AI-powered bookstore.</p>
  </PageContainer>
);

// Default export required for React.lazy().
export default HomePage;
