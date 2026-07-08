import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { LogOut, MessageSquare, FileText, Bug } from "lucide-react";
import clsx from "clsx";
import logo from "@/assets/logo.png";
import { useAuth } from "@/context/AuthContext";

const NAV_ITEMS = [
  { to: "/chat", label: "Chat", icon: MessageSquare },
  { to: "/documents", label: "Documents", icon: FileText },
];

export function AppShell() {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="flex h-screen w-full bg-surface">
      <aside className="flex w-[72px] flex-shrink-0 flex-col items-center border-r border-slate-200 bg-white py-4">
        <img src={logo} alt="ProdPilot AI" className="h-9 w-9 rounded-lg" />

        <nav className="mt-8 flex flex-1 flex-col items-center gap-2">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                clsx(
                  "group relative flex h-11 w-11 items-center justify-center rounded-xl transition-colors",
                  isActive
                    ? "brand-gradient text-white shadow-sm"
                    : "text-slate-400 hover:bg-slate-100 hover:text-slate-600",
                )
              }
              title={label}
            >
              <Icon className="h-5 w-5" />
              <span className="pointer-events-none absolute left-full ml-2 whitespace-nowrap rounded-md bg-slate-900 px-2 py-1 text-xs text-white opacity-0 shadow-lg transition-opacity group-hover:opacity-100">
                {label}
              </span>
            </NavLink>
          ))}

          <button
            className="group relative flex h-11 w-11 cursor-not-allowed items-center justify-center rounded-xl text-slate-300"
            title="Report a bug (coming soon)"
            disabled
          >
            <Bug className="h-5 w-5" />
            <span className="pointer-events-none absolute left-full ml-2 whitespace-nowrap rounded-md bg-slate-900 px-2 py-1 text-xs text-white opacity-0 shadow-lg transition-opacity group-hover:opacity-100">
              Report a bug — coming soon
            </span>
          </button>
        </nav>

        <div className="relative">
          <button
            onClick={() => setMenuOpen((v) => !v)}
            className="flex h-10 w-10 items-center justify-center rounded-full brand-gradient text-sm font-semibold text-white"
            title={user?.username}
          >
            {user?.username?.slice(0, 1).toUpperCase() ?? "U"}
          </button>

          {menuOpen && (
            <div className="absolute bottom-0 left-full z-20 ml-2 w-52 rounded-xl border border-slate-200 bg-white p-2 shadow-lg animate-fade-in">
              <div className="px-2 py-1.5">
                <p className="truncate text-sm font-medium text-slate-900">{user?.username}</p>
                <p className="truncate text-xs text-slate-500">{user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="mt-1 flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-sm text-red-600 hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" />
                Log out
              </button>
            </div>
          )}
        </div>
      </aside>

      <main className="flex min-w-0 flex-1 flex-col">
        <Outlet />
      </main>
    </div>
  );
}
