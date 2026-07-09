import { useState } from "react";
import ReactMarkdown from "react-markdown";
import clsx from "clsx";
import { FileText, AlertTriangle, ChevronDown, BookOpen } from "lucide-react";
import type { ChatMessage } from "@/types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const [sourcesOpen, setSourcesOpen] = useState(false);

  const citationCount = message.citations?.length ?? 0;

  return (
    <div className={clsx("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div
        className={clsx(
          "max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
          isUser
            ? "brand-gradient text-white"
            : message.error
              ? "border border-red-200 bg-red-50 text-red-700"
              : "border border-slate-200 bg-white text-slate-800",
        )}
      >
        {message.error && !isUser && (
          <div className="mb-1 flex items-center gap-1.5 text-xs font-medium">
            <AlertTriangle className="h-3.5 w-3.5" />
            Something went wrong
          </div>
        )}

        {message.pending && !message.content ? (
          <span className="flex items-center gap-1 py-1">
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400" />
          </span>
        ) : isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="prose prose-sm max-w-none prose-p:my-1.5 prose-pre:bg-slate-900 prose-pre:text-slate-100">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}

        {citationCount > 0 && (
          <div className="mt-2 border-t border-slate-100 pt-2">
            <button
              onClick={() => setSourcesOpen((v) => !v)}
              className="flex items-center gap-1.5 rounded-md px-1.5 py-1 text-xs font-medium text-slate-500 transition-colors hover:bg-slate-50 hover:text-slate-700"
            >
              <BookOpen className="h-3.5 w-3.5" />
              Sources ({citationCount})
              <ChevronDown
                className={clsx(
                  "h-3.5 w-3.5 transition-transform",
                  sourcesOpen && "rotate-180",
                )}
              />
            </button>

            {sourcesOpen && (
              <div className="mt-1.5 flex flex-col gap-1 animate-fade-in">
                {message.citations?.map((citation, idx) => (
                  <div
                    key={`${citation.filename}-${idx}`}
                    className="flex items-center gap-2 rounded-md bg-slate-50 px-2.5 py-1.5 text-xs text-slate-600"
                  >
                    <span className="flex h-4 w-4 flex-shrink-0 items-center justify-center rounded bg-slate-200 text-[10px] font-medium text-slate-500">
                      {idx + 1}
                    </span>
                    <FileText className="h-3.5 w-3.5 flex-shrink-0 text-slate-400" />
                    <span className="truncate">{citation.filename}</span>
                    {citation.page !== null && citation.page !== undefined && (
                      <span className="ml-auto flex-shrink-0 text-slate-400">
                        p.{citation.page}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}