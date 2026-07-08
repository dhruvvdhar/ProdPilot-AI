import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { authApi } from "@/api/auth";
import { registerUnauthorizedHandler } from "@/api/client";
import { tokenStorage } from "@/lib/tokenStorage";
import type { UserCreate, UserLogin, UserResponse } from "@/types";

interface AuthContextValue {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isBootstrapping: boolean;
  login: (payload: UserLogin) => Promise<void>;
  register: (payload: UserCreate) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isBootstrapping, setIsBootstrapping] = useState(true);

  const logout = useCallback(() => {
    tokenStorage.clear();
    setUser(null);
  }, []);

  useEffect(() => {
    registerUnauthorizedHandler(logout);
  }, [logout]);

  useEffect(() => {
    const token = tokenStorage.get();
    if (!token) {
      setIsBootstrapping(false);
      return;
    }

    authApi
      .me()
      .then(setUser)
      .catch(() => tokenStorage.clear())
      .finally(() => setIsBootstrapping(false));
  }, []);

  const login = useCallback(async (payload: UserLogin) => {
    const token = await authApi.login(payload);
    tokenStorage.set(token.access_token);
    const me = await authApi.me();
    setUser(me);
  }, []);

  const register = useCallback(async (payload: UserCreate) => {
    await authApi.register(payload);
    await login({ email: payload.email, password: payload.password });
  }, [login]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isBootstrapping,
      login,
      register,
      logout,
    }),
    [user, isBootstrapping, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
