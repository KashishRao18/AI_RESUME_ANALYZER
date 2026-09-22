/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#0F1720",
          900: "#16202B",
          800: "#1E2C3A",
          700: "#2A3B4C",
        },
        parchment: {
          100: "#F8F4EA",
          200: "#F1EADD",
          300: "#E7DCC7",
        },
        brass: {
          400: "#D9B54A",
          500: "#C9A227",
          600: "#A9840F",
        },
        sage: {
          400: "#7BAB92",
          500: "#5B9279",
          600: "#427260",
        },
        rust: {
          400: "#C97361",
          500: "#B4553F",
          600: "#8F4030",
        },
      },
      fontFamily: {
        display: ["Fraunces", "ui-serif", "Georgia", "serif"],
        body: ["'IBM Plex Sans'", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
      backgroundImage: {
        grain: "radial-gradient(circle at 1px 1px, rgba(255,255,255,0.035) 1px, transparent 0)",
      },
    },
  },
  plugins: [],
}
