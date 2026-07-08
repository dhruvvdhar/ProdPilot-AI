import { useEffect, useState } from "react";
import { ConversationList } from "@/components/chat/ConversationList";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { useConversationMessages, useConversations } from "@/hooks/useConversations";
import { useChat } from "@/hooks/useChat";
import type { ConversationResponse } from "@/types";

export function ChatPage() {
  const { data: conversations } = useConversations();
  const [activeConversation, setActiveConversation] = useState<ConversationResponse | null>(
    null,
  );

  // Default to the most recent conversation on first load.
  useEffect(() => {
    if (!activeConversation && conversations && conversations.length > 0) {
      setActiveConversation(conversations[0]);
    }
  }, [conversations, activeConversation]);

  const { data: history, isLoading: isLoadingHistory } = useConversationMessages(
    activeConversation?.id ?? null,
  );

  const { messages, isSending, send, stop } = useChat(activeConversation?.id ?? null, history);

  return (
    <div className="flex h-full min-h-0 w-full">
      <ConversationList
        activeId={activeConversation?.id ?? null}
        onSelect={setActiveConversation}
      />
      <ChatWindow
        conversation={activeConversation}
        messages={messages}
        isLoadingHistory={isLoadingHistory}
        isSending={isSending}
        onSend={send}
        onStop={stop}
      />
    </div>
  );
}
