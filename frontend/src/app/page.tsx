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
        maxWidth: 1100,
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
        <p
          style={{
            margin: 0,
            textTransform: "uppercase",
            letterSpacing: "0.12em",
            color: "var(--muted)",
            fontSize: 12,
          }}
        >
          Resume-focused AI project
        </p>
        <h1 style={{ marginBottom: 8 }}>Coursework Copilot</h1>
        <p style={{ marginTop: 0, maxWidth: 760, lineHeight: 1.6 }}>
          Start with a clean retrieval pipeline. Upload course material, ask grounded
          questions, and generate study outputs like summaries, quizzes, comparisons,
          and revision checklists from your own notes.
        </p>
      </section>

      <section
        style={{
          display: "grid",
          gap: 20,
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
        }}
      >
        <UploadForm onUploaded={refreshDocuments} />
        <StudyPanel documents={documents} />
      </section>
    </main>
  );
}
