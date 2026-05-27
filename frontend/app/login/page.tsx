import { Suspense } from "react";
import { AuthForm } from "@/components/auth/AuthForm";

export default function LoginPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <Suspense fallback={<p className="text-center text-slate-500">Loading…</p>}>
        <AuthForm mode="login" />
      </Suspense>
    </div>
  );
}
