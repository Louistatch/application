import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agronome Kabyè — Agent IA agricole",
  description: "Agent IA agronome qui parle kabyè (Togo)",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="kab">
      <body>{children}</body>
    </html>
  );
}
