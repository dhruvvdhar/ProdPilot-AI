import { useState } from "react";
import { FileText, FileImage, FileTerminal, Trash2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { StatusBadge } from "@/components/ui/Badge";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { useDeleteDocument } from "@/hooks/useDocuments";
import type { DocumentResponse } from "@/types";

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function FileIcon({ fileType }: { fileType: string }) {
  const type = fileType.toLowerCase();
  if (type.includes("png") || type.includes("jpg") || type.includes("jpeg")) {
    return <FileImage className="h-5 w-5 text-brand-500" />;
  }
  if (type.includes("log")) {
    return <FileTerminal className="h-5 w-5 text-brand-500" />;
  }
  return <FileText className="h-5 w-5 text-brand-500" />;
}

export function DocumentRow({ document }: { document: DocumentResponse }) {
  const [confirmOpen, setConfirmOpen] = useState(false);
  const deleteDocument = useDeleteDocument();

  const hasFailed =
    document.parse_status === "failed" ||
    document.embedding_status === "failed" ||
    document.vectorstore_status === "failed";

  return (
    <>
      <tr className="border-b border-slate-100 last:border-none hover:bg-slate-50">
        <td className="py-3 pl-4 pr-2">
          <div className="flex items-center gap-2.5">
            <FileIcon fileType={document.file_type} />
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-slate-800">{document.filename}</p>
              <p className="text-xs text-slate-400">
                {formatBytes(document.file_size)} ·{" "}
                {formatDistanceToNow(new Date(document.uploaded_at), { addSuffix: true })}
              </p>
            </div>
          </div>
        </td>
        <td className="px-2 py-3">
          <StatusBadge status={document.parse_status} />
        </td>
        <td className="px-2 py-3">
          <StatusBadge status={document.embedding_status} />
        </td>
        <td className="px-2 py-3">
          <StatusBadge status={document.vectorstore_status} />
        </td>
        <td className="px-2 py-3 text-sm text-slate-500">
          {document.chunk_count > 0 ? document.chunk_count : "—"}
        </td>
        <td className="py-3 pl-2 pr-4 text-right">
          <button
            onClick={() => setConfirmOpen(true)}
            className="rounded-md p-1.5 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-500"
            title="Delete document"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </td>
      </tr>
      {hasFailed && document.error_message && (
        <tr className="border-b border-slate-100 last:border-none">
          <td colSpan={6} className="bg-red-50 px-4 py-2 text-xs text-red-600">
            {document.error_message}
          </td>
        </tr>
      )}

      <ConfirmDialog
        open={confirmOpen}
        title="Delete document?"
        description={`"${document.filename}" will be removed along with its indexed content.`}
        isLoading={deleteDocument.isPending}
        onConfirm={async () => {
          await deleteDocument.mutateAsync(document.id);
          setConfirmOpen(false);
        }}
        onCancel={() => setConfirmOpen(false)}
      />
    </>
  );
}
