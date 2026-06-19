"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Trash2 } from "lucide-react";
import { v4 as uuidv4 } from "crypto";
import { streamChat } from "@/lib/api";
import { Message } from "@/types";
import ChatMessage from "./ChatMessage";

const WELCOME: Message = {
  id: "welcome",
  role: "assistant",
  content:
    "Azul ! Nekk d amẓarug aqbayli n tẓuṛt n wakal. Ttxil-k, d-ini-yi-d acu tebɣiḍ ad tesineḍ ɣef tẓuṛt n wakal — s teqbaylit neɣ s tafransist.\n\n**Bonjour !** Je suis votre agronome kabyle. Posez vos questions sur l'agriculture — en kabyle ou en français.",
  timestamp: new Date(),
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || streaming) return;

    const userMsg: Message = {
      id: Math.random().toString(36).slice(2),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    const assistantId = Math.random().toString(36).slice(2);
    const assistantMsg: Message = {
      id: assistantId,
      role: "assistant",
      content: "",
      timestamp: new Date(),
    };

    const history = messages
      .filter((m) => m.id !== "welcome")
      .map((m) => ({ role: m.role, content: m.content }));

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setInput("");
    setStreaming(true);

    try {
      for await (const chunk of streamChat(userMsg.content, history)) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, content: m.content + chunk } : m
          )
        );
      }
    } catch {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? { ...m, content: "Ttxil-k, ẓreɣ-d ccwal n uεqil. Ɛreḍ tikelt nniḍen." }
            : m
        )
      );
    } finally {
      setStreaming(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-kabyle-sand bg-white rounded-t-2xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-kabyle-blue flex items-center justify-center text-kabyle-gold font-bold text-lg">
            ⴰ
          </div>
          <div>
            <h1 className="font-semibold text-kabyle-blue text-sm">Amẓarug Aqbayli</h1>
            <p className="text-xs text-gray-500">Agronome · Tẓuṛt n Wakal</p>
          </div>
        </div>
        <button
          onClick={() => setMessages([WELCOME])}
          className="p-2 rounded-lg hover:bg-kabyle-sand transition-colors"
          title="Effacer la conversation"
        >
          <Trash2 size={16} className="text-gray-400" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1 bg-gray-50">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {streaming && messages[messages.length - 1]?.content === "" && (
          <div className="flex justify-start mb-4">
            <div className="bg-white border border-kabyle-sand rounded-2xl px-4 py-3 text-gray-400 text-sm">
              <Loader2 size={14} className="animate-spin inline mr-2" />
              Amẓarug yettwakkes...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t border-kabyle-sand rounded-b-2xl">
        <div className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Awal-ik/m... (Écrivez en kabyle ou en français)"
            rows={1}
            className="flex-1 resize-none border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-kabyle-blue max-h-32 overflow-y-auto"
            style={{ minHeight: "40px" }}
          />
          <button
            onClick={handleSend}
            disabled={streaming || !input.trim()}
            className="p-2.5 bg-kabyle-blue text-white rounded-xl hover:bg-opacity-90 disabled:opacity-40 transition-all"
          >
            <Send size={16} />
          </button>
        </div>
        <p className="text-[10px] text-gray-400 mt-1 text-center">
          Enter pour envoyer · Shift+Enter pour saut de ligne
        </p>
      </div>
    </div>
  );
}
