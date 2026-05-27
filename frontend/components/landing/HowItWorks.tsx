import { ClipboardList, Cpu, UserPlus } from "lucide-react";

const STEPS = [
  {
    step: "01",
    icon: UserPlus,
    title: "Create your account",
    description: "Sign up via POST /api/auth/signup and receive a JWT for authenticated requests.",
  },
  {
    step: "02",
    icon: ClipboardList,
    title: "Enter clinical data",
    description:
      "Open any model page — features load from GET /api/models/:type/features with sample values ready to run.",
  },
  {
    step: "03",
    icon: Cpu,
    title: "Get AI predictions",
    description:
      "Submit to the predict endpoint, view probability scores, and find results saved in your history.",
  },
];

export function HowItWorks() {
  return (
    <section className="py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-center text-3xl font-bold text-slate-900">
          How it works
        </h2>
        <div className="mt-14 grid gap-8 md:grid-cols-3">
          {STEPS.map((s, i) => (
            <div key={s.step} className="relative text-center">
              {i < STEPS.length - 1 && (
                <div
                  className="absolute top-8 left-[60%] hidden h-0.5 w-[80%] bg-gradient-to-r from-teal-200 to-transparent md:block"
                  aria-hidden
                />
              )}
              <span className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-teal-500 to-emerald-600 text-white shadow-lg shadow-teal-500/25">
                <s.icon className="h-7 w-7" aria-hidden />
              </span>
              <p className="mt-4 text-xs font-bold uppercase tracking-wider text-teal-600">
                Step {s.step}
              </p>
              <h3 className="mt-2 text-lg font-semibold text-slate-900">
                {s.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">
                {s.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
