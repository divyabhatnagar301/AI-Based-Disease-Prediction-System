"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AlertCircle, CheckCircle2, Play } from "lucide-react";
import { api, ApiError, type PredictionResponse } from "@/lib/api";
import {
  generateDemoEcg,
  getModelBySlug,
  SAMPLE_VALUES,
} from "@/lib/models";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { formatPercent } from "@/lib/utils";

export function PredictionForm({ slug }: { slug: string }) {
  const model = getModelBySlug(slug);
  const { token } = useAuth();
  const router = useRouter();
  const [features, setFeatures] = useState<string[]>([]);
  const [descriptions, setDescriptions] = useState<Record<string, string>>({});
  const [values, setValues] = useState<Record<string, string>>({});
  const [ecgJson, setEcgJson] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingFeatures, setLoadingFeatures] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [accuracy, setAccuracy] = useState<number | null>(null);
  const isEcg = model?.apiType === "heart_ecg";

  useEffect(() => {
    if (!token) {
      router.push(`/login?redirect=/predict/${slug}`);
      return;
    }
    if (!model) return;

    api
      .modelFeatures(model.apiType)
      .then((data) => {
        if (isEcg) {
          setAccuracy(data.model_accuracy ?? null);
          setLoadingFeatures(false);
          return;
        }
        const names = data.feature_names ?? [];
        setFeatures(names);
        setDescriptions(data.feature_descriptions ?? {});
        setAccuracy(data.model_accuracy ?? null);
        const sample = SAMPLE_VALUES[model.apiType] ?? {};
        const init: Record<string, string> = {};
        names.forEach((n) => {
          init[n] = sample[n] !== undefined ? String(sample[n]) : "";
        });
        setValues(init);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load features"))
      .finally(() => setLoadingFeatures(false));
  }, [model, token, slug, router, isEcg]);

  if (!model) {
    return (
      <p className="text-center text-slate-600">Model not found.</p>
    );
  }

  const Icon = model.icon;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!token || !model) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      let body: Record<string, unknown>;
      if (isEcg) {
        let signal: number[];
        if (ecgJson.trim()) {
          signal = JSON.parse(ecgJson);
          if (!Array.isArray(signal)) throw new Error("ECG must be a JSON array");
        } else {
          signal = generateDemoEcg();
        }
        body = { ecg_signal: signal };
      } else {
        body = {};
        for (const key of features) {
          const v = values[key];
          if (v === "" || v === undefined) {
            throw new Error(`Missing value for: ${key}`);
          }
          body[key] = Number(v);
        }
      }

      const res = await api.predict(model.endpoint, body, token);
      setResult(res);
    } catch (err) {
      if (err instanceof ApiError) setError(err.message);
      else if (err instanceof SyntaxError) setError("Invalid JSON for ECG signal");
      else setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  function loadSamples() {
    if (!model) return;
    if (isEcg) {
      setEcgJson(JSON.stringify(generateDemoEcg()));
      return;
    }
    const sample = SAMPLE_VALUES[model.apiType] ?? {};
    const next: Record<string, string> = { ...values };
    features.forEach((n) => {
      if (sample[n] !== undefined) next[n] = String(sample[n]);
    });
    setValues(next);
  }

  return (
    <div className="grid gap-8 lg:grid-cols-5">
      <div className="lg:col-span-3">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <span
                className={`flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br ${model.gradient} text-white`}
              >
                <Icon className="h-5 w-5" />
              </span>
              <div>
                <h1 className="text-xl font-bold text-slate-900">{model.name}</h1>
                <p className="font-mono text-xs text-slate-500">{model.endpoint}</p>
              </div>
            </div>
          </CardHeader>
          <CardBody>
            {loadingFeatures ? (
              <p className="text-sm text-slate-500">Loading features from API…</p>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5">
                {isEcg ? (
                  <div>
                    <label
                      htmlFor="ecg"
                      className="block text-sm font-medium text-slate-700"
                    >
                      ECG signal (187 samples JSON array)
                    </label>
                    <p className="mt-1 text-xs text-slate-500">
                      Leave empty to auto-generate a demo waveform, or paste your own array.
                    </p>
                    <textarea
                      id="ecg"
                      rows={6}
                      value={ecgJson}
                      onChange={(e) => setEcgJson(e.target.value)}
                      placeholder='[0.02, 0.01, ...] — 187 numbers'
                      className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2 font-mono text-xs focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
                    />
                  </div>
                ) : (
                  <div className="grid gap-4 sm:grid-cols-2">
                    {features.map((name) => (
                      <div key={name}>
                        <label
                          htmlFor={name}
                          className="block text-sm font-medium text-slate-700"
                        >
                          {name}
                        </label>
                        {descriptions[name] && (
                          <p className="text-xs text-slate-400">{descriptions[name]}</p>
                        )}
                        <input
                          id={name}
                          type="number"
                          step="any"
                          required
                          value={values[name] ?? ""}
                          onChange={(e) =>
                            setValues((v) => ({ ...v, [name]: e.target.value }))
                          }
                          className="mt-1 h-11 w-full rounded-xl border border-slate-200 px-3 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
                        />
                      </div>
                    ))}
                  </div>
                )}

                {error && (
                  <div
                    role="alert"
                    className="flex items-start gap-2 rounded-xl bg-rose-50 px-4 py-3 text-sm text-rose-800"
                  >
                    <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                    {error}
                  </div>
                )}

                <div className="flex flex-wrap gap-3">
                  <Button type="submit" loading={loading}>
                    <Play className="h-4 w-4" />
                    Run prediction
                  </Button>
                  <Button type="button" variant="secondary" onClick={loadSamples}>
                    Load sample data
                  </Button>
                </div>
              </form>
            )}
          </CardBody>
        </Card>
      </div>

      <div className="lg:col-span-2 space-y-6">
        <Card>
          <CardBody>
            <h2 className="font-semibold text-slate-900">Model info</h2>
            <dl className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <dt className="text-slate-500">API route</dt>
                <dd className="font-mono text-xs text-slate-700">{model.endpoint}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-slate-500">Features API</dt>
                <dd className="font-mono text-xs text-slate-700">{model.featuresEndpoint}</dd>
              </div>
              {accuracy != null && (
                <div className="flex justify-between">
                  <dt className="text-slate-500">Accuracy</dt>
                  <dd className="font-medium text-teal-700">{formatPercent(accuracy)}</dd>
                </div>
              )}
            </dl>
          </CardBody>
        </Card>

        {result && (
          <Card className="border-emerald-200 bg-emerald-50/50">
            <CardBody>
              <div className="flex items-center gap-2 text-emerald-800">
                <CheckCircle2 className="h-5 w-5" />
                <h2 className="font-semibold">Result</h2>
              </div>
              <p className="mt-3 text-2xl font-bold text-slate-900">
                {result.prediction}
              </p>
              <p className="mt-1 text-sm text-slate-600">
                Confidence:{" "}
                <strong>{formatPercent(result.probability)}</strong>
              </p>
              {result.model_accuracy != null && (
                <Badge variant="success" className="mt-3">
                  Model accuracy {formatPercent(result.model_accuracy)}
                </Badge>
              )}
              {result.probabilities && result.class_names && (
                <ul className="mt-4 space-y-1 text-xs text-slate-600">
                  {result.class_names.map((name, i) => (
                    <li key={name} className="flex justify-between">
                      <span>{name}</span>
                      <span>{formatPercent(result.probabilities![i])}</span>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        )}
      </div>
    </div>
  );
}
