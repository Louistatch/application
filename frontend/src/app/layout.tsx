import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Amẓarug Aqbayli — Agronome Kabyle",
  description: "Agent IA agronome qui parle kabyle",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="kab">
      <body>{children}</body>
    </html>
  );
}
