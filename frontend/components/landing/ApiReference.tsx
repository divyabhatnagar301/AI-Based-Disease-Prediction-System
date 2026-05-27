import { API_ENDPOINTS } from "@/lib/models";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";

const METHOD_COLORS: Record<string, string> = {
  GET: "bg-sky-50 text-sky-700",
  POST: "bg-emerald-50 text-emerald-700",
  PUT: "bg-amber-50 text-amber-800",
  DELETE: "bg-rose-50 text-rose-700",
};

export function ApiReference() {
  return (
    <section id="api" className="bg-slate-900 py-20 text-white sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight">API reference</h2>
          <p className="mt-4 text-slate-400">
            All routes exposed by the Flask backend. Authenticated routes require{" "}
            <code className="rounded bg-slate-800 px-1.5 py-0.5 text-sm text-teal-300">
              Authorization: Bearer &lt;token&gt;
            </code>
          </p>
        </div>
        <Card className="mt-10 overflow-hidden border-slate-700 bg-slate-800/50">
          <CardBody className="p-0">
            <ul className="divide-y divide-slate-700">
              {API_ENDPOINTS.map((ep) => (
                <li
                  key={`${ep.method}-${ep.path}`}
                  className="flex flex-col gap-2 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6"
                >
                  <div className="flex flex-wrap items-center gap-3">
                    <span
                      className={`rounded-md px-2 py-0.5 font-mono text-xs font-semibold ${METHOD_COLORS[ep.method]}`}
                    >
                      {ep.method}
                    </span>
                    <code className="font-mono text-sm text-slate-200">
                      {ep.path}
                    </code>
                  </div>
                  <div className="flex gap-2">
                    <Badge variant="muted" className="bg-slate-700 text-slate-300 ring-slate-600">
                      {ep.tag}
                    </Badge>
                    {ep.auth && (
                      <Badge className="bg-teal-900/50 text-teal-300 ring-teal-700">
                        Auth
                      </Badge>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      </div>
    </section>
  );
}
