"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { api, type User } from "@/lib/api";
import { clearAuth, getStoredUser, getToken, setAuth } from "@/lib/auth";

type AuthContextValue = {
  user: User | null;
  token: string | null;
  loading: boolean;
  signIn: (token: string, user: User) => void;
  signOut: () => void;
  refreshProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const signOut = useCallback(() => {
    clearAuth();
    setToken(null);
    setUser(null);
  }, []);

  const signIn = useCallback((t: string, u: User) => {
    setAuth(t, u);
    setToken(t);
    setUser(u);
  }, []);

  const refreshProfile = useCallback(async () => {
    const t = getToken();
    if (!t) return;
    try {
      const { user: profile } = await api.profile(t);
      setUser(profile);
      setAuth(t, profile);
    } catch {
      signOut();
    }
  }, [signOut]);

  useEffect(() => {
    const t = getToken();
    const stored = getStoredUser<User>();
    if (t && stored) {
      setToken(t);
      setUser(stored);
      api.profile(t).then(({ user: profile }) => {
        setUser(profile);
        setAuth(t, profile);
      }).catch(() => signOut()).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [signOut]);

  const value = useMemo(
    () => ({ user, token, loading, signIn, signOut, refreshProfile }),
    [user, token, loading, signIn, signOut, refreshProfile]
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
