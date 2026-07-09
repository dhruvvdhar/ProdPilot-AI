/**
 * These types mirror the FastAPI Pydantic schemas 1:1
 * (see app/schemas/*.py in the backend). Keep them in
 * sync with the backend when the API changes.
 */

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
}

export interface ErrorResponse {
  success: false;
  message: string;
  errors?: string[];
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

export interface UserResponse {
  id: number;
  username: string;
  email: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// ---------------------------------------------------------------------------
// Conversations
// ---------------------------------------------------------------------------

export interface ConversationResponse {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationCreate {
  title?: string | null;
}

export interface ConversationUpdate {
  title: string;
}

// ---------------------------------------------------------------------------
// Messages
// ---------------------------------------------------------------------------

export type MessageRole = "user" | "assistant";

export interface MessageResponse {
  id: number;
  role: string;
  content: string;
  created_at: string;
  citations: Citation[];
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

export interface Citation {
  filename: string;
  page: number | null;
}

export interface ChatRequest {
  conversation_id: number;
  question: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
}

/** Client-side only representation used to render the chat thread optimistically. */
export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  citations?: Citation[];
  created_at: string;
  pending?: boolean;
  error?: boolean;
}

// ---------------------------------------------------------------------------
// Documents
// ---------------------------------------------------------------------------

export type PipelineStatus = "pending" | "processing" | "completed" | "failed" | string;

export interface DocumentResponse {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  uploaded_at: string;
  parse_status: PipelineStatus;
  embedding_status: PipelineStatus;
  vectorstore_status: PipelineStatus;
  vector_count: number;
  chunk_count: number;
  error_message: string | null;
  processing_started_at: string | null;
  processing_completed_at: string | null;
}

export interface DocumentListResponse {
  documents: DocumentResponse[];
}
