import Link from "next/link";
import { ArrowRight, Shield, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-slate-50 via-white to-teal-50/30">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(20,184,166,0.15),transparent)]"
        aria-hidden
      />
      <div className="relative mx-auto max-w-7xl px-4 pb-20 pt-16 sm:px-6 sm:pt-24 lg:px-8 lg:pt-28">
        <div className="mx-auto max-w-3xl text-center">
          <Badge className="mb-6">5 ML models · REST API · Secure auth</Badge>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
            AI disease prediction,{" "}
            <span className="bg-gradient-to-r from-teal-600 to-emerald-600 bg-clip-text text-transparent">
              one modern platform
            </span>
          </h1>
          <p className="mt-6 text-lg leading-relaxed text-slate-600 sm:text-xl">
            Run diabetes, heart, kidney, liver, and ECG predictions through a
            clean interface wired to every API endpoint — with history, model
            insights, and real-time health checks.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/signup">
              <Button size="lg" className="min-w-[180px]">
                Start predicting
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Button>
            </Link>
            <Link href="/models">
              <Button variant="secondary" size="lg" className="min-w-[180px]">
                Explore models & APIs
              </Button>
            </Link>
          </div>
          <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-slate-500">
            <span className="inline-flex items-center gap-2">
              <Shield className="h-4 w-4 text-teal-600" aria-hidden />
              JWT-secured endpoints
            </span>
            <span className="inline-flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-teal-600" aria-hidden />
              Up to 98%+ model accuracy
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
