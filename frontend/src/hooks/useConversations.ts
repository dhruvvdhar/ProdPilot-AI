import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { conversationsApi } from "@/api/conversations";
import type { ConversationCreate } from "@/types";

export const conversationKeys = {
  all: ["conversations"] as const,
  messages: (id: number) => ["conversations", id, "messages"] as const,
};

export function useConversations() {
  return useQuery({
    queryKey: conversationKeys.all,
    queryFn: conversationsApi.list,
  });
}

export function useConversationMessages(conversationId: number | null) {
  return useQuery({
    queryKey: conversationId ? conversationKeys.messages(conversationId) : ["no-conversation"],
    queryFn: () => conversationsApi.messages(conversationId as number),
    enabled: conversationId !== null,
  });
}

export function useCreateConversation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: ConversationCreate = {}) => conversationsApi.create(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: conversationKeys.all });
    },
    onError: (error: Error) => toast.error(error.message),
  });
}

export function useDeleteConversation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (conversationId: number) => conversationsApi.remove(conversationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: conversationKeys.all });
    },
    onError: (error: Error) => toast.error(error.message),
  });
}
