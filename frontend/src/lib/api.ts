import type {
  DocumentIngestResponse,
  DocumentListResponse,
  StudyResponse,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const data = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(data?.detail ?? "Request failed.");
  }

  return (await response.json()) as T;
}

export async function uploadDocument(file: File): Promise<DocumentIngestResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return request<DocumentIngestResponse>("/api/documents/upload", {
    method: "POST",
    body: formData,
  });
}

export async function listDocuments(): Promise<DocumentListResponse> {
  return request<DocumentListResponse>("/api/documents");
}

export async function askQuestion(question: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
}

export async function routeStudyRequest(userInput: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: userInput }),
  });
}

export async function generateSummary(topic: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });
}

export async function explainSimply(topic: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/explain-simple", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });
}

export async function generateQuiz(topic: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/quiz", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });
}

export async function compareTopics(topicA: string, topicB: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic_a: topicA, topic_b: topicB }),
  });
}

export async function generateChecklist(topic: string): Promise<StudyResponse> {
  return request<StudyResponse>("/api/study/checklist", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic }),
  });
}
