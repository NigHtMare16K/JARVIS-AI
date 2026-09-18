export type AssistantState =
  | "sleeping"
  | "listening"
  | "processing"
  | "thinking"
  | "speaking"
  | "error";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface AssistantStatus {
  status: string;
  active_window: string | null;
  active_pdf: string | null;
  active_sessions: number;
}
