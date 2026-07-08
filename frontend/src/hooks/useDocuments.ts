import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { documentsApi } from "@/api/documents";
import type { DocumentResponse } from "@/types";

const documentsKey = ["documents"] as const;

function hasActivePipeline(documents: DocumentResponse[] | undefined): boolean {
  if (!documents) return false;
  return documents.some(
    (doc) =>
      doc.parse_status === "pending" ||
      doc.parse_status === "processing" ||
      doc.embedding_status === "pending" ||
      doc.embedding_status === "processing" ||
      doc.vectorstore_status === "pending" ||
      doc.vectorstore_status === "processing",
  );
}

export function useDocuments() {
  const query = useQuery({
    queryKey: documentsKey,
    queryFn: documentsApi.list,
    refetchInterval: (q) => (hasActivePipeline(q.state.data) ? 3000 : false),
  });

  return query;
}

export function useUploadDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      file,
      onProgress,
    }: {
      file: File;
      onProgress?: (percent: number) => void;
    }) => documentsApi.upload(file, onProgress),
    onSuccess: (doc) => {
      queryClient.invalidateQueries({ queryKey: documentsKey });
      toast.success(`"${doc.filename}" uploaded — processing started.`);
    },
    onError: (error: Error) => toast.error(error.message),
  });
}

export function useDeleteDocument() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (documentId: number) => documentsApi.remove(documentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: documentsKey });
      toast.success("Document deleted.");
    },
    onError: (error: Error) => toast.error(error.message),
  });
}
