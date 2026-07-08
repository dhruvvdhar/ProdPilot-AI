import { useCallback, useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { ApiError } from "@/api/client";
import { streamChat } from "@/api/chat";
import { conversationKeys } from "@/hooks/useConversations";
import type { ChatMessage, MessageResponse } from "@/types";

function fromServerMessage(message: MessageResponse): ChatMessage {
  return {
    id: String(message.id),
    role: message.role === "assistant" ? "assistant" : "user",
    content: message.content,
    created_at: message.created_at,
  };
}

export function useChat(conversationId: number | null, history: MessageResponse[] | undefined) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const queryClient = useQueryClient();

  // Hydrate local thread whenever the active conversation (and its
  // fetched history) changes.
  useEffect(() => {
    setMessages(history ? history.map(fromServerMessage) : []);
  }, [conversationId, history]);

  const send = useCallback(
    async (question: string) => {
      if (!conversationId || !question.trim() || isSending) return;

      const userMessage: ChatMessage = {
        id: `local-user-${Date.now()}`,
        role: "user",
        content: question,
        created_at: new Date().toISOString(),
      };

      const assistantId = `local-assistant-${Date.now()}`;
      const assistantMessage: ChatMessage = {
        id: assistantId,
        role: "assistant",
        content: "",
        created_at: new Date().toISOString(),
        pending: true,
      };

      setMessages((prev) => [...prev, userMessage, assistantMessage]);
      setIsSending(true);

      const controller = new AbortController();
      abortRef.current = controller;

      let receivedAnyToken = false;

      try {
        for await (const event of streamChat(
          { conversation_id: conversationId, question },
          controller.signal,
        )) {
          if (event.type === "token") {
            receivedAnyToken = true;
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, content: m.content + event.data } : m,
              ),
            );
          } else if (event.type === "citations") {
            setMessages((prev) =>
              prev.map((m) => (m.id === assistantId ? { ...m, citations: event.data } : m)),
            );
          }
        }

        if (!receivedAnyToken) {
          throw new ApiError(
            "ProdPilot AI couldn't generate a response for that question.",
          );
        }

        setMessages((prev) =>
          prev.map((m) => (m.id === assistantId ? { ...m, pending: false } : m)),
        );
      } catch (error) {
        const message = error instanceof Error ? error.message : "Something went wrong.";
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, pending: false, error: true, content: m.content || message }
              : m,
          ),
        );
        toast.error(message);
      } finally {
        setIsSending(false);
        queryClient.invalidateQueries({ queryKey: conversationKeys.all });
        queryClient.invalidateQueries({
          queryKey: conversationKeys.messages(conversationId),
        });
      }
    },
    [conversationId, isSending, queryClient],
  );

  const stop = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return { messages, isSending, send, stop };
}
