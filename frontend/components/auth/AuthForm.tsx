"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";

type Mode = "login" | "signup";

export function AuthForm({ mode }: { mode: Mode }) {
  const router = useRouter();
  const params = useSearchParams();
  const { signIn } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
  });

  const redirect = params.get("redirect") || "/dashboard";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res =
        mode === "signup"
          ? await api.signup({
              username: form.username,
              email: form.email,
              password: form.password,
              full_name: form.full_name,
            })
          : await api.signin({
              username: form.username,
              password: form.password,
            });
      signIn(res.token, res.user);
      router.push(redirect);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="mx-auto w-full max-w-md">
      <CardHeader>
        <h1 className="text-2xl font-bold text-slate-900">
          {mode === "signup" ? "Create account" : "Welcome back"}
        </h1>
        <p className="mt-1 text-sm text-slate-600">
          {mode === "signup"
            ? "Sign up to access predictions and history."
            : "Sign in to continue to your dashboard."}
        </p>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-slate-700">
              Username
            </label>
            <input
              id="username"
              required
              autoComplete="username"
              value={form.username}
              onChange={(e) => setForm((f) => ({ ...f, username: e.target.value }))}
              className="mt-1 h-11 w-full rounded-xl border border-slate-200 px-3 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          {mode === "signup" && (
            <>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="email"
                  value={form.email}
                  onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                  className="mt-1 h-11 w-full rounded-xl border border-slate-200 px-3 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
                />
              </div>
              <div>
                <label htmlFor="full_name" className="block text-sm font-medium text-slate-700">
                  Full name
                </label>
                <input
                  id="full_name"
                  value={form.full_name}
                  onChange={(e) => setForm((f) => ({ ...f, full_name: e.target.value }))}
                  className="mt-1 h-11 w-full rounded-xl border border-slate-200 px-3 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
                />
              </div>
            </>
          )}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-slate-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              minLength={6}
              autoComplete={mode === "signup" ? "new-password" : "current-password"}
              value={form.password}
              onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
              className="mt-1 h-11 w-full rounded-xl border border-slate-200 px-3 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          {error && (
            <p role="alert" className="text-sm text-rose-600">
              {error}
            </p>
          )}
          <Button type="submit" className="w-full" loading={loading}>
            {mode === "signup" ? "Sign up" : "Sign in"}
          </Button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-600">
          {mode === "signup" ? (
            <>
              Already have an account?{" "}
              <Link href="/login" className="font-medium text-teal-600 hover:text-teal-700">
                Sign in
              </Link>
            </>
          ) : (
            <>
              No account?{" "}
              <Link href="/signup" className="font-medium text-teal-600 hover:text-teal-700">
                Sign up
              </Link>
            </>
          )}
        </p>
      </CardBody>
    </Card>
  );
}
