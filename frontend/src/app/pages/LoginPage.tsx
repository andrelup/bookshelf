import { LoginForm } from '@/features/auth';

const LoginPage = () => (
  <>
    <h1 className="mb-6 text-2xl font-bold text-gray-900">Log in</h1>
    <LoginForm />
  </>
);

// Default export required for React.lazy().
export default LoginPage;
