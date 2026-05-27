import { Brain, Clock, LineChart, Lock } from "lucide-react";
import { Card, CardBody } from "@/components/ui/Card";

const FEATURES = [
  {
    icon: Brain,
    title: "Multi-model intelligence",
    description:
      "Diabetes RF, heart RF, kidney logistic, liver XGBoost, and LSTM ECG — each with dedicated forms and feature metadata from the API.",
  },
  {
    icon: Lock,
    title: "Secure by design",
    description:
      "JWT authentication on predict and history routes. Sign up, sign in, and manage your session from the dashboard.",
  },
  {
    icon: LineChart,
    title: "Prediction history",
    description:
      "Every run is stored via the API. Browse, filter by disease type, and review past results with confidence scores.",
  },
  {
    icon: Clock,
    title: "Live API health",
    description:
      "Health and models/info endpoints power status indicators so you know which models are loaded before you predict.",
  },
];

export function Features() {
  return (
    <section className="bg-slate-50 py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-slate-900">
            Built for clinicians & researchers
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            A complete frontend layer over your disease prediction backend.
          </p>
        </div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2">
          {FEATURES.map((f) => (
            <Card key={f.title}>
              <CardBody className="flex gap-4">
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-teal-50 text-teal-600">
                  <f.icon className="h-5 w-5" aria-hidden />
                </span>
                <div>
                  <h3 className="font-semibold text-slate-900">{f.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-slate-600">
                    {f.description}
                  </p>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
