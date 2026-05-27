import { cn } from "@/lib/utils";

export function Badge({
  children,
  variant = "default",
  className,
}: {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "muted";
  className?: string;
}) {
  const styles = {
    default: "bg-teal-50 text-teal-700 ring-teal-600/20",
    success: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    warning: "bg-amber-50 text-amber-800 ring-amber-600/20",
    muted: "bg-slate-100 text-slate-600 ring-slate-500/10",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset",
        styles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
