import { RegisterForm } from '@/features/auth';

const RegisterPage = () => (
  <>
    <h1 className="mb-6 text-2xl font-bold text-gray-900">Create account</h1>
    <RegisterForm />
  </>
);

// Default export required for React.lazy().
export default RegisterPage;
