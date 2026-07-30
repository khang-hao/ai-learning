export type DocumentIngestResponse = {
  document_id: string;
  filename: string;
  chunk_count: number;
  page_count: number;
  saved_path: string;
};

export type StoredDocument = {
  document_id: string;
  filename: string;
  chunk_count: number;
};

export type DocumentListResponse = {
  documents: StoredDocument[];
};

export type Citation = {
  filename: string;
  page_number: number | null;
  chunk_index: number;
  snippet: string;
};

export type StudyResponse = {
  answer: string;
  citations: Citation[];
};
