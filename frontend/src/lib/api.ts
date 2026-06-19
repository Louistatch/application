const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendChat(
  message: string,
  history: { role: string; content: string }[]
): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/v1/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.reply;
}

export async function* streamChat(
  message: string,
  history: { role: string; content: string }[]
): AsyncGenerator<string> {
  const res = await fetch(`${BASE_URL}/api/v1/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok || !res.body) throw new Error("Stream failed");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);
    const lines = text.split("\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const chunk = line.slice(6);
        if (chunk === "[DONE]") return;
        yield chunk;
      }
    }
  }
}

export async function translate(
  text: string,
  direction: "fr_to_kab" | "kab_to_fr"
): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/v1/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, direction }),
  });
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.translated;
}
