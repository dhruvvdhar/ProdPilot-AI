import type { ReactNode } from "react";
import logo from "@/assets/logo.png";

export function AuthLayout({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <div className="flex min-h-screen w-full bg-surface">
      <div className="hidden flex-1 flex-col justify-between brand-gradient p-10 text-white lg:flex">
        <div className="flex items-center gap-2.5">
          <img src={logo} alt="ProdPilot AI" className="h-9 w-9 rounded-lg bg-white/10 p-1" />
          <span className="text-lg font-semibold">ProdPilot AI</span>
        </div>

        <div>
          <h1 className="max-w-md text-3xl font-semibold leading-tight">
            Grounded answers for production incidents, in seconds.
          </h1>
          <p className="mt-4 max-w-md text-sm text-white/80">
            Hybrid search, cross-encoder reranking, and citation-backed AI responses over your
            runbooks, logs, and dashboards.
          </p>
        </div>

        <p className="text-xs text-white/60">
          © {new Date().getFullYear()} ProdPilot AI. Enterprise AI-Powered Production Support
          Platform.
        </p>
      </div>

      <div className="flex flex-1 items-center justify-center p-6 sm:p-10">
        <div className="w-full max-w-sm">
          <div className="mb-8 flex flex-col items-center gap-3 lg:hidden">
            <img src={logo} alt="ProdPilot AI" className="h-12 w-12 rounded-xl" />
          </div>

          <h2 className="text-xl font-semibold text-slate-900">{title}</h2>
          <p className="mt-1 text-sm text-slate-500">{subtitle}</p>

          <div className="mt-6">{children}</div>
        </div>
      </div>
    </div>
  );
}
