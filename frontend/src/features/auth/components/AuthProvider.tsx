import { useCallback, useEffect, useState, type ReactNode } from 'react';
import { useLocalStorage } from '@/hooks/useLocalStorage';
import { setAuthToken } from '@/lib/api-client';
import { loginUser } from '../api/auth-api';
import { AuthContext } from '../context/auth-context';
import type { AuthToken, LoginCredentials, User } from '../types';

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provides the authentication state (current user + token) to the whole
 * app via React Context. The token is persisted to `localStorage` and
 * synced with the API client so every request carries the auth header.
 */
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [token, setToken] = useLocalStorage<string | null>('auth-token', null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setAuthToken(token);
  }, [token]);

  const login = useCallback(
    async (credentials: LoginCredentials): Promise<AuthToken> => {
      setIsLoading(true);
      try {
        const authToken = await loginUser(credentials);
        setToken(authToken.accessToken);
        setUser(authToken.user);
        return authToken;
      } finally {
        setIsLoading(false);
      }
    },
    [setToken],
  );

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
  }, [setToken]);

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
