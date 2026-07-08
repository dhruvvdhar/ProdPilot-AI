import { useRef, useState } from "react";
import type { DragEvent } from "react";
import { UploadCloud } from "lucide-react";
import toast from "react-hot-toast";
import clsx from "clsx";
import { useUploadDocument } from "@/hooks/useDocuments";

const ACCEPTED_EXTENSIONS = [".pdf", ".txt", ".log", ".png", ".jpg", ".jpeg"];
const MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024;

function validate(file: File): string | null {
  const extension = `.${file.name.split(".").pop()?.toLowerCase() ?? ""}`;
  if (!ACCEPTED_EXTENSIONS.includes(extension)) {
    return `Unsupported file type "${extension}". Accepted: ${ACCEPTED_EXTENSIONS.join(", ")}`;
  }
  if (file.size === 0) {
    return "File is empty.";
  }
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "File exceeds the maximum allowed size (20 MB).";
  }
  return null;
}

export function DocumentUploader() {
  const [isDragging, setIsDragging] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const upload = useUploadDocument();

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;

    for (const file of Array.from(files)) {
      const error = validate(file);
      if (error) {
        toast.error(error);
        continue;
      }

      setProgress(0);
      try {
        await upload.mutateAsync({ file, onProgress: setProgress });
      } finally {
        setProgress(null);
      }
    }
  };

  return (
    <div
      onDragOver={(e: DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e: DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        void handleFiles(e.dataTransfer.files);
      }}
      onClick={() => inputRef.current?.click()}
      className={clsx(
        "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors",
        isDragging ? "border-brand-400 bg-brand-50" : "border-slate-200 bg-white hover:bg-slate-50",
      )}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={ACCEPTED_EXTENSIONS.join(",")}
        className="hidden"
        onChange={(e) => void handleFiles(e.target.files)}
      />
      <UploadCloud className="h-8 w-8 text-brand-500" />
      <p className="text-sm font-medium text-slate-700">
        Drop runbooks, logs, PDFs, or screenshots here
      </p>
      <p className="text-xs text-slate-400">
        {ACCEPTED_EXTENSIONS.join(", ")} · up to 20 MB
      </p>

      {progress !== null && (
        <div className="mt-2 h-1.5 w-48 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full brand-gradient transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}
