import { useMemo, useState } from "react";
import type { KeyboardEvent } from "react";
import { Plus, MessageCircle, Trash2, Pencil, Search, Check, X } from "lucide-react";
import clsx from "clsx";
import { formatDistanceToNow } from "date-fns";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import {
  useConversations,
  useCreateConversation,
  useDeleteConversation,
  useRenameConversation,
} from "@/hooks/useConversations";
import { useChatUiStore } from "@/store/chatUiStore";
import type { ConversationResponse } from "@/types";

function safeFormatDistance(dateString: string): string {
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return "";
  return formatDistanceToNow(date, { addSuffix: true });
}


interface ConversationListProps {
  activeId: number | null;
  onSelect: (conversation: ConversationResponse) => void;
}

export function ConversationList({ activeId, onSelect }: ConversationListProps) {
  const { data: conversations, isLoading } = useConversations();
  const createConversation = useCreateConversation();
  const deleteConversation = useDeleteConversation();
  const renameConversation = useRenameConversation();

  const searchTerm = useChatUiStore((s) => s.searchTerm);
  const setSearchTerm = useChatUiStore((s) => s.setSearchTerm);

  const [pendingDelete, setPendingDelete] = useState<ConversationResponse | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState("");

  const filtered = useMemo(() => {
    if (!conversations) return [];
    const term = searchTerm.trim().toLowerCase();
    if (!term) return conversations;
    return conversations.filter((c) => c.title.toLowerCase().includes(term));
  }, [conversations, searchTerm]);

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

  const startEditing = (conversation: ConversationResponse) => {
    setEditingId(conversation.id);
    setEditValue(conversation.title);
  };

  const commitEdit = async (conversation: ConversationResponse) => {
    const trimmed = editValue.trim();
    setEditingId(null);

    if (!trimmed || trimmed === conversation.title) return;

    await renameConversation.mutateAsync({ id: conversation.id, title: trimmed });
  };

  const handleEditKeyDown = (e: KeyboardEvent<HTMLInputElement>, conversation: ConversationResponse) => {
    if (e.key === "Enter") {
      e.preventDefault();
      void commitEdit(conversation);
    } else if (e.key === "Escape") {
      setEditingId(null);
    }
  };

  return (
    <div className="flex h-full w-72 flex-shrink-0 flex-col border-r border-slate-200 bg-white">
      <div className="flex flex-col gap-2 border-b border-slate-100 p-3">
        <Button
          variant="primary"
          className="w-full"
          icon={<Plus className="h-4 w-4" />}
          onClick={handleCreate}
          isLoading={createConversation.isPending}
        >
          New chat
        </Button>

        <div className="relative">
          <Search className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400" />
          <input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search chats…"
            className="h-8 w-full rounded-lg border border-slate-200 bg-slate-50 pl-8 pr-2 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-200"
          />
        </div>
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

        {!isLoading && conversations && conversations.length > 0 && filtered.length === 0 && (
          <p className="px-2 py-6 text-center text-sm text-slate-400">
            No chats match "{searchTerm}".
          </p>
        )}

        <ul className="flex flex-col gap-1">
          {filtered.map((conversation) => {
            const isEditing = editingId === conversation.id;

            return (
              <li key={conversation.id}>
                <div
                  className={clsx(
                    "group flex w-full items-start gap-2 rounded-lg px-2.5 py-2 text-left text-sm transition-colors",
                    activeId === conversation.id
                      ? "bg-brand-50 text-brand-800"
                      : "text-slate-600 hover:bg-slate-50",
                  )}
                >
                  <MessageCircle className="mt-0.5 h-4 w-4 flex-shrink-0 opacity-60" />

                  {isEditing ? (
                    <div className="flex min-w-0 flex-1 items-center gap-1">
                      <input
                        autoFocus
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onKeyDown={(e) => handleEditKeyDown(e, conversation)}
                        onBlur={() => void commitEdit(conversation)}
                        className="min-w-0 flex-1 rounded border border-brand-300 bg-white px-1.5 py-0.5 text-sm focus:outline-none"
                      />
                      <button
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => void commitEdit(conversation)}
                        className="rounded p-1 text-emerald-600 hover:bg-emerald-50"
                      >
                        <Check className="h-3.5 w-3.5" />
                      </button>
                      <button
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => setEditingId(null)}
                        className="rounded p-1 text-slate-400 hover:bg-slate-100"
                      >
                        <X className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  ) : (
                    <button onClick={() => onSelect(conversation)} className="min-w-0 flex-1 text-left">
                      <span className="block truncate font-medium">{conversation.title}</span>
                      <span className="block truncate text-xs text-slate-400">
                        {safeFormatDistance(conversation.updated_at)}
                      </span>
                    </button>
                  )}

                  {!isEditing && (
                    <span className="flex flex-shrink-0 gap-0.5 opacity-0 transition-opacity group-hover:opacity-100">
                      <span
                        role="button"
                        tabIndex={0}
                        onClick={(e) => {
                          e.stopPropagation();
                          startEditing(conversation);
                        }}
                        className="mt-0.5 rounded p-1 text-slate-300 hover:bg-slate-100 hover:text-slate-600"
                      >
                        <Pencil className="h-3.5 w-3.5" />
                      </span>
                      <span
                        role="button"
                        tabIndex={0}
                        onClick={(e) => {
                          e.stopPropagation();
                          setPendingDelete(conversation);
                        }}
                        className="mt-0.5 rounded p-1 text-slate-300 hover:bg-red-50 hover:text-red-500"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </span>
                    </span>
                  )}
                </div>
              </li>
            );
          })}
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