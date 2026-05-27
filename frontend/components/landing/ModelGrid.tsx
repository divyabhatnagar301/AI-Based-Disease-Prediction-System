import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { MODELS } from "@/lib/models";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export function ModelGrid() {
  return (
    <section id="models" className="py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Every model, one click away
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            Each card links to a dedicated prediction workspace connected to its
            Flask API route.
          </p>
        </div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {MODELS.map((model) => {
            const Icon = model.icon;
            return (
              <Link
                key={model.id}
                href={`/predict/${model.slug}`}
                className="group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 rounded-2xl"
              >
                <Card className="h-full transition-all duration-200 group-hover:border-teal-200 group-hover:shadow-lg group-hover:shadow-teal-500/10">
                  <CardBody>
                    <div className="flex items-start justify-between">
                      <span
                        className={`flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${model.gradient} text-white shadow-md`}
                      >
                        <Icon className="h-6 w-6" aria-hidden />
                      </span>
                      <ArrowUpRight
                        className="h-5 w-5 text-slate-300 transition-colors group-hover:text-teal-600"
                        aria-hidden
                      />
                    </div>
                    <h3 className="mt-4 text-lg font-semibold text-slate-900">
                      {model.name}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-slate-600">
                      {model.description}
                    </p>
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Badge variant="muted">{model.sampleHint}</Badge>
                    </div>
                    <p className="mt-3 font-mono text-xs text-slate-400">
                      {model.endpoint}
                    </p>
                  </CardBody>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}
