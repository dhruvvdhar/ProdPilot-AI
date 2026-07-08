import ReactMarkdown from "react-markdown";
import clsx from "clsx";
import { FileText, AlertTriangle } from "lucide-react";
import type { ChatMessage } from "@/types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

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

        {message.citations && message.citations.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5 border-t border-slate-100 pt-2">
            {message.citations.map((citation, idx) => (
              <span
                key={`${citation.filename}-${idx}`}
                className="inline-flex items-center gap-1 rounded-md bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                title={citation.filename}
              >
                <FileText className="h-3 w-3" />
                {citation.filename}
                {citation.page !== null && citation.page !== undefined && (
                  <span className="text-slate-400">· p.{citation.page}</span>
                )}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
