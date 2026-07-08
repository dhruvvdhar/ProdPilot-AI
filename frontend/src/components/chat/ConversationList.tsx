import { useState } from "react";
import { Plus, MessageCircle, Trash2 } from "lucide-react";
import clsx from "clsx";
import { formatDistanceToNow } from "date-fns";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import {
  useConversations,
  useCreateConversation,
  useDeleteConversation,
} from "@/hooks/useConversations";
import type { ConversationResponse } from "@/types";

interface ConversationListProps {
  activeId: number | null;
  onSelect: (conversation: ConversationResponse) => void;
}

export function ConversationList({ activeId, onSelect }: ConversationListProps) {
  const { data: conversations, isLoading } = useConversations();
  const createConversation = useCreateConversation();
  const deleteConversation = useDeleteConversation();
  const [pendingDelete, setPendingDelete] = useState<ConversationResponse | null>(null);

  const handleCreate = async () => {
    const conversation = await createConversation.mutateAsync({});
    onSelect(conversation);
  };

  const confirmDelete = async () => {
    if (!pendingDelete) return;
    await deleteConversation.mutateAsync(pendingDelete.id);
    if (activeId === pendingDelete.id) {
      const remaining = conversations?.filter((c) => c.id !== pendingDelete.id) ?? [];
      if (remaining[0]) onSelect(remaining[0]);
    }
    setPendingDelete(null);
  };

  return (
    <div className="flex h-full w-72 flex-shrink-0 flex-col border-r border-slate-200 bg-white">
      <div className="border-b border-slate-100 p-3">
        <Button
          variant="primary"
          className="w-full"
          icon={<Plus className="h-4 w-4" />}
          onClick={handleCreate}
          isLoading={createConversation.isPending}
        >
          New chat
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {isLoading && (
          <div className="flex justify-center py-6">
            <Spinner className="h-5 w-5" />
          </div>
        )}

        {!isLoading && conversations?.length === 0 && (
          <p className="px-2 py-6 text-center text-sm text-slate-400">
            No conversations yet. Start one above.
          </p>
        )}

        <ul className="flex flex-col gap-1">
          {conversations?.map((conversation) => (
            <li key={conversation.id}>
              <button
                onClick={() => onSelect(conversation)}
                className={clsx(
                  "group flex w-full items-start gap-2 rounded-lg px-2.5 py-2 text-left text-sm transition-colors",
                  activeId === conversation.id
                    ? "bg-brand-50 text-brand-800"
                    : "text-slate-600 hover:bg-slate-50",
                )}
              >
                <MessageCircle className="mt-0.5 h-4 w-4 flex-shrink-0 opacity-60" />
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium">{conversation.title}</span>
                  <span className="block truncate text-xs text-slate-400">
                    {formatDistanceToNow(new Date(conversation.updated_at), {
                      addSuffix: true,
                    })}
                  </span>
                </span>
                <span
                  role="button"
                  tabIndex={0}
                  onClick={(e) => {
                    e.stopPropagation();
                    setPendingDelete(conversation);
                  }}
                  className="mt-0.5 flex-shrink-0 rounded p-1 text-slate-300 opacity-0 transition-opacity hover:bg-red-50 hover:text-red-500 group-hover:opacity-100"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <ConfirmDialog
        open={Boolean(pendingDelete)}
        title="Delete conversation?"
        description={`"${pendingDelete?.title}" and all its messages will be permanently removed.`}
        isLoading={deleteConversation.isPending}
        onConfirm={confirmDelete}
        onCancel={() => setPendingDelete(null)}
      />
    </div>
  );
}
