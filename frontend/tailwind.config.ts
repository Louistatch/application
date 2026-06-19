import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        kabyle: {
          blue: "#1a3c5e",
          gold: "#c9a227",
          green: "#2d6a4f",
          sand: "#f4e6c8",
        },
      },
      fontFamily: {
        tifinagh: ["Noto Sans Tifinagh", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
