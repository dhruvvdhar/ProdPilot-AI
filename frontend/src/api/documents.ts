import { apiClient } from "@/api/client";
import type { APIResponse, DocumentListResponse, DocumentResponse } from "@/types";

export const documentsApi = {
  async upload(file: File, onProgress?: (percent: number) => void): Promise<DocumentResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const { data } = await apiClient.post<APIResponse<DocumentResponse>>(
      "/documents/upload",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (event) => {
          if (!onProgress || !event.total) return;
          onProgress(Math.round((event.loaded / event.total) * 100));
        },
      },
    );

    return data.data as DocumentResponse;
  },

  async list(): Promise<DocumentResponse[]> {
    const { data } = await apiClient.get<APIResponse<DocumentListResponse>>("/documents/");
    return data.data?.documents ?? [];
  },

  async get(documentId: number): Promise<DocumentResponse> {
    const { data } = await apiClient.get<APIResponse<DocumentResponse>>(
      `/documents/${documentId}`,
    );
    return data.data as DocumentResponse;
  },

  async remove(documentId: number): Promise<void> {
    await apiClient.delete<APIResponse<null>>(`/documents/${documentId}`);
  },
};
