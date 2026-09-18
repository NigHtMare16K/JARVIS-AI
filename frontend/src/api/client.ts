const API_BASE = import.meta.env.VITE_API_URL || "/api";

export async function fetchStatus(): Promise<{
  status: string;
  active_window: string | null;
  active_pdf: string | null;
}> {
  const res = await fetch(`${API_BASE}/assistant/status`);
  if (!res.ok) throw new Error("Backend unreachable");
  return res.json();
}

export async function sendVoice(
  audioBlob: Blob,
  sessionId: string
): Promise<{ audioUrl: string; text: string; answer: string }> {
  const form = new FormData();
  form.append("audio", audioBlob, "input.wav");
  form.append("session_id", sessionId);

  const res = await fetch(`${API_BASE}/voice/`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Voice request failed" }));
    throw new Error(err.detail || "Voice request failed");
  }

  const text = decodeURIComponent(res.headers.get("X-Transcribed-Text") || "");
  const answer = decodeURIComponent(res.headers.get("X-Answer-Text") || "");
  const audioBlob2 = await res.blob();
  const audioUrl = URL.createObjectURL(audioBlob2);

  return { audioUrl, text, answer };
}

export async function sendText(
  message: string,
  sessionId: string
): Promise<string> {
  const res = await fetch(`${API_BASE}/chat/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!res.ok) throw new Error("Chat request failed");
  const data = await res.json();
  return data.answer;
}
