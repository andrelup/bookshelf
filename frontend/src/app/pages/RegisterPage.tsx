import { Link } from 'react-router-dom';
import { RegisterForm } from '@/features/auth';

const RegisterPage = () => (
  <>
    <h1 className="mb-6 text-2xl font-bold text-gray-900">Crear cuenta</h1>
    <RegisterForm />
    <p className="mt-4 text-sm text-gray-600">
      ¿Ya tienes cuenta?{' '}
      <Link to="/login" className="font-medium text-primary hover:underline">
        Inicia sesión
      </Link>
    </p>
  </>
);

// Default export required for React.lazy().
export default RegisterPage;
