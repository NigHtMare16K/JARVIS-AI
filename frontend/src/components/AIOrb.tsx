import type { AssistantState } from "../types";

interface Props {
  state: AssistantState;
  audioLevel?: number;
}

const stateColors: Record<AssistantState, string> = {
  sleeping: "from-blue-900/40 to-indigo-900/20",
  listening: "from-blue-500/60 to-cyan-400/40",
  processing: "from-violet-500/50 to-blue-500/30",
  thinking: "from-purple-500/50 to-indigo-500/30",
  speaking: "from-emerald-500/50 to-blue-500/40",
  error: "from-red-500/40 to-orange-500/20",
};

export default function AIOrb({ state, audioLevel = 0 }: Props) {
  const scale = state === "listening" ? 1 + audioLevel * 0.15 : 1;
  const pulse =
    state === "listening" || state === "speaking" || state === "thinking";

  return (
    <div className="relative flex items-center justify-center w-48 h-48">
      {/* Outer glow ring */}
      <div
        className={`absolute inset-0 rounded-full bg-gradient-to-br ${stateColors[state]} blur-2xl opacity-60 ${pulse ? "animate-pulse_slow" : ""}`}
      />

      {/* Rotating ring */}
      {(state === "thinking" || state === "processing") && (
        <div className="absolute inset-2 rounded-full border border-blue-400/20 border-t-blue-400/60 animate-spin_slow" />
      )}

      {/* Core orb */}
      <div
        className={`relative w-32 h-32 rounded-full bg-gradient-to-br ${stateColors[state]} border border-white/10 shadow-[0_0_60px_rgba(59,130,246,0.3)] transition-transform duration-150`}
        style={{ transform: `scale(${scale})` }}
      >
        <div className="absolute inset-3 rounded-full bg-gradient-to-t from-transparent to-white/10" />
      </div>
    </div>
  );
}
