"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, History, Server } from "lucide-react";
import { AuthGuard } from "@/components/auth/AuthGuard";
import { useAuth } from "@/contexts/AuthContext";
import { api, type HealthResponse } from "@/lib/api";
import { MODELS } from "@/lib/models";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatPercent } from "@/lib/utils";

function DashboardContent() {
  const { user } = useAuth();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [models, setModels] = useState<Record<string, { accuracy: number; loaded: boolean }>>({});

  useEffect(() => {
    api.health().then(setHealth).catch(() => setHealth(null));
    api.modelsInfo().then((r) => {
      const m: Record<string, { accuracy: number; loaded: boolean }> = {};
      Object.entries(r.models).forEach(([k, v]) => {
        m[k] = { accuracy: v.accuracy, loaded: v.loaded };
      });
      setModels(m);
    }).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
          <p className="mt-1 text-slate-600">
            Welcome back, {user?.full_name || user?.username}
          </p>
        </div>
        <Link href="/history">
          <Button variant="secondary">
            <History className="h-4 w-4" />
            View history
          </Button>
        </Link>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <Card>
          <CardBody>
            <p className="text-sm text-slate-500">API status</p>
            <p className="mt-1 text-xl font-bold text-slate-900">
              {health?.status === "healthy" ? "Healthy" : "Unavailable"}
            </p>
            <Badge
              variant={health?.status === "healthy" ? "success" : "warning"}
              className="mt-2"
            >
              <Server className="mr-1 inline h-3 w-3" />
              {process.env.NEXT_PUBLIC_API_URL || "localhost:5000"}
            </Badge>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <p className="text-sm text-slate-500">Models loaded</p>
            <p className="mt-1 text-xl font-bold text-slate-900">
              {health
                ? Object.values(health.models_loaded).filter(Boolean).length
                : "—"}{" "}
              / {MODELS.length}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <p className="text-sm text-slate-500">Your account</p>
            <p className="mt-1 font-medium text-slate-900">{user?.email}</p>
          </CardBody>
        </Card>
      </div>

      <h2 className="mt-12 text-xl font-semibold text-slate-900">
        Run a prediction
      </h2>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {MODELS.map((m) => {
          const Icon = m.icon;
          const info = models[m.apiType];
          return (
            <Link key={m.id} href={`/predict/${m.slug}`}>
              <Card className="h-full transition-shadow hover:shadow-md">
                <CardBody className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span
                      className={`flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br ${m.gradient} text-white`}
                    >
                      <Icon className="h-5 w-5" />
                    </span>
                    <div>
                      <p className="font-semibold text-slate-900">{m.shortName}</p>
                      {info?.loaded && (
                        <p className="text-xs text-teal-600">
                          {formatPercent(info.accuracy)} accuracy
                        </p>
                      )}
                      {!info?.loaded && info !== undefined && (
                        <p className="text-xs text-amber-600">Not loaded</p>
                      )}
                    </div>
                  </div>
                  <ArrowRight className="h-5 w-5 text-slate-300" />
                </CardBody>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  );
}
