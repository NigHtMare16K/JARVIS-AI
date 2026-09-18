import type { Message } from "../types";

interface Props {
  messages: Message[];
}

export default function Conversation({ messages }: Props) {
  if (messages.length === 0) return null;

  return (
    <div className="w-full max-w-xl mx-auto mt-8 space-y-3 max-h-64 overflow-y-auto px-4 scrollbar-thin">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[85%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
              msg.role === "user"
                ? "bg-blue-600/20 text-blue-100 border border-blue-500/20"
                : "bg-white/5 text-gray-200 border border-white/5"
            }`}
          >
            {msg.content}
          </div>
        </div>
      ))}
    </div>
  );
}
