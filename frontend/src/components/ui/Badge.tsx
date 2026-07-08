import clsx from "clsx";
import type { PipelineStatus } from "@/types";

const STATUS_STYLES: Record<string, string> = {
  pending: "bg-slate-100 text-slate-600",
  processing: "bg-amber-100 text-amber-700",
  completed: "bg-emerald-100 text-emerald-700",
  failed: "bg-red-100 text-red-700",
};

export function StatusBadge({ status }: { status: PipelineStatus }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium capitalize",
        STATUS_STYLES[status] ?? "bg-slate-100 text-slate-600",
      )}
    >
      <span
        className={clsx("h-1.5 w-1.5 rounded-full", {
          "bg-slate-400": status === "pending",
          "bg-amber-500 animate-pulse": status === "processing",
          "bg-emerald-500": status === "completed",
          "bg-red-500": status === "failed",
        })}
      />
      {status}
    </span>
  );
}
