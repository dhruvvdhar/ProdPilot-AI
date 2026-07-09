import { create } from "zustand";

interface ChatUiState {
  activeConversationId: number | null;
  searchTerm: string;
  setActiveConversationId: (id: number | null) => void;
  setSearchTerm: (term: string) => void;
}

export const useChatUiStore = create<ChatUiState>((set) => ({
  activeConversationId: null,
  searchTerm: "",
  setActiveConversationId: (id) => set({ activeConversationId: id }),
  setSearchTerm: (term) => set({ searchTerm: term }),
}));