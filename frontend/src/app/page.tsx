"use client";

import { useEffect, useState } from "react";

import { StudyPanel } from "@/components/study-panel";
import { UploadForm } from "@/components/upload-form";
import { listDocuments } from "@/lib/api";
import type { StoredDocument } from "@/types/api";

export default function HomePage() {
  const [documents, setDocuments] = useState<StoredDocument[]>([]);

  const refreshDocuments = async () => {
    const response = await listDocuments();
    setDocuments(response.documents);
  };

  useEffect(() => {
    void refreshDocuments();
  }, []);

  return (
    <main
      style={{
        width: "min(100%, 1400px)",
        margin: "0 auto",
        display: "grid",
        gap: 20,
      }}
    >
      <section
        style={{
          padding: 24,
          border: "1px solid var(--border)",
          borderRadius: 20,
          background: "rgba(255, 253, 247, 0.92)",
        }}
      >
        <h1 style={{ marginBottom: 8 }}>Coursework Copilot</h1>
        <p style={{ marginTop: 0, maxWidth: 760, lineHeight: 1.6 }}>
          Start with a clean retrieval pipeline. Upload course material, screenshots of
          notes, or slide images, then generate grounded study outputs from your own data.
        </p>
      </section>

      <section
        className="workspace-grid"
        style={{
          display: "grid",
          gap: 20,
          gridTemplateColumns: "minmax(0, 0.8fr) minmax(0, 1.2fr)",
        }}
      >
        <UploadForm onUploaded={refreshDocuments} />
        <StudyPanel documents={documents} />
      </section>
    </main>
  );
}
