import { useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import { Send, Square } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface ChatInputProps {
  disabled?: boolean;
  isSending: boolean;
  onSend: (question: string) => void;
  onStop: () => void;
}

const MAX_QUERY_LENGTH = 1000;

export function ChatInput({ disabled, isSending, onSend, onStop }: ChatInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || isSending) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-slate-200 bg-white p-4">
      <div className="flex items-end gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2 focus-within:border-brand-300 focus-within:ring-2 focus-within:ring-brand-100">
        <textarea
          ref={textareaRef}
          value={value}
          maxLength={MAX_QUERY_LENGTH}
          placeholder="Ask about an incident, runbook, or log…"
          disabled={disabled}
          rows={1}
          onChange={(e) => {
            setValue(e.target.value);
            e.target.style.height = "auto";
            e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
          }}
          onKeyDown={handleKeyDown}
          className="max-h-40 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none disabled:opacity-60"
        />

        {isSending ? (
          <Button variant="secondary" size="sm" onClick={onStop} icon={<Square className="h-3.5 w-3.5" />}>
            Stop
          </Button>
        ) : (
          <Button
            size="sm"
            onClick={handleSend}
            disabled={disabled || !value.trim()}
            icon={<Send className="h-3.5 w-3.5" />}
          >
            Send
          </Button>
        )}
      </div>
      <p className="mt-1.5 text-right text-xs text-slate-400">
        {value.length}/{MAX_QUERY_LENGTH}
      </p>
    </div>
  );
}
