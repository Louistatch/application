export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  history: { role: string; content: string }[];
}

export interface TranslationRequest {
  text: string;
  direction: "fr_to_kab" | "kab_to_fr";
}
