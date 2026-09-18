/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        jarvis: {
          bg: "#0a0e17",
          surface: "#111827",
          accent: "#3b82f6",
          glow: "#60a5fa",
          muted: "#6b7280",
        },
      },
      animation: {
        pulse_slow: "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        spin_slow: "spin 8s linear infinite",
      },
    },
  },
  plugins: [],
};
