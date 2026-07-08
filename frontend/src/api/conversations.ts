import { apiClient } from "@/api/client";
import type { ConversationCreate, ConversationResponse, MessageResponse } from "@/types";

export const conversationsApi = {
  async list(): Promise<ConversationResponse[]> {
    const { data } = await apiClient.get<ConversationResponse[]>("/conversations");
    return data;
  },

  async create(payload: ConversationCreate = {}): Promise<ConversationResponse> {
    const { data } = await apiClient.post<ConversationResponse>("/conversations", payload);
    return data;
  },

  async get(conversationId: number): Promise<ConversationResponse> {
    const { data } = await apiClient.get<ConversationResponse>(
      `/conversations/${conversationId}`,
    );
    return data;
  },

  async remove(conversationId: number): Promise<void> {
    await apiClient.delete(`/conversations/${conversationId}`);
  },

  async messages(conversationId: number): Promise<MessageResponse[]> {
    const { data } = await apiClient.get<MessageResponse[]>(
      `/conversations/${conversationId}/messages`,
    );
    return data;
  },
};
