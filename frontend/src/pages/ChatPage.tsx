import { useEffect } from "react";
import { ConversationList } from "@/components/chat/ConversationList";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { useConversationMessages, useConversations } from "@/hooks/useConversations";
import { useChat } from "@/hooks/useChat";
import { useChatUiStore } from "@/store/chatUiStore";

export function ChatPage() {
  const { data: conversations } = useConversations();
  const activeConversationId = useChatUiStore((s) => s.activeConversationId);
  const setActiveConversationId = useChatUiStore((s) => s.setActiveConversationId);

  // Only auto-select the most recent conversation if nothing has ever
  // been picked yet — this no longer re-runs every time the page remounts.
  useEffect(() => {
    if (!activeConversationId && conversations && conversations.length > 0) {
      setActiveConversationId(conversations[0].id);
    }
  }, [conversations, activeConversationId, setActiveConversationId]);

  const activeConversation = conversations?.find((c) => c.id === activeConversationId) ?? null;

  const { data: history, isLoading: isLoadingHistory } = useConversationMessages(
    activeConversationId,
  );

  const { messages, isSending, send, stop } = useChat(activeConversationId, history);

  return (
    <div className="flex h-full min-h-0 w-full">
      <ConversationList
        activeId={activeConversationId}
        onSelect={(conversation) => setActiveConversationId(conversation.id)}
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