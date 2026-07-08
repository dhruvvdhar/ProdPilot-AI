import { useEffect, useRef } from "react";
import { MessageSquarePlus } from "lucide-react";
import { MessageBubble } from "@/components/chat/MessageBubble";
import { ChatInput } from "@/components/chat/ChatInput";
import { Spinner } from "@/components/ui/Spinner";
import type { ChatMessage, ConversationResponse } from "@/types";

interface ChatWindowProps {
  conversation: ConversationResponse | null;
  messages: ChatMessage[];
  isLoadingHistory: boolean;
  isSending: boolean;
  onSend: (question: string) => void;
  onStop: () => void;
}

export function ChatWindow({
  conversation,
  messages,
  isLoadingHistory,
  isSending,
  onSend,
  onStop,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (!conversation) {
    return (
      <div className="flex h-full flex-1 flex-col items-center justify-center gap-2 text-slate-400">
        <MessageSquarePlus className="h-10 w-10" />
        <p className="text-sm">Select a conversation or start a new chat.</p>
      </div>
    );
  }

  return (
    <div className="flex h-full min-w-0 flex-1 flex-col">
      <div className="border-b border-slate-200 bg-white px-5 py-3">
        <h2 className="truncate text-sm font-semibold text-slate-800">{conversation.title}</h2>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-4">
        {isLoadingHistory ? (
          <div className="flex h-full items-center justify-center">
            <Spinner className="h-6 w-6" />
          </div>
        ) : messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center gap-1.5 text-center text-slate-400">
            <p className="text-sm font-medium text-slate-500">
              Ask ProdPilot AI about an incident
            </p>
            <p className="max-w-sm text-xs">
              Answers are grounded in your uploaded runbooks, logs, and dashboards, with
              citations back to the source.
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <ChatInput isSending={isSending} onSend={onSend} onStop={onStop} />
    </div>
  );
}
