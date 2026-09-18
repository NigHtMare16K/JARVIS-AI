import { useCallback, useEffect, useRef, useState } from "react";
import { fetchStatus, sendText, sendVoice } from "../api/client";
import type { AssistantState, Message } from "../types";

const SESSION_ID = "frontend_session";

export function useJarvis() {
  const [state, setState] = useState<AssistantState>("sleeping");
  const [messages, setMessages] = useState<Message[]>([]);
  const [connected, setConnected] = useState(false);
  const [activePdf, setActivePdf] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const check = async () => {
      try {
        const status = await fetchStatus();
        setConnected(true);
        setActivePdf(status.active_pdf);
      } catch {
        setConnected(false);
      }
    };
    check();
    const interval = setInterval(check, 10000);
    return () => clearInterval(interval);
  }, []);

  const addMessage = useCallback((role: "user" | "assistant", content: string) => {
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role, content, timestamp: new Date() },
    ]);
  }, []);

  const stopSpeaking = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setState("sleeping");
  }, []);

  const playAudio = useCallback((url: string) => {
    return new Promise<void>((resolve) => {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      const audio = new Audio(url);
      audioRef.current = audio;
      setState("speaking");
      audio.onended = () => {
        setState("sleeping");
        resolve();
      };
      audio.onerror = () => {
        setState("sleeping");
        resolve();
      };
      audio.play().catch(() => {
        setState("sleeping");
        resolve();
      });
    });
  }, []);

  const processRecording = useCallback(
    async (blob: Blob) => {
      setState("processing");
      try {
        setState("thinking");
        const { audioUrl, text, answer } = await sendVoice(blob, SESSION_ID);
        if (text) addMessage("user", text);
        if (answer) addMessage("assistant", answer);
        await playAudio(audioUrl);
        URL.revokeObjectURL(audioUrl);
        setError(null);
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Something went wrong";
        setError(msg);
        setState("error");
      }
    },
    [addMessage, playAudio]
  );

  const startListening = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/wav" });
        if (blob.size > 0) await processRecording(blob);
        else setState("sleeping");
      };

      recorder.start();
      setState("listening");
    } catch {
      setError("Microphone access denied");
      setState("error");
    }
  }, [processRecording]);

  const stopListening = useCallback(() => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
      setState("processing");
    }
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;
      addMessage("user", text);
      setState("thinking");
      try {
        const answer = await sendText(text, SESSION_ID);
        addMessage("assistant", answer);
        setState("sleeping");
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Chat failed");
        setState("error");
      }
    },
    [addMessage]
  );

  const clearConversation = useCallback(() => {
    setMessages([]);
    setState("sleeping");
    setError(null);
  }, []);

  return {
    state,
    messages,
    connected,
    activePdf,
    error,
    startListening,
    stopListening,
    stopSpeaking,
    sendMessage,
    clearConversation,
  };
}
