"use client";
import ReactMarkdown from "react-markdown";
import { Message } from "@/types";

interface Props {
  message: Message;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      {!isUser && (
        <div className="w-9 h-9 rounded-full bg-kabyle-blue flex items-center justify-center text-kabyle-gold font-bold text-sm mr-2 shrink-0">
          ⴰ
        </div>
      )}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-kabyle-blue text-white rounded-br-sm"
            : "bg-white border border-kabyle-sand text-gray-800 rounded-bl-sm shadow-sm"
        }`}
      >
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-1 last:mb-0">{children}</p>,
              strong: ({ children }) => (
                <strong className="font-semibold text-kabyle-blue">{children}</strong>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        <span className={`text-[10px] mt-1 block ${isUser ? "text-blue-200" : "text-gray-400"}`}>
          {new Date(message.timestamp).toLocaleTimeString("fr-FR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
      {isUser && (
        <div className="w-9 h-9 rounded-full bg-kabyle-gold flex items-center justify-center text-white font-bold text-sm ml-2 shrink-0">
          U
        </div>
      )}
    </div>
  );
}
