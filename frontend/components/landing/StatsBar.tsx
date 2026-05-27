"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { MODELS } from "@/lib/models";

export function StatsBar() {
  const [loaded, setLoaded] = useState(0);
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    api
      .health()
      .then((h) => {
        setOnline(h.status === "healthy");
        setLoaded(
          Object.values(h.models_loaded).filter(Boolean).length
        );
      })
      .catch(() => setOnline(false));
  }, []);

  const stats = [
    { label: "Disease models", value: String(MODELS.length) },
    { label: "Models loaded", value: online === null ? "—" : String(loaded) },
    { label: "API status", value: online === null ? "Checking…" : online ? "Online" : "Offline" },
    { label: "API endpoints", value: "14+" },
  ];

  return (
    <section className="border-y border-slate-200 bg-white" aria-label="Platform stats">
      <div className="mx-auto grid max-w-7xl grid-cols-2 gap-6 px-4 py-10 sm:grid-cols-4 sm:px-6 lg:px-8">
        {stats.map((s) => (
          <div key={s.label} className="text-center">
            <p className="text-3xl font-bold text-slate-900">{s.value}</p>
            <p className="mt-1 text-sm text-slate-500">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
