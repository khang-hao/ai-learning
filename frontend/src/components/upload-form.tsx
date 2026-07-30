"use client";

import type { CSSProperties, FormEvent } from "react";
import { useState } from "react";

import { uploadDocument } from "@/lib/api";

type UploadFormProps = {
  onUploaded: () => Promise<void>;
};

export function UploadForm({ onUploaded }: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("Upload a PDF, TXT, or MD file.");
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setStatus("Choose a file first.");
      return;
    }

    try {
      setBusy(true);
      const result = await uploadDocument(file);
      setStatus(
        `Indexed ${result.filename} with ${result.chunk_count} chunks across ${result.page_count} pages.`
      );
      setFile(null);
      await onUploaded();
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={panelStyle}
    >
      <h2 style={headingStyle}>1. Upload Material</h2>
      <p style={copyStyle}>
        Keep v1 narrow. If your slides are in PowerPoint, export them to PDF first.
      </p>
      <input
        type="file"
        accept=".pdf,.txt,.md"
        onChange={(event) => setFile(event.target.files?.[0] ?? null)}
      />
      <button
        type="submit"
        disabled={busy}
        style={buttonStyle}
      >
        {busy ? "Indexing..." : "Upload and Index"}
      </button>
      <p style={statusStyle}>{status}</p>
    </form>
  );
}

const panelStyle: CSSProperties = {
  display: "grid",
  gap: 14,
  padding: 20,
  border: "1px solid var(--border)",
  borderRadius: 20,
  background: "var(--panel)",
};

const headingStyle: CSSProperties = {
  margin: 0,
};

const copyStyle: CSSProperties = {
  margin: 0,
  color: "var(--muted)",
  lineHeight: 1.6,
};

const buttonStyle: CSSProperties = {
  padding: "12px 16px",
  borderRadius: 12,
  border: "none",
  background: "var(--accent)",
  color: "white",
  cursor: "pointer",
};

const statusStyle: CSSProperties = {
  margin: 0,
  color: "var(--muted)",
};
