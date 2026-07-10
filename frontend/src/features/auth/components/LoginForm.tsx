import { useState, type FormEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useLogin } from '../hooks/useLogin';

/** Shape of the `location.state` set by `ProtectedRoute` when redirecting here. */
interface LoginLocationState {
  from?: { pathname: string };
}

export const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { execute, isLoading, error } = useLogin();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    const result = await execute({ email, password });
    if (result !== null) {
      const state = location.state as LoginLocationState | null;
      const destination = state?.from?.pathname ?? '/';
      navigate(destination, { replace: true });
    }
  };

  return (
    <form onSubmit={(event) => void handleSubmit(event)} className="flex flex-col gap-4" noValidate>
      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        required
      />
      <Input
        label="Password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
      />
      {error && (
        <p role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}
      <Button type="submit" isLoading={isLoading}>
        Log in
      </Button>
    </form>
  );
};
