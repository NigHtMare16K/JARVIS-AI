import { useState } from "react";
import AIOrb from "./components/AIOrb";
import Conversation from "./components/Conversation";
import MicrophoneButton from "./components/MicrophoneButton";
import { useJarvis } from "./hooks/useJarvis";
import type { AssistantState } from "./types";

const stateLabels: Record<AssistantState, string> = {
  sleeping: "Ready",
  listening: "Listening...",
  processing: "Processing...",
  thinking: "Thinking...",
  speaking: "Speaking...",
  error: "Error",
};

export default function App() {
  const {
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
  } = useJarvis();

  const [textInput, setTextInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (textInput.trim()) {
      sendMessage(textInput.trim());
      setTextInput("");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-8 relative">
      {/* Background subtle grid */}
      <div
        className="fixed inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(circle at 1px 1px, white 1px, transparent 0)",
          backgroundSize: "40px 40px",
        }}
      />

      {/* Header */}
      <header className="absolute top-6 flex items-center gap-3">
        <div
          className={`w-2 h-2 rounded-full ${connected ? "bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" : "bg-red-400"}`}
        />
        <span className="text-xs text-gray-500 tracking-widest uppercase">
          {connected ? "Connected" : "Offline"}
        </span>
      </header>

      {/* Title */}
      <h1 className="text-2xl font-light tracking-[0.3em] text-gray-300 mb-2">
        JARVIS
      </h1>

      {/* Active PDF indicator */}
      {activePdf && (
        <p className="text-xs text-blue-400/70 mb-4 truncate max-w-xs">
          📄 {activePdf}
        </p>
      )}

      {/* Orb */}
      <AIOrb state={state} />

      {/* Status */}
      <p
        className={`mt-6 text-sm tracking-wide transition-colors duration-300 ${
          state === "error" ? "text-red-400" : "text-gray-400"
        }`}
      >
        {error || stateLabels[state]}
      </p>

      {/* Microphone */}
      <div className="mt-8">
        <MicrophoneButton
          state={state}
          onStart={startListening}
          onStop={stopListening}
          onStopSpeaking={stopSpeaking}
          disabled={!connected}
        />
      </div>

      {/* Text input fallback */}
      <form onSubmit={handleSubmit} className="mt-6 w-full max-w-md flex gap-2">
        <input
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Or type a message..."
          disabled={!connected || state === "thinking"}
          className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-blue-500/50 disabled:opacity-40"
        />
        <button
          type="submit"
          disabled={!connected || !textInput.trim()}
          className="px-4 py-2 rounded-full bg-blue-600/30 border border-blue-500/30 text-sm text-blue-200 hover:bg-blue-600/50 disabled:opacity-30 transition-colors"
        >
          Send
        </button>
      </form>

      {/* Conversation */}
      <Conversation messages={messages} />

      {/* Actions */}
      {messages.length > 0 && (
        <button
          onClick={clearConversation}
          className="mt-4 text-xs text-gray-600 hover:text-gray-400 transition-colors"
        >
          Clear conversation
        </button>
      )}
    </div>
  );
}
