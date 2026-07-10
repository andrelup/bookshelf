import { PageContainer } from '@/components/layout/PageContainer';
import { LoginForm } from '@/features/auth';

const LoginPage = () => (
  <PageContainer>
    <h1 className="mb-6 text-2xl font-bold text-gray-900">Log in</h1>
    <LoginForm />
  </PageContainer>
);

// Default export required for React.lazy().
export default LoginPage;
