import { FolderOpen } from "lucide-react";
import { DocumentUploader } from "@/components/documents/DocumentUploader";
import { DocumentRow } from "@/components/documents/DocumentRow";
import { FullPageSpinner } from "@/components/ui/Spinner";
import { useDocuments } from "@/hooks/useDocuments";

export function DocumentsPage() {
  const { data: documents, isLoading } = useDocuments();

  return (
    <div className="flex h-full w-full flex-col overflow-y-auto">
      <div className="border-b border-slate-200 bg-white px-6 py-4">
        <h1 className="text-lg font-semibold text-slate-900">Documents</h1>
        <p className="text-sm text-slate-500">
          Upload runbooks, logs, PDFs, and screenshots to ground ProdPilot AI's answers.
        </p>
      </div>

      <div className="flex-1 space-y-6 p-6">
        <DocumentUploader />

        {isLoading ? (
          <FullPageSpinner />
        ) : documents && documents.length > 0 ? (
          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-slate-100 text-xs font-medium uppercase tracking-wide text-slate-400">
                  <th className="py-2.5 pl-4 pr-2 font-medium">File</th>
                  <th className="px-2 py-2.5 font-medium">Parsing</th>
                  <th className="px-2 py-2.5 font-medium">Embedding</th>
                  <th className="px-2 py-2.5 font-medium">Vector store</th>
                  <th className="px-2 py-2.5 font-medium">Chunks</th>
                  <th className="py-2.5 pl-2 pr-4" />
                </tr>
              </thead>
              <tbody>
                {documents.map((document) => (
                  <DocumentRow key={document.id} document={document} />
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-slate-200 py-16 text-slate-400">
            <FolderOpen className="h-8 w-8" />
            <p className="text-sm">No documents uploaded yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
