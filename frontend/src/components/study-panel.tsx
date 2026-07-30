"use client";

import type { CSSProperties } from "react";
import { useState } from "react";

import { askQuestion, generateQuiz, generateSummary } from "@/lib/api";
import { StudyResult } from "@/components/study-result";
import type { Citation, StoredDocument } from "@/types/api";

type StudyPanelProps = {
  documents: StoredDocument[];
};

type Mode = "ask" | "summarize" | "quiz";

export function StudyPanel({ documents }: StudyPanelProps) {
  const [mode, setMode] = useState<Mode>("ask");
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [busy, setBusy] = useState(false);

  const handleRun = async () => {
    if (!prompt.trim()) {
      setResult("Enter a question or topic first.");
      return;
    }

    try {
      setBusy(true);
      const response =
        mode === "ask"
          ? await askQuestion(prompt)
          : mode === "summarize"
            ? await generateSummary(prompt)
            : await generateQuiz(prompt);

      setResult(response.answer);
      setCitations(response.citations);
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Request failed.");
      setCitations([]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section style={panelStyle}>
      <h2 style={{ margin: 0 }}>2. Study Over Indexed Material</h2>
      <p style={copyStyle}>
        Indexed documents: {documents.length}. The UI is intentionally basic so the
        backend stays the real project.
      </p>

      <select
        value={mode}
        onChange={(event) => setMode(event.target.value as Mode)}
        style={inputStyle}
      >
        <option value="ask">Ask a question</option>
        <option value="summarize">Generate a summary</option>
        <option value="quiz">Generate a quiz</option>
      </select>

      <textarea
        rows={6}
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        placeholder={
          mode === "ask"
            ? "What is backpropagation and why does it work?"
            : mode === "summarize"
              ? "Neural network optimization"
              : "Gradient descent"
        }
        style={inputStyle}
      />

      <button
        type="button"
        disabled={busy}
        onClick={handleRun}
        style={buttonStyle}
      >
        {busy ? "Thinking..." : "Run"}
      </button>

      <div style={resultShellStyle}>
        <div style={resultHeaderStyle}>
          <div>
            <p style={eyebrowStyle}>Study Output</p>
            <h3 style={{ margin: "4px 0 0 0" }}>Result</h3>
          </div>
          <span style={modeBadgeStyle}>{mode}</span>
        </div>
        <div style={resultBoxStyle}>
          <StudyResult text={result} />
        </div>
      </div>

      <div style={citationShellStyle}>
        <div style={resultHeaderStyle}>
          <div>
            <p style={eyebrowStyle}>Grounding</p>
            <h3 style={{ margin: "4px 0 0 0" }}>Citations</h3>
          </div>
        </div>
        {citations.length === 0 ? (
          <p style={{ margin: 0, color: "var(--muted)" }}>No citations yet.</p>
        ) : (
          <ul style={citationListStyle}>
            {citations.map((citation) => (
              <li key={`${citation.filename}-${citation.chunk_index}`} style={citationCardStyle}>
                <div style={citationMetaRowStyle}>
                  <strong>{citation.filename}</strong>
                  <span style={citationPageStyle}>
                    {citation.page_number ? `Page ${citation.page_number}` : "Page n/a"}
                  </span>
                </div>
                <p style={citationSnippetStyle}>{citation.snippet}...</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
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

const copyStyle: CSSProperties = {
  margin: 0,
  color: "var(--muted)",
  lineHeight: 1.6,
};

const inputStyle: CSSProperties = {
  width: "100%",
  padding: 12,
  borderRadius: 12,
  border: "1px solid var(--border)",
  background: "#fff",
};

const buttonStyle: CSSProperties = {
  padding: "12px 16px",
  borderRadius: 12,
  border: "none",
  background: "#8a3b12",
  color: "white",
  cursor: "pointer",
};

const resultShellStyle: CSSProperties = {
  display: "grid",
  gap: 12,
};

const citationShellStyle: CSSProperties = {
  display: "grid",
  gap: 12,
  padding: 16,
  borderRadius: 18,
  background: "linear-gradient(180deg, rgba(216, 235, 232, 0.92), rgba(255, 253, 247, 0.95))",
  border: "1px solid rgba(24, 74, 69, 0.12)",
};

const resultHeaderStyle: CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "flex-start",
  gap: 12,
};

const eyebrowStyle: CSSProperties = {
  margin: 0,
  textTransform: "uppercase",
  letterSpacing: "0.12em",
  color: "var(--muted)",
  fontSize: 12,
};

const modeBadgeStyle: CSSProperties = {
  padding: "8px 10px",
  borderRadius: 999,
  background: "rgba(24, 74, 69, 0.1)",
  color: "var(--accent)",
  textTransform: "capitalize",
  fontSize: 13,
  fontWeight: 700,
};

const resultBoxStyle: CSSProperties = {
  padding: 20,
  borderRadius: 18,
  background: "linear-gradient(180deg, #eef7f6 0%, #f9fbf7 100%)",
  border: "1px solid rgba(24, 74, 69, 0.12)",
  boxShadow: "0 14px 28px rgba(24, 74, 69, 0.08)",
};

const citationListStyle: CSSProperties = {
  listStyle: "none",
  margin: 0,
  padding: 0,
  display: "grid",
  gap: 12,
};

const citationCardStyle: CSSProperties = {
  padding: 14,
  borderRadius: 14,
  background: "rgba(255, 255, 255, 0.78)",
  border: "1px solid rgba(24, 74, 69, 0.12)",
};

const citationMetaRowStyle: CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  gap: 12,
  alignItems: "center",
  marginBottom: 8,
};

const citationPageStyle: CSSProperties = {
  fontSize: 12,
  color: "var(--muted)",
  textTransform: "uppercase",
  letterSpacing: "0.08em",
};

const citationSnippetStyle: CSSProperties = {
  margin: 0,
  lineHeight: 1.7,
  color: "var(--muted)",
};
