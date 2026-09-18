import type { AssistantState } from "../types";

interface Props {
  state: AssistantState;
  onStart: () => void;
  onStop: () => void;
  onStopSpeaking: () => void;
  disabled?: boolean;
}

export default function MicrophoneButton({
  state,
  onStart,
  onStop,
  onStopSpeaking,
  disabled,
}: Props) {
  const isListening = state === "listening";
  const isBusy = ["processing", "thinking"].includes(state);
  const isSpeaking = state === "speaking";

  const handleClick = () => {
    if (isSpeaking) {
      onStopSpeaking();
    } else if (isListening) {
      onStop();
    } else if (!isBusy) {
      onStart();
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={disabled || isBusy}
      className={`group relative w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 ${
        isListening
          ? "bg-red-500/20 border-2 border-red-400 shadow-[0_0_30px_rgba(239,68,68,0.4)]"
          : isSpeaking
            ? "bg-amber-500/20 border-2 border-amber-400"
            : "bg-white/5 border border-white/10 hover:border-blue-400/50 hover:bg-blue-500/10"
      } ${disabled || isBusy ? "opacity-40 cursor-not-allowed" : "cursor-pointer"}`}
      aria-label={isListening ? "Stop recording" : "Start recording"}
    >
      {isListening ? (
        <svg className="w-6 h-6 text-red-400" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="6" width="12" height="12" rx="2" />
        </svg>
      ) : isSpeaking ? (
        <svg className="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="6" width="4" height="12" />
          <rect x="14" y="6" width="4" height="12" />
        </svg>
      ) : (
        <svg
          className="w-7 h-7 text-gray-300 group-hover:text-blue-400 transition-colors"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z"
          />
        </svg>
      )}
    </button>
  );
}
