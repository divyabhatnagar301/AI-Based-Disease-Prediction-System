import Link from "next/link";
import { Activity } from "lucide-react";
import { MODELS } from "@/lib/models";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-10 md:grid-cols-4">
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center gap-2 font-semibold text-slate-900">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white">
                <Activity className="h-4 w-4" />
              </span>
              MediPredict
            </Link>
            <p className="mt-3 max-w-sm text-sm leading-relaxed text-slate-600">
              AI-powered multi-disease prediction platform. Connects to Flask ML
              APIs for diabetes, heart, kidney, liver, and ECG analysis.
            </p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-900">Models</h3>
            <ul className="mt-3 space-y-2">
              {MODELS.map((m) => (
                <li key={m.id}>
                  <Link
                    href={`/predict/${m.slug}`}
                    className="text-sm text-slate-600 hover:text-teal-600"
                  >
                    {m.shortName}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-900">Platform</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>
                <Link href="/dashboard" className="hover:text-teal-600">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/history" className="hover:text-teal-600">
                  History
                </Link>
              </li>
              <li>
                <Link href="/models" className="hover:text-teal-600">
                  API & Models
                </Link>
              </li>
              <li>
                <Link href="/signup" className="hover:text-teal-600">
                  Create account
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <p className="mt-10 border-t border-slate-200 pt-6 text-center text-xs text-slate-500">
          For research and education only — not a substitute for professional medical advice.
        </p>
      </div>
    </footer>
  );
}
