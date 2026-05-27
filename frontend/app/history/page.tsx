"use client";

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import { AuthGuard } from "@/components/auth/AuthGuard";
import { useAuth } from "@/contexts/AuthContext";
import { api, type PredictionRecord } from "@/lib/api";
import { MODELS } from "@/lib/models";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDate, formatPercent } from "@/lib/utils";

function HistoryContent() {
  const { token } = useAuth();
  const [records, setRecords] = useState<PredictionRecord[]>([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!token) return;
    setLoading(true);
    try {
      const res = await api.predictions(token, {
        disease_type: filter || undefined,
        limit: 50,
      });
      setRecords(res.predictions);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [token, filter]);

  async function handleDelete(id: number) {
    if (!token || !confirm("Delete this prediction?")) return;
    try {
      await api.deletePrediction(id, token);
      setRecords((r) => r.filter((x) => x.id !== id));
    } catch (e) {
      alert(e instanceof Error ? e.message : "Delete failed");
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-slate-900">Prediction history</h1>
      <p className="mt-1 text-slate-600">
        Fetched from GET /api/predictions
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => setFilter("")}
          className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
            filter === ""
              ? "bg-teal-600 text-white"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          All
        </button>
        {MODELS.map((m) => (
          <button
            key={m.id}
            type="button"
            onClick={() => setFilter(m.apiType)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
              filter === m.apiType
                ? "bg-teal-600 text-white"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {m.shortName}
          </button>
        ))}
      </div>

      {loading && (
        <p className="mt-10 text-center text-slate-500">Loading history…</p>
      )}
      {error && (
        <p role="alert" className="mt-10 text-center text-rose-600">
          {error}
        </p>
      )}
      {!loading && !error && records.length === 0 && (
        <Card className="mt-10">
          <CardBody className="text-center py-12">
            <p className="text-slate-600">No predictions yet.</p>
            <p className="mt-1 text-sm text-slate-500">
              Run a model from the dashboard to see results here.
            </p>
          </CardBody>
        </Card>
      )}

      <ul className="mt-8 space-y-4">
        {records.map((r) => (
          <li key={r.id}>
            <Card>
              <CardBody className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge>{r.disease_type}</Badge>
                    <span className="text-xs text-slate-400">
                      #{r.id} · {formatDate(r.created_at)}
                    </span>
                  </div>
                  <p className="mt-2 text-lg font-semibold text-slate-900">
                    {r.prediction_result}
                  </p>
                  <p className="text-sm text-slate-600">
                    Confidence {formatPercent(r.prediction_probability)}
                  </p>
                </div>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => handleDelete(r.id)}
                  aria-label={`Delete prediction ${r.id}`}
                >
                  <Trash2 className="h-4 w-4" />
                  Delete
                </Button>
              </CardBody>
            </Card>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function HistoryPage() {
  return (
    <AuthGuard>
      <HistoryContent />
    </AuthGuard>
  );
}
