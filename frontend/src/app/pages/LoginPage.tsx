import { Link } from 'react-router-dom';
import { LoginForm } from '@/features/auth';

const LoginPage = () => (
  <>
    <h1 className="mb-6 text-2xl font-bold text-gray-900">Log in</h1>
    <LoginForm />
    <p className="mt-4 text-sm text-gray-600">
      ¿No tienes cuenta?{' '}
      <Link to="/register" className="font-medium text-primary hover:underline">
        Regístrate
      </Link>
    </p>
  </>
);

// Default export required for React.lazy().
export default LoginPage;
