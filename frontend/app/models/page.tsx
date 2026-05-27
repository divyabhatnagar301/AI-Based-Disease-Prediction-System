"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, type ModelInfo } from "@/lib/api";
import { API_ENDPOINTS, MODELS } from "@/lib/models";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatPercent } from "@/lib/utils";

export default function ModelsPage() {
  const [models, setModels] = useState<Record<string, ModelInfo>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .modelsInfo()
      .then((r) => setModels(r.models))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-slate-900">Models & API</h1>
      <p className="mt-2 max-w-2xl text-slate-600">
        Live data from GET /api/models/info. Each model links to its prediction
        workspace and Flask endpoint.
      </p>

      <div className="mt-10 grid gap-6 lg:grid-cols-2">
        {MODELS.map((m) => {
          const info = models[m.apiType];
          const Icon = m.icon;
          return (
            <Card key={m.id}>
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span
                      className={`flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br ${m.gradient} text-white`}
                    >
                      <Icon className="h-5 w-5" />
                    </span>
                    <div>
                      <h2 className="font-semibold text-slate-900">{m.name}</h2>
                      <p className="font-mono text-xs text-slate-500">
                        {m.endpoint}
                      </p>
                    </div>
                  </div>
                  {loading ? (
                    <Badge variant="muted">…</Badge>
                  ) : info?.loaded ? (
                    <Badge variant="success">Loaded</Badge>
                  ) : (
                    <Badge variant="warning">Offline</Badge>
                  )}
                </div>
              </CardHeader>
              <CardBody className="pt-0">
                <dl className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <dt className="text-slate-500">Model</dt>
                    <dd className="font-medium">
                      {info?.model_name ?? "—"}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-slate-500">Accuracy</dt>
                    <dd className="font-medium text-teal-700">
                      {info ? formatPercent(info.accuracy) : "—"}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-slate-500">Features</dt>
                    <dd className="font-medium">{info?.feature_count ?? "—"}</dd>
                  </div>
                  <div>
                    <dt className="text-slate-500">Features API</dt>
                    <dd className="font-mono text-xs truncate">
                      {m.featuresEndpoint}
                    </dd>
                  </div>
                </dl>
                <Link
                  href={`/predict/${m.slug}`}
                  className="mt-4 inline-block text-sm font-medium text-teal-600 hover:text-teal-700"
                >
                  Open predictor →
                </Link>
              </CardBody>
            </Card>
          );
        })}
      </div>

      <h2 className="mt-16 text-2xl font-bold text-slate-900">All endpoints</h2>
      <Card className="mt-6 overflow-hidden">
        <ul className="divide-y divide-slate-100">
          {API_ENDPOINTS.map((ep) => (
            <li
              key={`${ep.method}-${ep.path}`}
              className="flex flex-wrap items-center justify-between gap-2 px-6 py-4 text-sm"
            >
              <div className="flex items-center gap-3">
                <span className="font-mono font-semibold text-teal-700">
                  {ep.method}
                </span>
                <code className="text-slate-700">{ep.path}</code>
              </div>
              <div className="flex gap-2">
                <Badge variant="muted">{ep.tag}</Badge>
                {ep.auth && <Badge>Auth required</Badge>}
              </div>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
