import { useEffect, useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useApi } from '@/hooks/useApi';
import { useToast } from '@/hooks/useToast';
import { registerUser } from '../api/auth-api';
import type { UserRole } from '../types';

export const RegisterForm = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [role] = useState<UserRole>('customer');
  const { execute, isLoading, error } = useApi(registerUser);
  const { showToast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    if (error) {
      showToast({ type: 'error', message: error });
    }
  }, [error, showToast]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    const result = await execute({ email, name, password, role });
    if (result !== null) {
      showToast({ type: 'success', message: 'Account created successfully' });
      // Registration only creates the account — there is no session to
      // start yet, so the user must log in explicitly.
      navigate('/login', { replace: true });
    }
  };

  return (
    <form onSubmit={(event) => void handleSubmit(event)} className="flex flex-col gap-4" noValidate>
      <Input
        label="Name"
        type="text"
        value={name}
        onChange={(event) => setName(event.target.value)}
        required
      />
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
        Register
      </Button>
    </form>
  );
};
