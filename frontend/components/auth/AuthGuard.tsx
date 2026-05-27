"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <span
          className="h-8 w-8 animate-spin rounded-full border-2 border-teal-600 border-t-transparent"
          aria-label="Loading"
        />
      </div>
    );
  }

  if (!user) return null;
  return <>{children}</>;
}
