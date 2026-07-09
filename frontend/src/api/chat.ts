import { API_BASE_URL, apiClient, ApiError } from "@/api/client";
import { tokenStorage } from "@/lib/tokenStorage";
import type { APIResponse, ChatRequest, ChatResponse, Citation } from "@/types";

export const chatApi = {
  async send(payload: ChatRequest): Promise<ChatResponse> {
    const { data } = await apiClient.post<APIResponse<ChatResponse>>("/chat/", payload);
    return data.data as ChatResponse;
  },
};

export type StreamEvent =
  | { type: "token"; data: string }
  | { type: "citations"; data: Citation[] }
  | { type: "error"; data: string }
  | { type: "done" };

/**
 * Consumes the backend's `/chat/stream` endpoint.
 *
 * The endpoint is a POST request emitting a text/event-stream body
 * (`event: <type>\ndata: <json>\n\n` frames), so the native `EventSource`
 * API can't be used (it only supports GET). We read the fetch body
 * stream manually and parse frames as they arrive.
 */
export async function* streamChat(
  payload: ChatRequest,
  signal?: AbortSignal,
): AsyncGenerator<StreamEvent> {
  const token = tokenStorage.get();

  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(payload),
    signal,
  });

  if (!response.ok || !response.body) {
    let message = "Failed to reach ProdPilot AI.";
    try {
      const errorBody = await response.json();
      message = errorBody.detail || errorBody.message || message;
    } catch {
      /* response body wasn't JSON, keep default message */
    }
    throw new ApiError(message, response.status);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";

    for (const frame of frames) {
      const lines = frame.split("\n");
      let eventType = "message";
      let rawData = "";

      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventType = line.slice("event:".length).trim();
        } else if (line.startsWith("data:")) {
          rawData += line.slice("data:".length).trim();
        }
      }

      if (eventType === "done") {
        yield { type: "done" };
        continue;
      }

      if (!rawData) continue;

      try {
        const parsed = JSON.parse(rawData);
        if (eventType === "token") {
          yield { type: "token", data: parsed as string };
        } else if (eventType === "citations") {
          yield { type: "citations", data: parsed as Citation[] };
        } else if (eventType === "error") {
          yield { type: "error", data: parsed as string };
        }
      } catch {
        /* ignore malformed frame */
      }
    }
  }
}