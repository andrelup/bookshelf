import { useEffect, useState, type FormEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useToast } from '@/hooks/useToast';
import { useLogin } from '../hooks/useLogin';

/** Shape of the `location.state` set by `ProtectedRoute` when redirecting here. */
interface LoginLocationState {
  from?: { pathname: string };
}

export const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { execute, isLoading, error } = useLogin();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (error) {
      showToast({ type: 'error', message: error });
    }
  }, [error, showToast]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    const result = await execute({ email, password });
    if (result !== null) {
      showToast({ type: 'success', message: 'Logged in successfully' });
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
      <Button type="submit" isLoading={isLoading}>
        Log in
      </Button>
    </form>
  );
};
