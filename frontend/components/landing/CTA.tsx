import Link from "next/link";
import { Button } from "@/components/ui/Button";

export function CTA() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-teal-600 to-emerald-700 px-8 py-16 text-center shadow-xl shadow-teal-600/25 sm:px-16">
          <div
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.15),transparent_50%)]"
            aria-hidden
          />
          <h2 className="relative text-3xl font-bold text-white sm:text-4xl">
            Ready to run your first prediction?
          </h2>
          <p className="relative mx-auto mt-4 max-w-xl text-teal-50">
            Create a free account, pick a model, and get results in seconds —
            powered by your local Flask API.
          </p>
          <div className="relative mt-8 flex flex-col justify-center gap-4 sm:flex-row">
            <Link href="/signup">
              <Button
                size="lg"
                className="min-w-[160px] bg-white text-teal-700 hover:bg-teal-50 shadow-none"
              >
                Create account
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button
                variant="secondary"
                size="lg"
                className="min-w-[160px] border-white/30 bg-white/10 text-white hover:bg-white/20"
              >
                Open dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
